#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 08:10:51 2026

@author: h
"""
#%%

        # EDA - Explorative Data Analysis - Hotel Bookings Demand


#%%

import pandas as pd
import os

        # Ladebefehl Datensatz - dieser Befehl sagt Spyder, dass es im Ordner des Skripts suchen soll
        

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

        # Prompt zum Laden des Datensatzes
        
try:
    df = pd.read_csv('hotel_bookings.csv')
    print("✅ Erfolg: Datensatz geladen!")
    print(f"Der Datensatz hat {df.shape[0]} Zeilen und {df.shape[1]} Spalten.")
except FileNotFoundError:
    print("❌ Fehler: Die Datei 'hotel_bookings.csv' wurde nicht gefunden.")
    print("Stelle sicher, dass sie im gleichen Ordner wie dein Skript liegt!")
    
    
        # Zusätzlicher Befehl der die Namen aller Spalten anzeigt
    
print(df.columns)

#%%

        # Datenbereinigung
        # 1. Fehlende Werte ersetzen
        # In 'children' wird auf 0 gesetzt, in 'country' zur Bereinigung auf 'Unknown'
        

nan_replacements = {"children": 0, "country": "Unknown", "agent": 0, "company": 0}
df_clean = df.fillna(nan_replacements)

        # 2. "Null-Gäste"-Einträge entfernen
        # Es gibt Buchungen mit 0 Erwachsenen, Kindern und Babys - die löschen wir.

filter_no_guests = (df_clean['adults'] == 0) & (df_clean['children'] == 0) & (df_clean['babies'] == 0)
df_clean = df_clean[~filter_no_guests]

print(f"Bereinigung abgeschlossen. Verbleibende Zeilen: {df_clean.shape[0]}")

        # Nach Ausführung der Bereinigung verbleiben 119210 Zeilen von 119390 Zeilen


#%%

        # ANALYSE 1: Top 10 Herkunftsländer der Gäste (Tabelle + Weltkarte)

        # 0. Benötigte Bibliotheken für diesen Block importieren
        
        
import pandas as pd
import plotly.express as px
import plotly.io as pio
from tabulate import tabulate

        # Erzwingt das Öffnen der interaktiven Plotly-Grafik im Webbrowser
        
pio.renderers.default = 'browser'


        # TEIL 1: Tabellarische Auswertung (mit Tabulate)
        

        # Daten vorbereiten (Nur Gäste, die nicht storniert haben)
        
arrival_data = df_clean[df_clean['is_canceled'] == 0]
country_data = arrival_data['country'].value_counts().reset_index()
country_data.columns = ['Land_ISO', 'Anzahl_Gäste']

        # Ranking und Prozentanteil berechnen
        
total_arrivals = country_data['Anzahl_Gäste'].sum()
country_data['Prozent'] = (country_data['Anzahl_Gäste'] / total_arrivals * 100).round(2)
country_data['Rang'] = country_data['Anzahl_Gäste'].rank(ascending=False, method='min').astype(int)

        # Top 10 filtern und für die Tabellenausgabe formatieren
        
top_10_countries = country_data.head(10)[['Rang', 'Land_ISO', 'Anzahl_Gäste', 'Prozent']].copy()
top_10_countries['Prozent'] = top_10_countries['Prozent'].map(lambda x: f"{x:.2f} %")

        # Formatierte Ausgabe der Tabelle in der Konsole
        
print("\n--- TABELLE 1: TOP 10 HERKUNFTSLÄNDER (EFFEKTIVE ANREISEN) ---")
print(tabulate(top_10_countries, headers='keys', tablefmt='grid', showindex=False))
print(f"Gesamtzahl der Anreisen über alle Länder: {total_arrivals:,}")


# TEIL 2: Interaktive Visualisierung mit Plotly (Weltkarte)

fig = px.choropleth(country_data,
                    locations="Land_ISO",
                    color="Anzahl_Gäste",
                    hover_name="Land_ISO", 
                    
                    # Hier legen wir fest, was im Fenster beim Drüberfahren erscheint:
                        
                    hover_data={
                        "Land_ISO": False, 
                        "Anzahl_Gäste": True, 
                        "Rang": True, 
                        "Prozent": ":.2f" # Zeigt Prozent mit 2 Dezimalstellen
                    },
                    color_continuous_scale=px.colors.sequential.YlOrRd, # Gelb-Orange-Rot
                    title="<b>Globale Verteilung der Hotelgäste</b><br>Basierend auf tatsächlichen Anreisen",
                    labels={'Anzahl_Gäste': 'Gäste absolut', 'Rang': 'Platzierung', 'Prozent': 'Anteil in %'})

        # Layout-Details der Weltkarte
        
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=70),
    geo=dict(showframe=False, projection_type='equirectangular')
)

fig.show()



#%%

        # Analyse 2: Stornierungsvergleich - City Hotel und Resort Hotel
        
        # Prompt Import
        
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tabulate import tabulate


        # TEIL 1: Tabellarische Auswertung (mit Tabulate)

        # Kreuztabelle für Stornierungen pro Hoteltyp erstellen
        
cancel_table = pd.crosstab(df_clean['hotel'], df_clean['is_canceled'])
cancel_table.columns = ['Eingecheckt (0)', 'Storniert (1)']

        # Stornierungsrate in Prozent berechnen
        
cancel_table['Gesamtbuchungen'] = cancel_table['Eingecheckt (0)'] + cancel_table['Storniert (1)']
cancel_table['Stornierungsrate'] = (cancel_table['Storniert (1)'] / cancel_table['Gesamtbuchungen'] * 100).round(2)

        # Für die schöne Tabellenausgabe kopieren und formatieren
        
cancel_formatted = cancel_table.reset_index()
cancel_formatted['Eingecheckt (0)'] = cancel_formatted['Eingecheckt (0)'].map(lambda x: f"{x:,}")
cancel_formatted['Storniert (1)'] = cancel_formatted['Storniert (1)'].map(lambda x: f"{x:,}")
cancel_formatted['Gesamtbuchungen'] = cancel_formatted['Gesamtbuchungen'].map(lambda x: f"{x:,}")
cancel_formatted['Stornierungsrate'] = cancel_formatted['Stornierungsrate'].map(lambda x: f"{x:.2f} %")

        # Spaltenreihenfolge für die Anzeige anpassen
        
cancel_formatted = cancel_formatted[['hotel', 'Gesamtbuchungen', 'Eingecheckt (0)', 'Storniert (1)', 'Stornierungsrate']]
cancel_formatted.rename(columns={'hotel': 'Hoteltyp', 'Stornierungsrate': 'Stornierungsrate (%)'}, inplace=True)

        # Ausgabe in der Konsole
        
print("\n--- TABELLE 2: STORNIERUNGSVERGLEICH PRO HOTELTYP ---")
print(tabulate(cancel_formatted, headers='keys', tablefmt='grid', showindex=False))


        # TEIL 2: Visualisierung (countplot)

        # Grafik mit hoher Auflösung (dpi=300)
        
plt.figure(figsize=(8, 6), dpi=300)

sns.countplot(data=df_clean, x='hotel', hue='is_canceled', palette='magma')

plt.title('Stornierungen pro Hoteltyp', fontsize=16)
plt.xlabel('Hotel')
plt.ylabel('Anzahl Buchungen')
plt.legend(title='Storniert', labels=['Nein (0)', 'Ja (1)'])

plt.tight_layout()
plt.show()



#%%

        # Analyse 3: Vorlaufzeit und Stornierung
        # Frage: Hat es Einfluss auf die Stornierung, wie lange im Voraus jemand bucht?

        # Prompt Import
        
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tabulate import tabulate


        # TEIL 1: Tabellarische Kennzahlen (mit Tabulate)

        # Statistische Kennzahlen für die Vorlaufzeit berechnen, gruppiert nach Buchungsstatus
        
lead_stats = df_clean.groupby('is_canceled')['lead_time'].agg(
    Mittelwert='mean',
    Median='median',
    Standardabweichung='std',
    Maximum='max'
).reset_index()

        # Bezeichnungen für die Tabelle leserlicher machen
        
lead_stats['is_canceled'] = lead_stats['is_canceled'].map({0: 'Eingecheckt (0)', 1: 'Storniert (1)'})
lead_stats.rename(columns={'is_canceled': 'Buchungsstatus'}, inplace=True)

        # Werte für eine saubere Darstellung formatieren (Einheit "Tage" hinzufügen)
        
lead_stats_formatted = lead_stats.copy()
lead_stats_formatted['Mittelwert'] = lead_stats_formatted['Mittelwert'].map(lambda x: f"{x:.1f} Tage")
lead_stats_formatted['Median'] = lead_stats_formatted['Median'].map(lambda x: f"{x:.0f} Tage")
lead_stats_formatted['Standardabweichung'] = lead_stats_formatted['Standardabweichung'].map(lambda x: f"{x:.1f} Tage")
lead_stats_formatted['Maximum'] = lead_stats_formatted['Maximum'].map(lambda x: f"{x:.0f} Tage")

        # Ausgabe der Tabelle in der Konsole
        
print("\n--- TABELLE 3: STATISTIK VORLAUFZEIT VS. STORNIERUNG ---")
print(tabulate(lead_stats_formatted, headers='keys', tablefmt='grid', showindex=False))


        # TEIL 2: Visualisierung (KDE-Plot)

        # Grafik mit hoher Auflösung (dpi=300)
        
plt.figure(figsize=(10, 6), dpi=300)

        # KDE-Plot (Glattes Dichtediagramm) mit halbtransparenten Flächen
        
sns.kdeplot(
    data=df_clean, 
    x='lead_time', 
    hue='is_canceled', 
    fill=True,              # Flächen ausfüllen
    common_norm=False,      # Unabhängige Skalierung der beiden Kurven für bessere Vergleichbarkeit
    palette='Set1',         # Kontrastreiche Farbpalette
    alpha=0.4,              # Transparenz der Flächen
    linewidth=2
)

        # Titel und Achsen beschriften
        
plt.title('Dichteverteilung: Vorlaufzeit bei stornierten vs. eingecheckten Buchungen', fontsize=14, pad=15)
plt.xlabel('Vorlaufzeit (Tage)', fontsize=12)
plt.ylabel('Dichte (Häufigkeit)', fontsize=12)

        # Achsen-Einschränkung (blendet die extremen Ausreißer über 500 Tage aus für eine bessere Grafik)
        
plt.xlim(0, df_clean['lead_time'].quantile(0.99))

        # Legende anpassen
        
plt.legend(title='Buchungsstatus', labels=['Storniert (1)', 'Eingecheckt (0)'])

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#%%

        # Analyse 4: Preisentwicklung übers Jahr pro Nacht (Average Daily Rate)
        # Chronologische Sortierung der Monate
        
        # 0. Benötigte Imports für diesen Block
        
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

ordered_months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
df_clean['arrival_date_month'] = pd.Categorical(df_clean['arrival_date_month'], categories=ordered_months, ordered=True)


        # TEIL 1: Tabellarische Auswertung (mit Tabulate)

        # Durchschnittliche ADR pro Monat und Hoteltyp berechnen (nur eingecheckte Gäste)
        
        
monthly_revenue = df_clean[df_clean['is_canceled'] == 0].groupby(['arrival_date_month', 'hotel'], observed=True)['adr'].mean().unstack()


        # Werte für eine saubere Darstellung formatieren (Euro-Zeichen hinzufügen)
        
        
monthly_revenue_formatted = monthly_revenue.map(lambda x: f"{x:.2f} €" if pd.notnull(x) else "-").reset_index()
monthly_revenue_formatted.rename(columns={'arrival_date_month': 'Monat'}, inplace=True)

        # Ausgabe in der Konsole
        
        
print("\n--- TABELLE 4: DURCHSCHNITTSPREIS (ADR) PRO MONAT UND HOTELTYP ---")
print(tabulate(monthly_revenue_formatted, headers='keys', tablefmt='grid', showindex=False))


        # TEIL 2: Visualisierung

        # Grafik mit hoher Auflösung (dpi=300)
        
        
plt.figure(figsize=(12, 6), dpi=300)

sns.lineplot(data=df_clean[df_clean['is_canceled'] == 0], 
             x='arrival_date_month', y='adr', hue='hotel', marker='o')

plt.title('Durchschnittspreis pro Nacht (ADR) im Jahresverlauf', fontsize=16)
plt.xlabel('Monat')
plt.ylabel('Preis (Euro/Nacht)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

#%%

        # Analyse 5: Zielgruppen-Segmentierung - Vergleich zwischen den Hotels für Marketing Konzepte
        
        # 1. Funktions Defination um Buchungen zu kategorisieren
        
        


        # Analyse 5: Zielgruppen-Segmentierung - Vergleich zwischen den Hotels für Marketing Konzepte
        
        # 0. Import von tabulate für schönere Tabellenausgabe und plotly für das Diagramm
from tabulate import tabulate
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# Erzwingt das Öffnen der interaktiven Grafik im Webbrowser
pio.renderers.default = 'browser'

        # 1. Funktions Definition um Buchungen zu kategorisieren
        
def define_guest_type(row):
    total_kids = row['children'] + row['babies']
    if row['adults'] == 1 and total_kids == 0:
        return 'Single'
    elif row['adults'] == 2 and total_kids == 0:
        return 'Couple'
    elif row['adults'] > 0 and total_kids > 0:
        return 'Family'
    else:
        return 'Group / Other'

        # 2. Kategorie-Spalte erstellen
        
df_clean['guest_type'] = df_clean.apply(define_guest_type, axis=1)

        # 3. STATISTIK-AUSGABE 1: Verteilung (Anzahl)
        
guest_dist = pd.crosstab(df_clean['hotel'], df_clean['guest_type'], normalize='index') * 100

        # Wertformatierung für Tabelle 5 (mit %-Zeichen)
guest_dist_formatted = guest_dist.map(lambda x: f"{x:.2f} %" if pd.notnull(x) else "-")

print("\n--- TABELLE 5: ZIELGRUPPEN-VERTEILUNG PRO HOTELTYP (in %) ---")
print(tabulate(guest_dist_formatted, headers='keys', tablefmt='grid'))


        # --- 4. ZUSÄTZLICHE INFO: Wer bringt am meisten Geld? (ADR nach Gästetyp) ---
        # Hier berechnen wir den Durchschnittspreis
        
guest_revenue = df_clean[df_clean['is_canceled'] == 0].groupby(['hotel', 'guest_type'], observed=True)['adr'].mean().unstack()

        # Wertformatierung für Tabelle 6 (mit Euro-Symbol)
guest_revenue_formatted = guest_revenue.map(lambda x: f"{x:.2f} €" if pd.notnull(x) else "-")
        
print("\n--- TABELLE 6: DURCHSCHNITTSPREIS (ADR) PRO NACHT NACH GÄSTETYP ---")
print(tabulate(guest_revenue_formatted, headers='keys', tablefmt='grid'))


        # --- 5. VISUALISIERUNG: Interaktives Sunburst-Diagramm (Fehlerfrei berechnet) ---
        
        # Wir filtern auf tatsächliche Anreisen, um verlässliche Umsätze zu zeigen
        
arrival_guests = df_clean[df_clean['is_canceled'] == 0]

        # Daten auf den verschiedenen Ebenen aggregieren
        
total_count = len(arrival_guests)
global_adr_mean = arrival_guests['adr'].mean()

        # Ebene 1: Hotels
        
hotel_data = arrival_guests.groupby('hotel').agg(
    Anzahl_Buchungen=('adr', 'count'),
    Durchschnitts_ADR=('adr', 'mean')
).reset_index()

        # Ebene 2: Hotel + Gästetyp
        
guest_data = arrival_guests.groupby(['hotel', 'guest_type'], observed=True).agg(
    Anzahl_Buchungen=('adr', 'count'),
    Durchschnitts_ADR=('adr', 'mean')
).reset_index()

        # Hierarchische Listen für Plotly vorbereiten
        
ids = ["Gesamt"]
labels = ["Gesamt"]
parents = [""]
values = [total_count]
colors = [global_adr_mean]
texts = [f"Gesamt<br>100%<br>{global_adr_mean:.2f} €"]

        # 1. Hotels (innerer Ring) hinzufügen
        
for _, row in hotel_data.iterrows():
    pct = (row['Anzahl_Buchungen'] / total_count) * 100
    ids.append(row['hotel'])
    labels.append(row['hotel'])
    parents.append("Gesamt")
    values.append(row['Anzahl_Buchungen'])
    colors.append(row['Durchschnitts_ADR'])
    texts.append(f"{row['hotel']}<br>{pct:.1f}%<br>{row['Durchschnitts_ADR']:.2f} €")

        # 2. Gästetypen (äußerer Ring) hinzufügen
        
for _, row in guest_data.iterrows():
    
       # Ermittlung des Gesamtwerts des übergeordneten Hotels für die korrekte Prozentberechnung
    
    hotel_total = hotel_data[hotel_data['hotel'] == row['hotel']]['Anzahl_Buchungen'].values[0]
    pct = (row['Anzahl_Buchungen'] / hotel_total) * 100
    
    ids.append(f"{row['hotel']} - {row['guest_type']}")
    labels.append(row['guest_type'])
    parents.append(row['hotel'])
    values.append(row['Anzahl_Buchungen'])
    colors.append(row['Durchschnitts_ADR'])
    texts.append(f"{row['guest_type']}<br>{pct:.1f}%<br>{row['Durchschnitts_ADR']:.2f} €")

        # Diagramm mit Graph Objects erstellen (erlaubt volle Kontrolle über Farben und Texte)
        
fig_sunburst = go.Figure(go.Sunburst(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    text=texts,
    hoverinfo="text",                    # Nutzt unseren sauberen Text auch beim Hovern
    branchvalues="total",                # Garantiert korrekte Proportionen der Ringe
    marker=dict(
        colors=colors, 
        colorscale='RdYlBu_r', 
        coloraxis="coloraxis"            # Bindung an eine globale Farbskala
    )
))

        # Layout & Farbskala konfigurieren
        
fig_sunburst.update_layout(
    title="<b>Strategische Zielgruppen-Analyse</b><br>Segmentgröße = Buchungen | Farbe = Durchschnittlicher Preis (ADR)",
    coloraxis=dict(
        colorscale='RdYlBu_r', 
        colorbar=dict(title="ADR (Schnitt)")
    ),
    margin=dict(t=80, l=0, r=0, b=0)
)

        # Textdarstellung optimieren
        
fig_sunburst.update_traces(
    textinfo="text", 
    insidetextorientation="horizontal"
)

fig_sunburst.show()