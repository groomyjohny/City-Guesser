from flask import Flask, render_template, redirect, request, abort
from GameInstance import GameInstance
from shared import *

app = Flask(__name__)
@app.route('/slide/<int:slide_number>')
def slide(slide_number):
    clientAddr = request.environ["REMOTE_ADDR"]
    return render_template("slide.html",
        n = slide_number,
        imgPath = games[clientAddr].slidePaths[slide_number],
        totalSlides = len(games[clientAddr].slidePaths),
        hint = games[clientAddr].hint,
        hintNot = games[clientAddr].hintNot
    )

@app.route('/reset')
def reset():
    clientAddr = request.environ["REMOTE_ADDR"]
    games[clientAddr] = GameInstance()
    print("Клиент ",clientAddr, " получил город: ", games[clientAddr].chosenCity)
    return redirect('/game')

@app.route("/game")
def game():
    return render_template("game.html")

@app.route('/hint/<int:slide_number>')
def hintFunc(slide_number):
    clientAddr = request.environ["REMOTE_ADDR"]
    games[clientAddr].getHint()
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

games = {}
app.run(host = '0.0.0.0', port = 8080)