"""
Modul zur Darstellung von Finanzkennzahlen weltweit oder je Land.
Beinhaltet Metriken wie BIP, Inflation, Export und Import.
Erzeugt sowohl Zeitreihen-Visualisierungen als auch Kartenansichten.
"""

# Import von benötigten Bibliotheken
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import requests

# Hauptfunktion zur Anzeige des Finanz-Dashboards
def render_financial_dashboard(selected_country):
    """Rendert das Finanz-Dashboard je nach Länderauswahl."""

    # Auswahl einer Finanzmetrik über Dropdown
    metric = st.selectbox("Wähle eine Finanzmetrik", ["BIP", "Inflation", "Export", "Import"])

    # Laden der Finanzdaten aus CSV-Dateien
    gdp_df = pd.read_csv("Datasets/world_gdp_data.csv", encoding="latin1", sep=";", on_bad_lines="skip")
    infl_df = pd.read_csv("Datasets/global_inflation_data.csv", encoding="latin1", sep=";", on_bad_lines="skip")
    trade_df = pd.read_csv("Datasets/34_years_world_export_import_dataset.csv", encoding="latin1", sep=";", on_bad_lines="skip")

    # Umbenennen fehlerhafter Spaltennamen
    infl_df.rename(columns={"ï»¿country_name": "country_name"}, inplace=True)
    trade_df.rename(columns={"Partner Name": "Country"}, inplace=True)

    # Liste mit zu ignorierenden Regionen (keine Länder)
    excludes = ["World", "Europe", "Eastern Europe", "Asia", "Africa", "America", "Caribbean", "Middle East", "Oceania",
                "income", "Other", "unspecified", "regions", "nes"]

    # --------------------------
    # EINZELLAND-ANSICHT
    # --------------------------
    if selected_country != "Alle":
        st.markdown(f"### 🗺️ Finanzdaten für {selected_country}")

        # Aufteilung in zwei Spalten: Karte + Flagge
        col_map, col_flag = st.columns((2, 1), gap="large")

        # Anzeige der Karte mit hervorgehobenem Land
        with col_map:
            try:
                df_map = pd.read_csv("Datasets/world_population.csv")
                cca3 = df_map[df_map["Country/Territory"] == selected_country]["CCA3"].values[0]

                fig_map = px.choropleth(
                    pd.DataFrame({"Country": [selected_country], "CCA3": [cca3], "Dummy": [1]}),
                    locations="CCA3",
                    color="Dummy",
                    hover_name="Country",
                    color_continuous_scale="Blues",
                    range_color=(0, 1),
                    projection="natural earth",
                    title=f"{selected_country}",
                    labels={"Dummy": ""}
                )
                fig_map.update_geos(showcountries=True, showcoastlines=True, fitbounds="locations")
                fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0), height=500)
                st.plotly_chart(fig_map, use_container_width=True)
            except:
                st.warning("Landkarte konnte nicht geladen werden.")

        # Anzeige der Länderflagge aus REST-API
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

        # --------------------------
        # Zeitreihen-Charts (2x2)
        # --------------------------
        st.markdown("### 📊 Finanzmetriken im Zeitverlauf")

        col1, col2 = st.columns(2)

        # BIP-Entwicklung über die Jahre
        with col1:
            st.markdown("#### 💸 Jährliches BIP-Wachstum (prozentuale Veränderung)")
            try:
                gdp_country = gdp_df[gdp_df["country_name"] == selected_country].melt(id_vars="country_name",
                                                                                      var_name="Year", value_name="BIP")
                gdp_country["Year"] = pd.to_numeric(gdp_country["Year"], errors="coerce")
                gdp_country["BIP"] = pd.to_numeric(gdp_country["BIP"], errors="coerce")
                gdp_country = gdp_country.dropna()
                fig_gdp = px.line(gdp_country, x="Year", y="BIP", title="", markers=True)
                fig_gdp.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=400,
                    xaxis_title="Jahr",
                    yaxis_title="BIP-Wachstum (%)"
                )
                st.plotly_chart(fig_gdp, use_container_width=True, config={"displayModeBar": False})
            except:
                st.info("Keine BIP-Daten verfügbar.")

        # Inflationsentwicklung
        with col2:
            st.markdown("#### 📈 Inflation (in %)")
            try:
                infl_country = infl_df[infl_df["country_name"] == selected_country].melt(id_vars="country_name",
                                                                                         var_name="Year",
                                                                                         value_name="Inflation")
                infl_country["Year"] = pd.to_numeric(infl_country["Year"], errors="coerce")
                infl_country["Inflation"] = pd.to_numeric(infl_country["Inflation"], errors="coerce")
                infl_country = infl_country.dropna()
                fig_infl = px.line(infl_country, x="Year", y="Inflation", title="", markers=True)
                fig_infl.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=400,
                    xaxis_title="Jahr",
                    yaxis_title="Inflation (%)"
                )
                st.plotly_chart(fig_infl, use_container_width=True, config={"displayModeBar": False})
            except:
                st.info("Keine Inflationsdaten verfügbar.")

        col3, col4 = st.columns(2)

        # Exportentwicklung
        with col3:
            st.markdown("#### 📦 Exporte (in Tausend USD)")
            try:
                export_country = trade_df[trade_df["Country"] == selected_country][
                    ["Year", "Export (US$ Thousand)"]].copy()
                export_country["Export (US$ Thousand)"] = pd.to_numeric(export_country["Export (US$ Thousand)"],
                                                                        errors="coerce")
                export_country = export_country.dropna()
                fig_export = px.line(export_country, x="Year", y="Export (US$ Thousand)", title="", markers=True)
                fig_export.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=400,
                    xaxis_title="Jahr",
                    yaxis_title="Exporte (Tsd. USD)"
                )
                st.plotly_chart(fig_export, use_container_width=True, config={"displayModeBar": False})
            except:
                st.info("Keine Exportdaten verfügbar.")

        # Importentwicklung
        with col4:
            st.markdown("#### 📥 Importe (in Tausend USD)")
            try:
                import_country = trade_df[trade_df["Country"] == selected_country][
                    ["Year", "Import (US$ Thousand)"]].copy()
                import_country["Import (US$ Thousand)"] = pd.to_numeric(import_country["Import (US$ Thousand)"],
                                                                        errors="coerce")
                import_country = import_country.dropna()
                fig_import = px.line(import_country, x="Year", y="Import (US$ Thousand)", title="", markers=True)
                fig_import.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=400,
                    xaxis_title="Jahr",
                    yaxis_title="Importe (Tsd. USD)"
                )
                st.plotly_chart(fig_import, use_container_width=True, config={"displayModeBar": False})
            except:
                st.info("Keine Importdaten verfügbar.")

    # --------------------------
    # GLOBAL-VIEW
    # --------------------------
    else:
        # Auswahl des Jahres und Zusammenstellung der globalen Daten
        if metric == "BIP":
            years = [col for col in gdp_df.columns if col.isdigit()]
            year = st.slider("Wähle Jahr", min_value=int(min(years)), max_value=int(max(years)), value=2022)
            df = gdp_df[["country_name", str(year)]].copy()
            df.columns = ["Country", "Value"]
        elif metric == "Inflation":
            years = [col for col in infl_df.columns if col.isdigit()]
            year = st.slider("Wähle Jahr", min_value=int(min(years)), max_value=int(max(years)), value=2022)
            df = infl_df[["country_name", str(year)]].copy()
            df.columns = ["Country", "Value"]
        elif metric == "Export":
            years = sorted(trade_df["Year"].dropna().unique())
            year = st.slider("Wähle Jahr", min_value=int(min(years)), max_value=int(max(years)), value=2021)
            df = trade_df[trade_df["Year"] == year][["Country", "Export (US$ Thousand)"]].copy()
            df.columns = ["Country", "Value"]
        elif metric == "Import":
            years = sorted(trade_df["Year"].dropna().unique())
            year = st.slider("Wähle Jahr", min_value=int(min(years)), max_value=int(max(years)), value=2021)
            df = trade_df[trade_df["Year"] == year][["Country", "Import (US$ Thousand)"]].copy()
            df.columns = ["Country", "Value"]

        # Datenbereinigung und Transformation
        df["Country"] = df["Country"].astype(str).str.strip()
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        df = df.dropna(subset=["Value"])
        df = df[~df["Country"].str.contains('|'.join(excludes), case=False)]

        # Skalierung für Darstellung mit log-ähnlicher Transformation
        def symlog(x, lin_thresh=1):
            return np.sign(x) * np.log10(np.abs(x) + lin_thresh)

        df["Color"] = symlog(df["Value"])

        # Aufteilung in zwei Spalten: Tabelle und Karte
        col1, col2 = st.columns((1.5, 4.5), gap="large")

        # Anzeige der Top-Werte als Liste mit Fortschrittsbalken
        with col1:
            st.markdown(f"### 💰 {metric} aller Länder im Jahr {year}")
            df_display = df.sort_values("Value", ascending=False)
            st.dataframe(
                df_display[["Country", "Value"]],
                use_container_width=True,
                hide_index=True,
                height=600,
                column_config={
                    "Country": st.column_config.TextColumn("Land"),
                    "Value": st.column_config.ProgressColumn(
                        metric,
                        format="%f",
                        min_value=float(df["Value"].min()),
                        max_value=float(df["Value"].max())
                    )
                }
            )

        # Darstellung der Weltkarte mit Choroplethen
        with col2:
            st.markdown(f"### 🌍 {metric} nach Ländern im Jahr {year}")
            fig = px.choropleth(
                df,
                locations="Country",
                locationmode="country names",
                color="Color",
                hover_name="Country",
                color_continuous_scale="Blues",
                labels={"Color": f"{metric}"},
                title=f"{metric} im Jahr {year}",
                projection="natural earth",
                height=500
            )

            fig.update_geos(
                showcountries=True,
                showcoastlines=True,
                showland=True,
                fitbounds="locations"
            )

            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=0, r=0, t=30, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)

        # Heatmap: Entwicklung der Metrik bei Top 6 Ländern über Jahre
        st.markdown(f"### 📈 Zeitverlauf: {metric} der Top 6 Länder")

        if metric in ["BIP", "Inflation"]:
            df_heat = gdp_df if metric == "BIP" else infl_df
            df_heat = df_heat.drop(columns=["indicator_name"], errors='ignore')
            selected_years = [str(y) for y in range(2000, 2025, 4)]
            df_heat = df_heat[["country_name"] + selected_years]
            df_heat = df_heat[~df_heat["country_name"].str.contains('|'.join(excludes), case=False)]
            df_melt = df_heat.melt(id_vars="country_name", var_name="Year", value_name="Value")
        else:
            metric_col = "Export (US$ Thousand)" if metric == "Export" else "Import (US$ Thousand)"
            df_heat = trade_df.rename(columns={metric_col: "Value", "Country": "country_name"})
            df_heat = df_heat[~df_heat["country_name"].str.contains('|'.join(excludes), case=False)]
            df_heat = df_heat[df_heat["Year"].isin([2000, 2004, 2008, 2012, 2016, 2020])]
            df_melt = df_heat[["country_name", "Year", "Value"]]

        df_melt["Year"] = pd.to_numeric(df_melt["Year"], errors="coerce")
        df_melt["Value"] = pd.to_numeric(df_melt["Value"], errors="coerce")
        df_melt = df_melt.dropna()

        top6 = df_melt.groupby("country_name")["Value"].mean().nlargest(6).index.tolist()
        df_top = df_melt[df_melt["country_name"].isin(top6)]

        heatmap = alt.Chart(df_top).mark_rect().encode(
            y=alt.Y("Year:O", axis=alt.Axis(title="Jahr", titleFontSize=14, labelAngle=0)),
            x=alt.X("country_name:O", axis=alt.Axis(title="Land", labelAngle=-30)),
            color=alt.Color("Value:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["country_name", "Year", "Value"]
        ).properties(
            width=700,
            height=300,
            title=f"{metric} Zeitverlauf – Top 6 Länder"
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )

        st.altair_chart(heatmap, use_container_width=True)
