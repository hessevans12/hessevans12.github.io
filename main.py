import folium
from folium import FeatureGroup
import os
import json


m = folium.Map(location=[38.576, -122.945], zoom_start=10,
               tiles='https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
               attr='ESRI World Imagery')


geojson_directory = r'WSVineyards'


for filename in os.listdir(geojson_directory):
    if filename.endswith('.geojson'):
        file_path = os.path.join(geojson_directory, filename)


        with open(file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)


            for feature in geojson_data['features']:
                geometry_type = feature['geometry']['type']
                properties = feature['properties']

                if geometry_type == 'Point':
                    coords = feature['geometry']['coordinates']
                    folium.CircleMarker(
                        location=[coords[1], coords[0]],
                        radius=properties.get('marker-size', 5),
                        color=properties.get('marker-color', 'red'),
                        fill=True,
                        fill_color=properties.get('marker-color', 'red'),
                        fill_opacity=properties.get('marker-opacity', 0.8),
                        popup=folium.Popup(
                            html='<br>'.join([f"<b>{key}</b>: {value}" for key, value in properties.items()]),
                            max_width=300)
                    ).add_to(m)
                else:

                    geojson_layer = folium.GeoJson(
                        feature,
                        name=filename,
                        tooltip=folium.GeoJsonTooltip(fields=list(properties.keys()) if properties else []),
                        style_function=lambda x: {
                            'fillColor': x['properties'].get('marker-color', '#228B22'),
                            'color': x['properties'].get('marker-color', 'black'),
                            'weight': x['properties'].get('stroke-width', 1.5),
                            'fillOpacity': x['properties'].get('marker-opacity', 0.5)
                        }
                    )
                    geojson_layer.add_to(m)

from folium.plugins import FloatImage

url = (
    "https://i.imgur.com/Cz6uDCr.png"
)

FloatImage(url, bottom=-0, left=3).add_to(m)

from folium.plugins import Fullscreen

Fullscreen(position='topright').add_to(m)

m.save('index.html')

print("Map has been saved as 'index.html'")
