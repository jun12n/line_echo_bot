import requests
import datetime
import json
import os

api_key = os.getenv('API_KEY', None)


def get_day5_data():
    global w_txt
    DAY5_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=ja&appid={key}'
    CITY_NAME = 'Kobe'
    forecast_dt = {}

    url = DAY5_URL.format(city=CITY_NAME, key=api_key)
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
        date_time = datetime.datetime.strptime(date_txt, '%Y-%m-%d %H:%M:%S')
        date_time = date_time + delta
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        sub_dt['Datetime'] = date_time

        forecast_dt[i] = sub_dt
    w_txt = """
Temperature is {}
Weather is {}
    """.format(forecast_dt[0]['Temperature'], forecast_dt[0]['Weather'])
    return w_txt
