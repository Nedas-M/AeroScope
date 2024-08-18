import sqlite3

def database_insert(weather_data, state):
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()

    cursor.execute(''' 
    INSERT INTO PastSearches (
        country_location,
        name_location,
        state_location,
        weather_main,
        weather_description,
        weather_icon,
        weather_temperature,
        weather_min_temperature,
        weather_max_temperature,
        weather_feels_like_temperature,
        weather_humidity,
        weather_wind_speed
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        weather_data.country_location,
        weather_data.name_location,
        state,
        weather_data.weather_main,
        weather_data.weather_description,
        weather_data.weather_icon,
        weather_data.weather_temperature,
        weather_data.weather_min_temperature,
        weather_data.weather_max_temperature,
        weather_data.weather_feels_like_temperature,
        weather_data.weather_humidity,
        weather_data.weather_wind_speed

    ))

    connection.commit()
    connection.close()

def database_fetch():
    connection = sqlite3.connect('weather.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute('''
    DELETE FROM PastSearches
    WHERE timestamp NOT IN (
        SELECT timestamp FROM PastSearches
        ORDER BY timestamp DESC
        LIMIT 3)
                   ''')
    
    connection.commit()

    cursor.execute('''
    SELECT * FROM PastSearches
    ORDER BY timestamp DESC
    LIMIT 3 
                   ''')
    
    recent_searches = cursor.fetchall()

    connection.close()

    return recent_searches