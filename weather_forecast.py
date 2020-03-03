import requests
import datetime

API_KEY = '4b20be5e5cb0d0906e861a0aabd5f104'

# CURRENT_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ja&APPID={key}'


def get_day5_data():
    DAY5_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=ja&appid={key}'
    CITY_NAME = 'Kobe'
    forecast_dt = {}

    url = DAY5_URL.format(city=CITY_NAME, key=API_KEY)
    response = requests.get(url)
    data = response.json()

    delta = datetime.timedelta(hours=9)
    for i, per_dt in enumerate(data['list']):
        sub_dt = {}
        main_dt = per_dt['main']
        temp = main_dt['temp']
        sub_dt['Temperature'] = temp

        weather_dt = per_dt['weather'][0]
        weather = weather_dt['main']
        sub_dt['Weather'] = weather

        if weather == 'Rain':
            rain_vol = per_dt['rain']
            rain_vol = rain_vol['3h']
        else:
            rain_vol = 0
        sub_dt['Rain_volume'] = rain_vol
        date_txt = per_dt['dt_txt']
        date_time = datetime.datetime.fromisoformat(date_txt)
        date_time = date_time + delta
        sub_dt['Datetime'] = date_time

        forecast_dt[i] = sub_dt
    return forecast_dt
