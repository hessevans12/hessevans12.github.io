import folium
import json

# Replace 'your_geojson_file.geojson' with the path to your GeoJSON file
your_geojson_file = 'your_geojson_file.geojson'

# Create a map object centered at a specific latitude and longitude
# You can adjust the latitude and longitude to focus on your area of interest
map_center = [38.5780, -122.9888]  # Sonoma County, CA
map_object = folium.Map(location=map_center, zoom_start=12, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community')


# Load the GeoJSON file and add it to the map with feature names
with open('map.geojson') as f:
    geojson_data = json.load(f)

# Extract available field names from the first feature in the GeoJSON file
available_fields = list(geojson_data.get('features', [{}])[0].get('properties', {}).keys())

folium.GeoJson(
    geojson_data,
    name='geojson',
    tooltip=folium.GeoJsonTooltip(fields=available_fields, aliases=[f'{field}:' for field in available_fields]),
).add_to(map_object)

# Add layer control to toggle the GeoJSON layer
folium.LayerControl().add_to(map_object)

# Save the map to an HTML file
map_object.save('map_with_geojson.html')

print("Map has been saved as 'map_with_geojson.html'")