import folium as fol
import pandas as pd
import branca.colormap as cm

# Capture the data. Change location here. Currently filters for Canada and returns a dataframe
def AQI_data_extract():
    # Read locations and AQI data
    locations = pd.read_csv('locations.csv')
    AQI_datum = pd.read_csv('AQI data.csv')

    # Merge data on lat and lon
    datum_filter = AQI_datum.merge(right=locations, on=['lat', 'lon'], how='left')

    # Filter for Canada
    datum_filter = pd.DataFrame(datum_filter[datum_filter['Country'] == 'Canada'])

    # Drop duplicates and keep the last entry for each lat-lon pair
    datum_filter = datum_filter.drop_duplicates(keep='last', subset=['lat', 'lon'])

    return datum_filter

# Initialize the folium map
def Start_map():
    AQI_data_filtered = AQI_data_extract()

    # Ensure that the folium map is correctly initialized
    map_init = fol.Map(location=(49.2414, -123.1111), zoom_start=10, min_zoom=9, tiles="cartodb positron")

    return map_init, AQI_data_filtered

# Add AQI markers to the map
def AQI_Markers(map_init, AQI_data_filtered):
    # Define colormap based on AQI levels
    cmap = cm.StepColormap(["lightblue", "lightgreen", "green", "orange", "red"], vmin=0, vmax=5)

    # Add colormap to the map
    cmap.add_to(map_init)

    # Define a dictionary to map AQI range to valid Folium colors
    aqi_to_color = {
        0: 'lightblue',   # Light Blue for low AQI
        1: 'lightgreen',  # Light Green for moderate AQI
        2: 'green',       # Green for good AQI
        3: 'orange',      # Orange for moderate-high AQI
        4: 'red'          # Red for very poor AQI
    }

    # Generate markers
    for i in AQI_data_filtered.itertuples():
        # Get AQI value (assuming it is in column index 3, change if necessary)
        aqi_value = i[3]

        # Map AQI value to a valid Folium color
        if aqi_value < 1:
            marker_color = aqi_to_color[0]
        elif aqi_value < 2:
            marker_color = aqi_to_color[1]
        elif aqi_value < 3:
            marker_color = aqi_to_color[2]
        elif aqi_value < 4:
            marker_color = aqi_to_color[3]
        else:
            marker_color = aqi_to_color[4]

        # Add marker to map with corresponding color
        fol.Marker(
            location=[i[1], i[2]],  # lat, lon
            icon=fol.Icon(icon="cloud", color=marker_color),  # Use a valid color
            popup=f"AQI: {aqi_value}"
        ).add_to(map_init)
    return map_init
# Save the map to an HTML file
def save_Map(map_init):
    map_init.save("map_view.html")
    return map_init
# Main execution
if __name__ == "__main__":
    map_init, AQI_data_filtered = Start_map()  # Get the map and filtered data
    AQI_Markers(map_init, AQI_data_filtered)  # Pass both map_init and AQI data to the marker function
    save_Map(map_init)  # Save the map to an HTML file

print(AQI_data_extract())