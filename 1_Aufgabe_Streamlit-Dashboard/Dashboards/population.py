"""
Modul zur Darstellung der Bevölkerungsentwicklung weltweit und einzelner Länder.
Stellt interaktive Diagramme, Ländervergleiche und Landesdetails dar.
"""

# Bibliotheken importieren
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from countryinfo import CountryInfo

# Hauptfunktion zur Darstellung des Dashboards
def render_population_dashboard(selected_country):
    """Visualisiert Bevölkerungsdaten für ein einzelnes Land oder global."""

    # CSV-Datei einlesen und in Long-Format transformieren
    df = pd.read_csv("Datasets/world_population.csv")
    df_long = pd.melt(
        df,
        id_vars=["Country/Territory", "CCA3"],  # Länderspalten beibehalten
        value_vars=["2010 Population", "2015 Population", "2020 Population", "2022 Population"],  # Jahre extrahieren
        var_name="Year",
        value_name="Population"
    )
    df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)  # Jahreszahl extrahieren
    df_long["Population"] = df_long["Population"].astype(int)  # Bevölkerung in Integer umwandeln

    # Jahr für Standardanzeige setzen
    default_year = 2022
    df_selected = df_long[df_long["Year"] == default_year]
    df_sorted = df_selected.sort_values(by="Population", ascending=False)

    # Länderansicht oder Weltansicht vorbereiten
    if selected_country != "Alle":
        # Daten für ausgewähltes Land
        df_selected = df_selected[df_selected["Country/Territory"] == selected_country]
        df_country_all_years = df_long[df_long["Country/Territory"] == selected_country].sort_values("Year",
                                                                                                     ascending=False)
        unit = "M"  # Millionen
        factor = 1e6
    else:
        # Aggregierte Weltansicht
        df_country_all_years = df_long.groupby("Year")["Population"].sum().reset_index()
        df_country_all_years["Country/Territory"] = "Welt"
        df_country_all_years = df_country_all_years.sort_values("Year", ascending=False)
        unit = "B"  # Milliarden
        factor = 1e9

    # Übersicht über die Entwicklung in Metriken anzeigen
    st.markdown("### 🌐 Bevölkerung im Vergleich")
    df_country_all_years["Population_Unit"] = df_country_all_years["Population"] / factor

    # Anzeige als Metrik-Elemente mit Delta zu Vorjahr
    metric_cols = st.columns(len(df_country_all_years))
    for idx, row in enumerate(df_country_all_years.itertuples()):
        delta = ""
        if idx < len(df_country_all_years) - 1:
            delta_value = row.Population_Unit - df_country_all_years.iloc[idx + 1].Population_Unit
            delta = f"{delta_value:.2f} {unit}"
        metric_cols[idx].metric(
            label=f"{row.Year}",
            value=f"{row.Population_Unit:.2f} {unit}",
            delta=delta
        )

    # --------------------------
    # WELTANSICHT
    # --------------------------
    if selected_country == "Alle":
        col1, col2 = st.columns((1.5, 4.5), gap='large')

        # Tabelle mit allen Ländern & Bevölkerung
        with col1:
            st.markdown(f"### 🏆 Gesamtbevölerung aller Länder im Jahr {default_year}")
            st.dataframe(
                df_sorted[["Country/Territory", "Population"]],
                column_order=("Country/Territory", "Population"),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Country/Territory": st.column_config.TextColumn("Land"),
                    "Population": st.column_config.ProgressColumn(
                        "Bevölkerung",
                        format="%f",
                        min_value=0,
                        max_value=int(df_sorted["Population"].max())
                    )
                },
                height=600
            )

            # Jahresauswahl-Slider
            selected_year = st.slider("Wähle ein Jahr", min_value=2010, max_value=2022, step=5, value=default_year)

        # Weltkarte mit Bevölkerung
        with col2:
            st.markdown("### 🌍 Weltbevölkerung nach Ländern")
            df_all_map = df_long[df_long["Year"] == selected_year].copy()
            df_all_map["log_population"] = np.log10(df_all_map["Population"] + 1)  # log-Skalierung für bessere Anzeige

            fig_map = px.choropleth(
                df_all_map,
                locations="CCA3",
                color="log_population",
                hover_name="Country/Territory",
                color_continuous_scale="Blues",
                range_color=(6, 9.5),
                projection="natural earth",
                title=f"Weltbevölkerung {selected_year}",
                labels={"log_population": "Bevölkerungsgröße"}
            )
            fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0), height=500)
            st.plotly_chart(fig_map, use_container_width=True)

    # --------------------------
    # EINZELLAND-ANSICHT
    # --------------------------
    else:
        st.markdown(f"### 🗺️ Bevölkerung in {selected_country}")
        df_selected["log_population"] = np.log10(df_selected["Population"] + 1)
        col_map, col_flag = st.columns((2, 1), gap="large")

        # Karte mit dem ausgewählten Land
        with col_map:
            fig_map = px.choropleth(
                df_selected,
                locations="CCA3",
                color="log_population",
                hover_name="Country/Territory",
                color_continuous_scale="Blues",
                range_color=(6, 9.5),
                projection="natural earth",
                title=f"{selected_country} ({default_year})",
                labels={"log_population": "Bevölkerungsgröße"}
            )
            fig_map.update_geos(visible=True, showcountries=True, showcoastlines=True, fitbounds="locations")
            fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0), height=500)
            st.plotly_chart(fig_map, use_container_width=True)

        # Länderflagge anzeigen
        with col_flag:
            try:
                response = requests.get(f"https://restcountries.com/v3.1/name/{selected_country}")
                country_data = response.json()[0]
                flag_url = country_data.get("flags", {}).get("svg") or country_data.get("flags", {}).get("png")
                if flag_url:
                    st.markdown(
                        f"""
                            <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; height: 450px;'>
                                <img src="{flag_url}" width="650">
                                <p style='color: white; margin-top: 0.5rem;'></p>
                            </div>
                            """,
                        unsafe_allow_html=True
                    )
            except:
                st.warning("Keine Flagge verfügbar.")

        # Zusatzinfos zum Land anzeigen
        with st.expander("About", expanded=False):
            try:
                ci = CountryInfo(selected_country)
                st.markdown(f"""

*{selected_country}*

- 🏩 **Hauptstadt**: {ci.capital()}
- 📊 **Fläche**: {ci.area():,} km²
- 🛍 **Nachbarländer**: {", ".join(ci.borders())}
- 💱 **Währungen**: {", ".join(ci.currencies())}
- 🎤 **Sprachen**: {", ".join(ci.languages())}
- 🌍 **Region**: {ci.region()}
- 🕒 **Zeitzonen**: {", ".join(ci.timezones())}
                """)
            except:
                st.error("ℹ️ Keine Zusatzinformationen verfügbar.")
