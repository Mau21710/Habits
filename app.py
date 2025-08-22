from History import run_history_page
import streamlit as st
from config_loader import load_config_from_excel
from CategoryPage import run_category_page
from Statistics import run_statistics_page
import os

categories, activities, params = load_config_from_excel()
page_names = ["Statistiche"] + [c["name"] for c in categories] + ["Storico"]
selected_page = st.sidebar.radio("Menu", page_names)
if params.get("debug", False):
    filename = os.path.basename(__file__)
    st.sidebar.markdown(
        f"<div style='position:fixed;bottom:10px;left:10px;color:gray;font-size:small;'>{filename}</div>",
        unsafe_allow_html=True
    )

# --- Esecuzione della pagina selezionata ---
if selected_page == "Statistiche":
    run_statistics_page(categories, activities, params)
elif selected_page == "Storico":
    run_history_page(categories, activities, params)
else:
    category = next(c for c in categories if c["name"] == selected_page)
    run_category_page(category, [a for a in activities if a["category"] == category["name"]], params)
