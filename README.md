# Projekt_Data_Mgmt_Fundamentals

Dies ist das GitHub-Repository zur Portfolio-Prüfung von **Niklas Bräuninger** und **Jeremia Neuhaus** im Modul *Data Management Fundamentals* bei **Prof. Dr. Giacomo Welsch** an der **DHBW Heilbronn**.

## 🔧 Projektstruktur

Das Repository ist wie folgt aufgebaut:

---

### 📁 `1_Aufgabe_Streamlit-Dashboard`

Hier befinden sich alle relevanten Dateien zur Ausführung des interaktiven Dashboards.

- **`/Dashboards/`**  
  Enthält zwei Python-Module:
  - `financial.py`: Modul zur Visualisierung von Finanzkennzahlen wie BIP, Inflation, Export und Import.
  - `population.py`: Modul zur Darstellung von Bevölkerungsentwicklungen weltweit und pro Land.

- **`EDA.py`**  
  Dieses Skript führt die notwendige **Explorative Datenanalyse (EDA)** der verwendeten Datensätze durch. Hier werden erste Einblicke in die Datenstruktur, Verteilungen und eventuelle Besonderheiten der Daten gewonnen.

- **`/Datasets/`**  
  Hier sind sämtliche zur Visualisierung verwendeten Datensätze abgelegt.  
  Die genutzten Quellen sind:
  - [Weltbevölkerung](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset)
  - [BIP-Daten](https://www.kaggle.com/datasets/sazidthe1/world-gdp-growth)
  - [Export/Import-Daten](https://www.kaggle.com/datasets/muhammadtalhaawan/world-export-and-import-dataset)
  - [Inflation](https://www.kaggle.com/datasets/sazidthe1/global-inflation-data)

- **`.streamlit/config.toml`**  
  Konfigurationsdatei für das Layout und Theme des Dashboards (z. B. Dark Mode, Farben etc.).

- **`main.py`**  
  Startpunkt des Dashboards. Von hier werden die Module dynamisch geladen und die Streamlit-Oberfläche aufgerufen.

---

### 📁 `2_Aufgabe_Gestaltungsentwurf`

In diesem Ordner befinden sich alle relevanten Dateien zum **Systementwurf** der Anwendung.

- Der **Systementwurf selbst** ist enthalten.
- Ebenso die **Ausarbeitung** mit Erläuterungen zu Architektur, Datenflüssen und technischen Entscheidungen.

---

### 👥 Arbeitsaufteilung

Die Arbeitsaufteilung in der Gruppe war folgendermaßen:

- **Aufgabe Dashboard** – Niklas: 70 % / Jeremia: 30 %  
- **Aufgabe Systementwurf** – Niklas: 30 % / Jeremia: 70 %
