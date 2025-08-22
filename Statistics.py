import streamlit as st
import pandas as pd
import os, datetime
from config_loader import show_debug

def run_statistics_page(categories, activities, params):
    st.title("📊 Statistiche settimanali")

    log_columns = ["timestamp", "category", "label", "points"]
    try:
        log = pd.read_csv("activity_log.csv")
        if 'timestamp' not in log.columns and 'date' in log.columns:
            log.rename(columns={'date': 'timestamp'}, inplace=True)
        log["timestamp"] = pd.to_datetime(log["timestamp"], format='ISO8601')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        log = pd.DataFrame(columns=log_columns)
        st.warning("File activity_log.csv non trovato o vuoto. Inizializzato un nuovo log.")
    
    if log.empty:
        st.info("Nessuna attività registrata.")
        return

    today = datetime.date.today()
    week_number = today.isocalendar()[1]
    week_start = today - datetime.timedelta(days=today.weekday())
    weekly_log = log[log["timestamp"].dt.date >= week_start]

    summary_data = {}
    for cat in categories:
        cat_name = cat["name"]
        target = cat.get("target_weekly", cat.get("weekly_goal", 100))
        cat_points = weekly_log[weekly_log["category"] == cat_name]["points"].sum()
        perc = (cat_points / target) * 100 if target > 0 else 0
        summary_data[cat_name] = f"{perc:.1f}%"

    el = [f"[{cat_name}](#{cat_name.lower()}): {perc}" for cat_name, perc in summary_data.items()]
    st.subheader(f"{' | '.join(el)}")

    st.write(f"Settimana {week_number}: {week_start.strftime('%Y-%m-%d')} - {today.strftime('%Y-%m-%d')}")
    st.write("---")

    for cat in categories:
        cat_name = cat["name"]
        target = cat.get("target_weekly", cat.get("weekly_goal", 100))
        cat_points = weekly_log[weekly_log["category"] == cat_name]["points"].sum()
        perc = (cat_points / target) * 100 if target > 0 else 0
        
        st.subheader(f"{cat_name}", anchor=cat_name.lower())
        st.metric("Completamento settimana", f"{perc:.1f}%")
        st.write(f"Punti accumulati: {cat_points} / {target}")
        
        cat_log = weekly_log[weekly_log["category"] == cat_name]
        if not cat_log.empty:
            st.table(cat_log[["timestamp", "label", "points"]].sort_values("timestamp", ascending=False).assign(timestamp=lambda df: df.timestamp.dt.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            st.info("Nessuna attività registrata per questa categoria.")
        st.write("---")
    
    st.subheader("Aggiungi attività manualmente")
    manual_date = st.date_input("Data", today)
    manual_category = st.selectbox("Categoria", [cat["name"] for cat in categories])
    manual_label = st.text_input("Nome attività", key="manual_label_stats")
    manual_points = st.number_input("Punti", min_value=1, value=1, key="manual_points_stats")

    if st.button("Aggiungi manualmente", key="add_manual_stats"):
        if not manual_label.strip():
            st.error("Inserisci un nome attività valido.")
        else:
            manual_timestamp = datetime.datetime.combine(manual_date, datetime.datetime.now().time()).strftime('%Y-%m-%d %H:%M:%S')
            new_activity = {
                "timestamp": manual_timestamp,
                "category": manual_category,
                "label": manual_label,
                "points": manual_points
            }
            log = pd.concat([log, pd.DataFrame([new_activity], columns=log_columns)], ignore_index=True)
            log.to_csv("activity_log.csv", index=False)
            st.success("Attività aggiunta con successo!")
            st.rerun()
    
    show_debug(params)
