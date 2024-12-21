import folium
from folium import FeatureGroup
import os
import json

# Initialize a map centered on Sonoma County, CA
m = folium.Map(location=[38.576, -122.945], zoom_start=10,
               tiles='https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
               attr='ESRI World Imagery')

# Directory containing GeoJSON files
geojson_directory = r'C:\Users\hessx\OneDrive\Desktop\WSVineyards'

# Iterate through all files in the directory
for filename in os.listdir(geojson_directory):
    if filename.endswith('.geojson'):
        file_path = os.path.join(geojson_directory, filename)

        # Load the GeoJSON file
        with open(file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)

            # Add GeoJSON to the map with enhanced styling
            geojson_layer = folium.GeoJson(
                geojson_data,
                name=filename,
                tooltip=folium.GeoJsonTooltip(fields=list(geojson_data['features'][0]['properties'].keys()) if geojson_data['features'] else []),
                style_function=lambda x: {
                    'fillColor': x['properties'].get('marker-color', '#228B22') if x['geometry']['type'] != 'Point' else x['properties'].get('marker-color', '#FF0000'),
                    'color': x['properties'].get('marker-color', 'black'),
                    'weight': x['properties'].get('marker-size', 1.5),
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

# Add a search control to easily find features by 'Name'
from folium.plugins import Search

search = Search(
    layer=geojson_layer,
    geom_type='Polygon',
    placeholder='Search Vineyard...',
    search_label='Name',
    collapsed=False
).add_to(m)

# Save the map to an HTML file
m.save('sonoma_county_map2.html')

print("Map has been saved as 'sonoma_county_map2.html'")
