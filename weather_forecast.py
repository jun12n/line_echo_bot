import requests
import datetime
import json
import os

api_key = os.getenv('API_KEY', None)

DAY5_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=ja&appid={key}'


def get_day5_data(location):
    location = get_location(location)
    forecast_dt = []
    url = DAY5_URL.format(city=location, key=api_key)
    response = requests.get(url)
    data = response.json()

    delta = datetime.timedelta(hours=9)
    for i, per_dt in enumerate(data['list']):
        if i == 3:
            break

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
        date_time = date_time.strftime('%m/%d %H:%M')
        sub_dt['Datetime'] = date_time
        forecast_dt.append(sub_dt)
    return forecast_dt


def get_location(location):
    if location == '神戸':
        return 'Kobe'
    elif location == '岡山':
        return 'Okayama'
    elif location == 'New York':
        return 'New York City'
    else:
        return '天気'


def make_template(all_data):
    text_list = []
    for data in all_data:
        emoji = choose_emoji(data)
        text = """{date}
天気は、{weather}{emoji}
降水量は、{volume}mm
温度は、{temperature}℃""".format(date=data['Datetime'], weather=data['Weather'],
                             volume=data['Rain_volume'], emoji=emoji, temperature=data['Temperature'])
        text_list.append(text)
    return text_list


def choose_emoji(data):
    if data['Weather'] == 'Rain':
        emoji = chr(0x1000AA)
    elif data['Weather'] == 'Clouds':
        emoji = chr(0x1000AC)
    else:
        emoji = chr(0x1000A9)
    return emoji
