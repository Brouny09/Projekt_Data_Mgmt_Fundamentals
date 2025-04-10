"""
Explorative Datenanalyse (EDA) der im Dashboard verwendeten Datensätze.
Ziel: Erste Einblicke in Struktur, Inhalte und Besonderheiten der Daten gewinnen.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    # 🚀 Einstiegspunkt, falls Skript direkt ausgeführt wird
    print("\n🚀 Starte EDA...\n")

    # Datensätze einlesen
    gdp_df = pd.read_csv("Datasets/world_gdp_data.csv", sep=";", encoding="latin1", on_bad_lines="skip")
    infl_df = pd.read_csv("Datasets/global_inflation_data.csv", sep=";", encoding="latin1", on_bad_lines="skip")
    trade_df = pd.read_csv("Datasets/34_years_world_export_import_dataset.csv", sep=";", encoding="latin1", on_bad_lines="skip")
    pop_df = pd.read_csv("Datasets/world_population.csv")

    # Länder-Namensspalten prüfen
    print("👉 Spaltennamen zur Ländererkennung in den Datensätzen:\n")
    print(f"GDP: {gdp_df.columns[0]}")
    print(f"Inflation: {infl_df.columns[0]} (enthält Encoding-Fehler)")
    print(f"Trade: {trade_df.columns[0]}")
    print(f"Population: {pop_df.columns[0]}")

    print("\nHinweis: Die Ländernamen mussten teilweise vereinheitlicht werden, da sie in den Datensätzen unterschiedlich benannt oder formatiert waren.\n")

    # Spaltenübersicht
    print("📌 Spaltenübersicht pro Datensatz:\n")
    print("GDP:\n", gdp_df.columns.tolist(), "\n")
    print("Inflation:\n", infl_df.columns.tolist(), "\n")
    print("Export/Import:\n", trade_df.columns.tolist(), "\n")
    print("Population:\n", pop_df.columns.tolist(), "\n")

    # Vorschau auf Daten
    print("🔍 Beispiel GDP-Daten:\n", gdp_df.head(), "\n")
    print("🔍 Beispiel Inflationsdaten:\n", infl_df.head(), "\n")
    print("🔍 Beispiel Export/Import-Daten:\n", trade_df.head(), "\n")
    print("🔍 Beispiel Populationsdaten:\n", pop_df.head(), "\n")

    # -----------------------------
    # Visualisierung: Fehlende Werte
    # -----------------------------
    infl_df.rename(columns={"ï»¿country_name": "country_name"}, inplace=True)  # Encoding-Fix

    null_data = {
        "BIP": gdp_df.isnull().sum().sum(),
        "Inflation": infl_df.isnull().sum().sum(),
        "Export / Import": trade_df.isnull().sum().sum(),
        "Population": pop_df.isnull().sum().sum()
    }

    null_df = pd.DataFrame.from_dict(null_data, orient='index', columns=["Missing Values"])

    plt.figure(figsize=(8, 5))
    sns.barplot(x=null_df.index, y="Missing Values", data=null_df, palette="Blues_d")
    plt.title("Anzahl fehlender Werte pro Datensatz")
    plt.ylabel("Fehlende Werte (gesamt)")
    plt.xlabel("Datensatz")
    plt.tight_layout()
    plt.show()

    # -----------------------------
    # 🔧 Datenbereinigung
    # -----------------------------

    # Zeilen mit fehlenden Werten werden entfernt, da Visualisierungen sonst fehlschlagen oder unvollständig sind.
    gdp_df_clean = gdp_df.dropna()
    infl_df_clean = infl_df.dropna()
    trade_df_clean = trade_df.dropna()

    print("✅ Nullwertbereinigung abgeschlossen. Zeilen mit fehlenden Werten wurden entfernt (BIP, Inflation, Handel).\n")

    # ⚠️ Hinweis: Für die spätere Verwendung in Visualisierungen und beim Matching von Ländernamen
    # ist es entscheidend, dass Ländernamen korrekt und konsistent geschrieben sind.
    # Besonders bei Quellendaten treten häufig Variationen auf, z. B.:
    # - "Korea, Rep." vs "South Korea"
    # - "Russian Federation" vs "Russia"
    # - usw.

    # Manuelle Kontrolle ergab, dass Ländernamen nicht einheitlich sind – Mapping wird verwendet, um diese zu vereinheitlichen.
    # Beispielhafte Mapping-Tabelle:

    country_replacements = {
        "Russian Federation": "Russia",
        "Bahamas, The": "Bahamas",
        "Cabo Verde": "Cape Verde",
        "China, People's Republic of": "China",
        "Türkiye": "Turkey",
        "Turkey, Republic of": "Turkey",
        "Iran (Islamic Republic of)": "Iran",
        "Viet Nam": "Vietnam",
        "Korea, Rep.": "South Korea",
        "Egypt, Arab Rep.": "Egypt"
    }

    print("📌 Mapping-Tabelle für Ländername-Korrekturen erstellt.\n")
