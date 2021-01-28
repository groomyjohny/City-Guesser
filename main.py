cities = [
    'Москва',
    "Санкт-Петербург",
    "Нижний Новгород",
    "Самара",
    "Уфа",
    "Челябинск",
    "Владивосток",
    "Токио",
    "Берлин",
    "Лондон",
    "Вашингтон",
    "Киев",
    "Минск",
    "Стокгольм",
    "Казань",
    "Тверь",
    "Париж",
    "Нью-Йорк",
    "Амстердам",
    "Брюссель",
    "Дюссельдорф",
    "Афины",
    "Марсель",
    "София"
]
staticApiAddr = "https://static-maps.yandex.ru/1.x/?"

hint = []
hintNot = []
chosenCity = ''
cityCoords = []
hintsUsed = 0

from flask import Flask, render_template, redirect, request
from apikey import apikey
import random
import requests

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

app = Flask(__name__)

slidePaths = []
@app.route('/slide/<int:slide_number>')
def slide(slide_number):
    return render_template("slide.html",
    n = slide_number,
    imgPath = slidePaths[slide_number],
    totalSlides = len(slidePaths),
    hint = "Подсказка: это - один из следующих городов: "+ ', '.join(hint),
    hintNot = "Подсказка: это НЕ один из следующих городов: "+ ', '.join(hintNot)
    )

@app.route('/reset')
def reset():
    global hintsUsed, hint, hintNot, chosenCity, cityCoords
    slidePaths.clear()
    chosenCity = random.choice(cities)
    hint = cities
    hintNot.clear()
    cityCoords = fetch_coordinates(apikey,chosenCity)
    cityCoords = [ float(cityCoords[0]), float(cityCoords[1]) ]
    hintsUsed = 0

    slideCount = 10
    for i in range(0,slideCount):
        zoom = int(random.uniform(13,17))
        offset = [ random.uniform(-0.05,0.05), random.uniform(-0.05,0.05) ]
        pos = [ cityCoords[0] + offset[0], cityCoords[1] + offset[1] ]
        mtype = random.choice(['map','sat'])
        args = {
            'l' : mtype,
            'll' : f"{pos[0]},{pos[1]}",
            'z' : str(zoom)
        }
        slidePath = staticApiAddr + encodeParams(args)
        slidePaths.append(slidePath)

    print("Игра сброшена. Новый город:",chosenCity)
    return redirect('/slide/0')

@app.route('/hint/<int:slide_number>')
def hintFunc(slide_number):
    global hintsUsed, hint, hintNot
    if len(hint) > 2:
        el = random.choice(hint)
        hintNot.append(el)
        hint.remove(el)
        hintsUsed += 1
    return redirect(f'/slide/{slide_number}')

@app.route('/answer/<int:slideNum>', methods = ['POST'])
def answer(slideNum):
    if request.form['cityGuess'] == chosenCity:
        return redirect('/won')
    else:
        return redirect(f'/slide/{slideNum}')

@app.route('/won')
def won():
    return render_template("won.html", hintsUsed = hintsUsed)

@app.route('/')
def index():
    return render_template('index.html')
    
app.run(port = 8080)