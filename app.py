from flask import Flask, render_template, request
from main import main
import os
from dotenv import load_dotenv
import sqlite3
from databaseFunctions import database_fetch

load_dotenv()
API_key = os.getenv('API_KEY')

def database_setup():
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PastSearches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_location TEXT NOT NULL,
        name_location TEXT NOT NULL,
        state_location TEXT,
        weather_main TEXT,
        weather_description TEXT,
        weather_icon TEXT,
        weather_temperature REAL,
        weather_min_temperature REAL,
        weather_max_temperature REAL,
        weather_feels_like_temperature REAL,
        weather_humidity INTEGER,
        weather_wind_speed REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    
    connection.commit()
    connection.close()

database_setup()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    recent_searches = []
    state = None
    if request.method == 'POST':
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']

        data = main(city, state, country, API_key)

    recent_searches = database_fetch()
    return render_template('index.html', data=data, state=state, recent_searches=recent_searches)

if __name__ == '__main__':
    app.run(debug=True)