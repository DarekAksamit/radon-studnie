import pandas as pd
import folium
from folium import CircleMarker, Popup
from folium.plugins import MarkerCluster
import plotly.express as px
from pathlib import Path
import os
from folium import Element
import numpy as np

# Automatyczne określenie folderu skryptu
script_dir = Path(__file__).resolve().parent
csv_path = script_dir / "radon_data.csv"
disclaimer_path = script_dir / "disclaimer_content.html"

# Wczytanie danych z CSV
df = pd.read_csv(csv_path, sep=";")
df = df.dropna(subset=["latitude", "longitude", "radon", "Sample"])
df["radon"] = pd.to_numeric(df["radon"], errors="coerce")



# Funkcja kolorowania markerów według stężenia
def radon_color(val):
    if val <= 10:
        return "green"
    elif val <= 20:
        return "yellow"
    elif val <= 30:
        return "orange"
    else:
        return "red"

# Inicjalizacja mapy
warsaw_coords = [52.2297, 21.0122]
m = folium.Map(location=warsaw_coords, zoom_start=13, control_scale=True)

# Podział na warstwy według źródła próbki
sample_groups = df.groupby("Sample")

for sample_name, group in sample_groups:
    fg = folium.FeatureGroup(name=sample_name)
    cluster = MarkerCluster().add_to(fg)

    for _, row in group.iterrows():
        color = radon_color(row["radon"])
        popup_html = f"""
        <b>ID studni:</b> {row['well_id']}<br>
        <b>Nazwa:</b> {row['well_name']}<br>
        <b>Dzielnica:</b> {row['district']}<br>
        <b>Stężenie radonu:</b> {row['radon']} {row['unit']}<br>
        <b>Niepewność:</b> ±{row['uncertainty']}<br>
        <b>Data:</b> {row['Sample']}<br>
        <b>Komentarz:</b> {row['comment']}
        """
        folium.CircleMarker(
            #location=[row["latitude"], row["longitude"]],  
            # Przesunięcie o losowy, bardzo mały margines (np. ±0.0001)
            location=[row["latitude"] + np.random.uniform(-0.0001, 0.00001), row["longitude"] + np.random.uniform(+0.0001, 0.00001)],           
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=Popup(popup_html, max_width=400),
        ).add_to(cluster)

    fg.add_to(m)

# Dodanie kontroli warstw (w lewym górnym rogu)
folium.LayerControl(collapsed=False, position='topleft').add_to(m)

# Dodanie legendy kolorów
legend_html = """
<div style="
    position: fixed;
    bottom: 100px;
    left: 20px;
    z-index:9999;
    background-color:white;
    padding:10px;
    border:2px solid gray;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
<b>Legenda kolorów (Bq/l):</b><br>
<svg width="20" height="10"><rect width="20" height="10" style="fill:green"/></svg> 0–10<br>
<svg width="20" height="10"><rect width="20" height="10" style="fill:yellow"/></svg> 10–20<br>
<svg width="20" height="10"><rect width="20" height="10" style="fill:orange"/></svg> 20–30<br>
<svg width="20" height="10"><rect width="20" height="10" style="fill:red"/></svg> 30+
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Wykres słupkowy - top 5 stężeń
df_sorted = df.sort_values(by="radon", ascending=False).head(5)
fig = px.bar(
    df_sorted,
    x="well_name",
    y="radon",
    error_y="uncertainty",
    color="district",
    labels={"radon": "Radon (Bq/l)", "well_name": "Studnia"},
    title="Top 5 stężeń radonu",
    height=300
)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
plot_html = fig.to_html(include_plotlyjs='cdn')
plot_div = f"""
<div style="position: fixed;
            bottom: 10px;
            right: 10px;
            width: 400px;
            height: 320px;
            z-index: 9999;
            background-color: white;
            border: 2px solid gray;
            padding: 5px;
            overflow: auto;">
{plot_html}
</div>
"""
m.get_root().html.add_child(folium.Element(plot_div))

# Wczytanie i dodanie disclaimera
with open(disclaimer_path, "r", encoding="utf-8") as f:
    disclaimer_html = f.read()
    disclaimer_element = Element(disclaimer_html)

m.get_root().html.add_child(disclaimer_element)

# Zapis do pliku
output_path = script_dir / "radon_dashboard.html"
m.save(str(output_path))
print("Mapa została zapisana jako 'radon_dashboard.html'")
