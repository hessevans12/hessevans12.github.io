import folium
from folium import FeatureGroup
import os
import json

# Initialize a map centered on Sonoma County, CA
m = folium.Map(location=[38.576, -122.945], zoom_start=10, tiles='https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community')


# Directory containing GeoJSON files
geojson_directory = r'C:\Users\hessx\OneDrive\Desktop\WSVineyards'

# Iterate through all files in the directory
for filename in os.listdir(geojson_directory):
    if filename.endswith('.geojson'):
        file_path = os.path.join(geojson_directory, filename)

        # Load the GeoJSON file
        with open(file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)

            # Iterate through features to handle points separately
            for feature in geojson_data['features']:
                geometry_type = feature['geometry']['type']
                properties = feature['properties']

                if geometry_type == 'Point':
                    coords = feature['geometry']['coordinates']
                    popup_content = '<br>'.join([f"<b>{key}</b>: {value}" for key, value in properties.items()])
                    folium.CircleMarker(
                        location=[coords[1], coords[0]],
                        radius=properties.get('marker-size', 5),
                        color=properties.get('marker-color', 'red'),
                        fill=True,
                        fill_color=properties.get('marker-color', 'red'),
                        fill_opacity=properties.get('marker-opacity', 0.8),
                        popup=folium.Popup(html=popup_content, max_width=300)
                    ).add_to(m)
                else:
                    # Add GeoJSON to the map with enhanced styling for non-point features
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

# Add a minimap for better navigation
from folium.plugins import MiniMap

minimap = MiniMap(toggle_display=True)
minimap.add_to(m)

# Add a fullscreen button for better user experience
from folium.plugins import Fullscreen

Fullscreen(position='topright').add_to(m)

m.save('sonoma_county_map4.html')

print("Map has been saved as 'sonoma_county_map4.html'")

