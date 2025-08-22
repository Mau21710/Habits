import streamlit as st
import pandas as pd
import datetime
import csv
import os
from config_loader import show_debug

def run_category_page(category, activities, params):
    st.title(f"📊 {category['name']}")

    # Carica log attività
    log_columns = ["timestamp", "category", "label", "points"]
    try:
        df_log = pd.read_csv("activity_log.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_log = pd.DataFrame(columns=log_columns)

    # Filtra log per categoria e settimana corrente
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    if not df_log.empty and 'timestamp' in df_log.columns:
        df_log['timestamp'] = pd.to_datetime(df_log['timestamp'])
        df_cat = df_log[(df_log["category"] == category["name"]) & (df_log["timestamp"].dt.date >= week_start)]
    else:
        df_cat = pd.DataFrame(columns=log_columns)

    # Calcola percentuale completamento
    weekly_goal = category.get("weekly_goal", 100)
    total_points = df_cat["points"].sum() if not df_cat.empty else 0
    percent_complete = min(100, int(total_points / weekly_goal * 100))
    st.metric("Completamento settimana", f"{percent_complete}%")

    # Form inserimento manuale
    st.subheader("Aggiungi attività manuale")
    manual_label = st.text_input("Nome attività")
    manual_points = st.number_input("Punti", min_value=1, step=1)
    if st.button("Aggiungi manualmente"):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "category": category["name"],
            "label": manual_label,
            "points": manual_points
        }
        df_log = pd.concat([df_log, pd.DataFrame([log_entry])], ignore_index=True)
        append_activity_log(log_entry, log_columns)
        st.success(f"Aggiunta manuale: {manual_label} (+{manual_points} punti)")
        st.rerun()

    # Attività ordinate per data (mai fatta per prima)
    st.subheader("Attività disponibili")
    done_labels = set(df_cat["label"])

    activities_for_page = {a['label']: a for a in activities if a['category'] == category['name']}.values()

    sorted_activities = sorted(
        activities_for_page,
        key=lambda a: (a["label"] in done_labels, df_cat[df_cat["label"] == a["label"]]["timestamp"].max() if a["label"] in done_labels else pd.Timestamp.min)
    )
    for act in sorted_activities:
        if st.button(f"➕ {act['label']} ({act['points']} punti)"):
            activity_label = act['label']
            
            all_entries_for_activity = [a for a in activities if a['label'] == activity_label]
            
            new_log_entries = []
            for entry in all_entries_for_activity:
                log_entry = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "category": entry["category"],
                    "label": entry["label"],
                    "points": entry["points"]
                }
                new_log_entries.append(log_entry)

            for log in new_log_entries:
                df_log = pd.concat([df_log, pd.DataFrame([log])], ignore_index=True)
                append_activity_log(log, log_columns)

            categories_str = ", ".join(e["category"] for e in all_entries_for_activity)
            st.success(f"Aggiunta attività: {activity_label} (+{act['points']} punti a: {categories_str})")
            st.rerun()

    show_debug(params)

def append_activity_log(entry, fieldnames):
    with open("activity_log.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(entry)