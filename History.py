import streamlit as st
import pandas as pd
import numpy as np

def run_history_page(categories, activities, params):
    st.title("📜 Storico e Andamenti")

    try:
        log = pd.read_csv("activity_log.csv")
        if log.empty:
            st.info("Il file di log è vuoto. Inizia a registrare attività per vedere lo storico.")
            return
        log['timestamp'] = pd.to_datetime(log['timestamp'])
    except FileNotFoundError:
        st.warning("File activity_log.csv non trovato. Inizia a registrare attività.")
        return

    # Aggiungi colonna per l'anno e la settimana
    log['week'] = log['timestamp'].dt.isocalendar().week
    log['year'] = log['timestamp'].dt.isocalendar().year
    log['year_week'] = log['year'].astype(str) + "-W" + log['week'].astype(str).str.zfill(2)

    # Dizionario degli obiettivi settimanali per categoria
    weekly_goals = {cat['name']: cat.get('weekly_goal', 100) for cat in categories}

    # Calcola i punti totali per ogni settimana e categoria
    weekly_summary = log.groupby(['year_week', 'category'])['points'].sum().reset_index()

    # Calcola la percentuale di completamento
    weekly_summary['goal'] = weekly_summary['category'].map(weekly_goals)
    weekly_summary['percentage'] = (weekly_summary['points'] / weekly_summary['goal']) * 100
    weekly_summary['percentage'] = weekly_summary['percentage'].clip(upper=100) # Non superare il 100%

    # --- Grafico Generale ---
    st.header("Andamento Generale")
    st.write("Media delle percentuali di completamento di tutte le categorie.")

    # Calcola la media delle percentuali per settimana
    general_trend = weekly_summary.groupby('year_week')['percentage'].mean().reset_index()
    general_trend = general_trend.sort_values('year_week')
    general_trend.set_index('year_week', inplace=True)

    if not general_trend.empty:
        st.line_chart(general_trend['percentage'])
    else:
        st.info("Non ci sono ancora abbastanza dati per un andamento generale.")

    st.write("---")

    # --- Grafici per Categoria ---
    st.header("Andamento per Categoria")

    for cat in categories:
        cat_name = cat['name']
        st.subheader(cat_name)
        
        cat_trend = weekly_summary[weekly_summary['category'] == cat_name]
        if not cat_trend.empty:
            cat_trend = cat_trend.sort_values('year_week')
            cat_trend.set_index('year_week', inplace=True)
            st.line_chart(cat_trend['percentage'])
        else:
            st.info(f"Nessuna attività registrata per la categoria '{cat_name}' nello storico.")
