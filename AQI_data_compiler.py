#Open Weather API key: ca1ca86f5b4d189a67b068d1be5b16d6
#Current AQI key: http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API key}
#compile AQI data to be pulled.

import requests
import csv
import pandas as pd
from datetime import datetime
import pytz

key="ca1ca86f5b4d189a67b068d1be5b16d6"
query_list=[]
data_list=[]
#CSV Table headings['lat','lon','AQI','co','o3','pm2_5','no2'] #concentration values are in ug/m3
# data interpretation: https://openweathermap.org/api/air-pollution

#compile API calls for each location in locations.csv
def AQI_loc_compiler():

    #Import locations and lat-lon
    with open("locations.csv","r") as read_rows:
        location=csv.reader(read_rows)
        location_list=list(location)
        location_list=location_list[1:] #city, country, lat, long
    
    #compile all the API calls
    for loci in location_list:
        call="http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}".format(loci[2],loci[3],key)
        query_list.append(call)
    return query_list
#Make API calls and add data to the AQI data.csv
def AQI_data2csv_compiler():
    for url in query_list: 
        response=requests.get(url)
        if response.status_code==200:
            post_raw=response.json()
            loc_lat=post_raw.get("coord",{}).get("lat")#location
            loc_lon=post_raw.get("coord",{}).get("lon")#location
            AQI=post_raw.get("list",{})
            AQI=AQI[0]
            AQIvalue=AQI.get("main",{}).get("aqi")#AQI value
            #subset of AQI value components
            AQIco=AQI.get("components",{}).get("co") 
            AQIo3=AQI.get("components",{}).get("o3") 
            AQIno2=AQI.get("components",{}).get("no2") 
            AQIpm2_5=AQI.get("components",{}).get("pm2_5")
            tz = pytz.timezone("America/Vancouver") #vancouver timezone
            current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            #print(current_time)
            post_List=[loc_lat,loc_lon,AQIvalue,AQIco,AQIo3,AQIpm2_5,AQIno2,current_time] 
            data_list.append(post_List)
            with open("AQI data.csv",'a',encoding='UTF8',newline="") as f:
                csv.writer(f).writerow(post_List)
        else:
            print('Error:', response.status_code)

