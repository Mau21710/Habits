import pandas as pd
import streamlit as st
import inspect
import os

CONFIG_XLSX = "config.xlsx"

def load_config_from_excel(path=CONFIG_XLSX):
    categories_df = pd.read_excel(path, sheet_name="categories")
    activities_df = pd.read_excel(path, sheet_name="activities")
    params_df = pd.read_excel(path, sheet_name="parameters")
    
    categories = categories_df.to_dict(orient="records")
    activities = activities_df.to_dict(orient="records")
    params = dict(zip(params_df["key"], params_df["value"]))
    
    for cat in categories:
        if "weekly_goal" not in cat and "target_weekly" in cat:
            cat["weekly_goal"] = cat["target_weekly"]
    
    return categories, activities, params

def show_debug(params, filename=None):
    if params.get("debug", False):
        filename = os.path.basename(inspect.stack()[1].filename)
        st.markdown(
            f"<div style='position:fixed;bottom:10px;right:10px;color:gray;font-size:small;'>"
            f"{filename}"
            f"</div>",
            unsafe_allow_html=True
        )
