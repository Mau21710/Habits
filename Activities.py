import streamlit as st
import pandas as pd
import os, datetime
from config_loader import load_config_from_excel, show_debug

def run():
    st.title("📌 Aggiungi Attività")
    
    categories, activities, params = load_config_from_excel()

    # Seleziona categoria
    category_names = [c["name"] for c in categories]
    selected_category = st.selectbox("Categoria", category_names)

    # Filtra attività per categoria
    available_activities = [a for a in activities if a["category"] == selected_category]

    # Tabella attività cliccabili
    st.subheader(f"Attività per {selected_category}")
    for act in available_activities:
        if st.button(f"➕ {act['label']} ({act['points']} punti)"):
            log_entry = {
                "date": datetime.date.today().isoformat(),
                "category": act["category"],
                "label": act["label"],
                "points": act["points"]
            }
            # Salvataggio append su CSV
            df = pd.DataFrame([log_entry])
            try:
                df_existing = pd.read_csv("activity_log.csv")
                df = pd.concat([df_existing, df], ignore_index=True)
            except FileNotFoundError:
                pass
            df.to_csv("activity_log.csv", index=False)
            st.success(f"Aggiunta attività: {act['label']} (+{act['points']} punti)")
    
    show_debug(params)
