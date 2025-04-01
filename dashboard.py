import streamlit as st
import pandas as pd
import folium as fol
from PIL import Image
import AQI_data_compiler as AQI
import map_Van as Map
import streamlit.components.v1 as components  # To embed HTML
import time
import Chart as Chart


# Setup page - Description on top. Three compartments: Data readings, map with current readings, projected forecast.
st.set_page_config(layout="wide")
st.sidebar.image(Image.open("1_Transparent_Image.png"), width=50)
st.sidebar.title("Air Quality Monitoring")
st.sidebar.subheader("Vancouver, BC")
st.sidebar.write("Data dashboard can be constructed to harness real-time data and provide users with key metrics.")
st.sidebar.write("This dashboard is a demonstration of that. It provides real-time air quality data for four selected areas in and around Vancouver, BC.")
st.sidebar.write("The data is sourced from OpenWeather API and can be refreshed every 10 minutes, and builds an inventory of data over time, whenever it is used.") 



def make_map():
    map_init, AQI_data_filtered = Map.Start_map()
    map_init = Map.AQI_Markers(map_init, AQI_data_filtered)  # Add AQI markers
    map_html = map_init._repr_html_()  # Convert the Folium map to HTML
    components.html(map_html, height=400, width=500)  # You can adjust the height and width as needed
def compile_locations():
    AQI.AQI_loc_compiler()
    AQI.AQI_data2csv_compiler()
def table():
    filtered_vals=Map.AQI_data_extract()
    clean_vals=filtered_vals.reset_index(drop=True)
    clean_vals=clean_vals.drop(columns=['lat', 'lon','Country','co'])
    col_order=['location','AQI','pm2_5','o3','no2']
    clean_vals=clean_vals[col_order]
    clean_vals=clean_vals.rename(columns={"AQI": "AQI Score", "location":"City",
                                          "o3":"Ozone (ug/cu.m)","pm2_5":"PM 2.5 (ug/cu.m)",
                                          "no2":"Nitrogen Dioxide (ug/cu.m)"})
    
    st.dataframe(clean_vals, hide_index=True)
    return clean_vals

with st.container(border=True):
    st.write("This dashboard monitors real-time data and plots it as a map and a detailed table. Historical data is displayed as a chart. New data can be refreshed every 15 minutes.")
    #data refersh button on 10 min cooldown
    current_time = time.time()
    button_disabled = current_time < st.session_state.button_disabled_until if 'button_disabled_until' in st.session_state else False
    def dis_click():
        st.session_state.button_disabled_until = time.time() + 900  # 10 minutes cooldown
    if st.button("Refresh Data",on_click=dis_click(),disabled=button_disabled):
        compile_locations()


a,b=st.columns([0.6,0.4])
with a:
    st.subheader("Current AQI across the lower mainland")
    make_map()
with b:
    st.subheader("Current AQI metrics across the lower mainland")
    table()
    st.write("This table shows the current air quality data for selected locations in Vancouver, BC.")


#make a graph
st.subheader("Historical Record of AQI parameters")
Chart.dataChart()
