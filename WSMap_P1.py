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

            # Add GeoJSON to the map
            geojson_layer = folium.GeoJson(
                geojson_data,
                name=filename,
                tooltip=folium.GeoJsonTooltip(fields=['Name'], aliases=['Name'])
            )
            geojson_layer.add_to(m)

# Add a layer control to toggle GeoJSON layers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('sonoma_county_map.html')

print("Map has been saved as 'sonoma_county_map.html'")
