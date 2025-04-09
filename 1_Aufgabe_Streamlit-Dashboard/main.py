# --------------------------------------------------
# Imports
# --------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import requests
from countryinfo import CountryInfo

# --------------------------------------------------
# Seiteneinstellungen und Custom-Style
# --------------------------------------------------
st.set_page_config(
    page_title="World Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")

st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
}
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------
def load_csv(filepath, **kwargs):
    return pd.read_csv(filepath, encoding="latin1", sep=";", on_bad_lines="skip", **kwargs)

def clean_country_column(df, original="Partner Name", new="Country"):
    if original in df.columns:
        df.rename(columns={original: new}, inplace=True)
    return df

def get_country_flag(selected_country):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{selected_country}")
        country_data = response.json()[0]
        return country_data.get("flags", {}).get("svg") or country_data.get("flags", {}).get("png")
    except:
        return None

# --------------------------------------------------
# Sidebar-Auswahl
# --------------------------------------------------
with st.sidebar:
    st.title(":earth_africa: Global Dashboard")
    data_mode = st.radio("Anzeigemodus", ["Population", "Financial"])

    if data_mode == "Population":
        population_df = pd.read_csv("Datasets/world_population.csv")
        countries = sorted(population_df["Country/Territory"].unique())
        selected_country = st.selectbox("Wähle ein Land", ["Alle"] + countries, key="pop_country")
    else:
        gdp_df = load_csv("Datasets/world_gdp_data.csv")
        infl_df = load_csv("Datasets/global_inflation_data.csv")
        trade_df = load_csv("Datasets/34_years_world_export_import_dataset.csv")
        infl_df.rename(columns={"\ufeffcountry_name": "country_name"}, inplace=True)
        trade_df = clean_country_column(trade_df)
        countries = sorted(set(gdp_df["country_name"]) | set(infl_df["country_name"]) | set(trade_df["Country"]))
        selected_country = st.selectbox("Wähle ein Land", ["Alle"] + sorted(countries), key="fin_country")

# --------------------------------------------------
# Modularisierte Dashboards
# --------------------------------------------------
from Dashboards.population import render_population_dashboard
from Dashboards.financial import render_financial_dashboard

# --------------------------------------------------
# Dashboard-Renderer
# --------------------------------------------------
if data_mode == "Population":
    render_population_dashboard(selected_country)
else:
    render_financial_dashboard(selected_country)