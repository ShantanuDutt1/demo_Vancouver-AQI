import streamlit as st
import pandas as pd

def AQI_data4chart():
    # Read locations and AQI data
    locations = pd.read_csv('locations.csv')
    AQI_datum = pd.read_csv('AQI data.csv')

    # Merge data on lat and lon
    datum_filter = AQI_datum.merge(right=locations, on=['lat', 'lon'], how='left')

    # Filter for Canada
    datum_filter = pd.DataFrame(datum_filter[datum_filter['Country'] == 'Canada'])
    return datum_filter
def dataChart():
    lineChart_data=AQI_data4chart()
    metric_options = {
        "Air Quality Index (AQI)": "AQI",
        "Carbon Monoxide (CO)": "co",
        "Ozone (O3)": "o3",
        "Fine Particulate Matter (PM2.5)": "pm2_5",
        "Nitrogen Dioxide (NO2)": "no2"
    }
        
        # Convert 'datetime' to a proper datetime format and set index
    lineChart_data["datetime"] = pd.to_datetime(lineChart_data["datetime"])
    lineChart_data = lineChart_data.set_index("datetime")

    # Streamlit UI
    selected_label = st.selectbox("📊 Select a metric to plot", list(metric_options.keys()))
    metric = metric_options[selected_label]  # Convert selection to actual column name

    # Pivot Data to create a line for each 'location'
    if metric in lineChart_data.columns:
        lineChart_pivot = lineChart_data.pivot(columns="location", values=metric)
        st.line_chart(lineChart_pivot, color=["#FFC300",'#900C3F','#7d3c98','#1abc9c'], use_container_width=True)
    else:
        st.error(f"Metric '{metric}' not found in data.")