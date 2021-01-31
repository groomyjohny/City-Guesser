from cities import cities
staticApiAddr = "https://static-maps.yandex.ru/1.x/?"
games = {}

from flask import Flask, render_template, redirect, request, abort
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

@app.route('/slide/<int:slide_number>')
def slide(slide_number):
    clientAddr = request.environ["REMOTE_ADDR"]
    return render_template("slide.html",
    n = slide_number,
    imgPath = games[clientAddr].slidePaths[slide_number],
    totalSlides = len(games[clientAddr].slidePaths),
    hint = "Подсказка: это - один из следующих городов: "+ ', '.join(games[clientAddr].hint),
    hintNot = "Подсказка: это НЕ один из следующих городов: "+ ', '.join(games[clientAddr].hintNot)
    )

@app.route('/reset')
def reset():
    clientAddr = request.environ["REMOTE_ADDR"]
    slidePaths = []
    chosenCity =  random.choice(cities)
    chosenCity = chosenCity
    hint = cities
    hintNot = []
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
    games[clientAddr] = {
        'slidePaths': slidePaths,
        'chosenCity': chosenCity,
        'hint': hint,
        'hintNot': hintNot,
        'cityCoords': cityCoords,
        'hintsUsed': hintsUsed,
    }
    return redirect('/game')

@app.route("/game")
def game():
    return render_template("game.html")

@app.route('/hint/<int:slide_number>')
def hintFunc(slide_number):
    clientAddr = request.environ["REMOTE_ADDR"]
    if len(games[clientAddr].hint) > 2:
        el = random.choice(games[clientAddr].hint)
        games[clientAddr].hintNot.append(el)
        games[clientAddr].hint.remove(el)
        games[clientAddr].hintsUsed += 1
    return redirect(f'/slide/{slide_number}')

@app.route('/answer/<int:slideNum>', methods = ['POST'])
def answer(slideNum):
    clientAddr = request.environ["REMOTE_ADDR"]
    if request.form['cityGuess'] == games[clientAddr].chosenCity:
        games[clientAddr].wonGame = True
        return redirect('/won')
    else:
        return redirect(f'/slide/{slideNum}')

@app.route('/won')
def won():
    clientAddr = request.environ["REMOTE_ADDR"]
    if games[clientAddr].wonGame:
        return render_template("won.html", hintsUsed = games[clientAddr].hintsUsed)
    else:
        return abort(404)

@app.route('/')
def index():
    return render_template('index.html')
    
app.run(port = 8080)