# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:54:46 2023

@author: Ye Jian_cheng
"""
def stampabella(ris_Server):
    import json

    api_response= ris_Server
    #api_response = b'{"request":{"type":"City","query":"Verona, Italy","language":"en","unit":"m"},"location":{"name":"Verona","country":"Italy","region":"Veneto","lat":"45.450","lon":"11.000","timezone_id":"Europe\\/Rome","localtime":"2023-04-26 16:49","localtime_epoch":1682527740,"utc_offset":"2.0"},"current":{"observation_time":"02:49 PM","temperature":19,"weather_code":116,"weather_icons":["https:\\/\\/cdn.worldweatheronline.com\\/images\\/wsymbols01_png_64\\/wsymbol_0002_sunny_intervals.png"],"weather_descriptions":["Partly cloudy"],"wind_speed":7,"wind_degree":180,"wind_dir":"S","pressure":1013,"precip":0.2,"humidity":35,"cloudcover":25,"feelslike":19,"uv_index":4,"visibility":10,"is_day":"yes"}}'
    
    # parse the JSON response
    data = json.loads(api_response)
    
    # create a string with the relevant information
    s = (f"Location: {data['location']['name']}, {data['location']['region']}, {data['location']['country']}\n"
         f"Local time: {data['location']['localtime']}\n"
         f"Temperature: {data['current']['temperature']}°C\n"
         f"Weather description: {data['current']['weather_descriptions'][0]}\n"
         f"Humidity: {data['current']['humidity']}%\n"
         f"precip: {data['current']['precip']}%\n"
         
         f"Wind: {data['current']['wind_speed']} km/h {data['current']['wind_dir']}")
    
    # return the string
    return s


def get_meteo_info(luogo): #METODO MAIN DA CHIAMARE
    import requests
    
    params = {
      'access_key': '85475062472c85d3a0782760f15ad3c9',
      'query': luogo,
      
      
    }
    
    api_result = requests.get('http://api.weatherstack.com/current', params)
    #print(api_result.content)
    
    ris=stampabella(api_result.content)
    #print(ris)
    return ris





#ris=get_meteo_info("verona")
#print(ris)