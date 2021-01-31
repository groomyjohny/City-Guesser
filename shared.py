from apikey import *
import requests

staticApiAddr = "https://static-maps.yandex.ru/1.x/?"
GAME_VERSION_DIGITS = [ 0, 5, 0, 0]
GAME_VERSION_STRING = ''
for i in GAME_VERSION_DIGITS:
    GAME_VERSION_STRING += str(i).zfill(2)

def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat

def encodeParams(args):
    p = ''
    for k in args:
        p += k + '=' + args[k] + '&'
    return p