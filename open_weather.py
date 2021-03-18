# -*- coding: utf-8 -*-

import json
import requests
import sys, os
from dotenv import load_dotenv

def getWeather(key):
    city = 'Tokyo'
    key = key
    url = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&lang=ja&cnt=2&q=' + city + '&APPID=' + key

    response = requests.get(url)
    data = response.json()
    jsonText = json.dumps(data, indent=4)
    data = json.loads(response.text)
    return data
