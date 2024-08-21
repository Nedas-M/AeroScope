import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from databaseFunctions import database_insert

load_dotenv()
API_key = os.getenv('API_KEY')

@dataclass 
class currentWeatherData:

    country_location: str
    name_location:str

    weather_main: str
    weather_description: str
    weather_icon: str
    weather_temperature: float
    weather_min_temperature: float
    weather_max_temperature: float
    weather_feels_like_temperature: float
    weather_humidity: int
    weather_wind_speed: float

def get_lat_and_lon(city_name, state_name, country_code, API_key):
    try:
        lat_lon_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}, {state_name}, {country_code}&appid={API_key}")

        if lat_lon_response.status_code == 200:
            lat_lon_response = lat_lon_response.json()
            lat = lat_lon_response[0].get('lat', 'COULD NOT ACQUIRE LATITUDE')
            lon = lat_lon_response[0].get('lon', 'COULD NOT ACQUIRE LONGITUDE')
            print(lat, lon)
            return lat, lon
        
        else:
            print(f'Failed to acquire latitude and longitude for location: {lat_lon_response.status_code}')
            return None, None
        
    except Exception as e:
        print(f'Error occcured: {e}')
        return None, None

def get_weather(lat, lon, API_key):
    if lat is not None and lon is not None:
        try:
            weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric")
            if weather_response.status_code == 200:
                weather_response = weather_response.json()

                data = currentWeatherData(

                weather_main = weather_response.get('weather')[0].get('main'),
                weather_description = weather_response.get('weather')[0].get('description'),
                weather_icon = weather_response.get('weather')[0].get('icon'),
                weather_temperature = round(weather_response.get('main').get('temp'), 1),
                weather_min_temperature = round(weather_response.get('main').get('temp_min'), 1),
                weather_max_temperature = round(weather_response.get('main').get('temp_max'), 1),
                weather_feels_like_temperature = round(weather_response.get('main').get('feels_like'), 1),
                weather_humidity = weather_response.get('main').get('humidity'),
                weather_wind_speed = weather_response.get('wind').get('speed'),
                country_location = weather_response.get('sys').get('country'),
                name_location = weather_response.get('name'),

                )
                print("------------------------\n  weather_response received \n", weather_response, "\n------------------------")
                return data

            else:
                print(f'No data found for weather: {weather_response.status_code}')

        except Exception as e:
            print(f'Error occurred: {e}')

def main(city_name, state_name, country_code, API_key):
    lat, lon = get_lat_and_lon(city_name, state_name, country_code, API_key)
    weather_data = get_weather(lat, lon, API_key)

    if weather_data:
        print("------------------------\n  if weather_data passed \n------------------------")
        database_insert(weather_data, state_name)

    return weather_data
