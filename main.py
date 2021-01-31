from flask import Flask, render_template, redirect, request, abort
from GameInstance import GameInstance
from shared import *
import sqlite3


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

@app.route("/game", methods = ["GET", "POST"])
def game():
    if request.method == "GET":
        return render_template("game.html")
    else:
        clientAddr = request.environ["REMOTE_ADDR"]
        g = games[clientAddr]
        usrName = request.form['username']
        sqlQuery("INSERT INTO results (username, hintsUsed, wrongAnswers, cityName, gameStartTime, gameEndTime, gameDuration, gameVersion) VALUES (?,?,?,?,?,?,?,?)",(usrName, g.hintsUsed, g.wrongGuesses, g.chosenCity, g.gameStartTime, g.gameEndTime, g.gameDuration, GAME_VERSION_STRING)) 
        return redirect('/leaderboard')

@app.route('/hint/<int:slide_number>')
def hintFunc(slide_number):
    clientAddr = request.environ["REMOTE_ADDR"]
    games[clientAddr].getHint()
    return redirect(f'/slide/{slide_number}')

@app.route('/answer/<int:slideNum>', methods = ['POST'])
def answer(slideNum):
    clientAddr = request.environ["REMOTE_ADDR"]
    if games[clientAddr].checkGuess(request.form['cityGuess']):               
        return redirect('/won')
    else:
        return redirect(f'/slide/{slideNum}')

@app.route('/won', methods = ["GET", "POST"])
def won():
    clientAddr = request.environ["REMOTE_ADDR"]
    if request.method == "GET":
        if games[clientAddr].gameWon:
            return render_template("won.html", hintsUsed = games[clientAddr].hintsUsed)
        else:
            return abort(404)
    else:
       pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    data = sqlQuery('SELECT * from results ORDER BY points DESC')
    return render_template('leaderboard.html', data=data)

games = {}

def sqlQuery(query, params = []):
    conn = sqlite3.connect('database.db')
    data = conn.cursor().execute(query, params).fetchall()
    conn.commit()
    conn.close()
    return data

import os
tableCreateQuery = str('''CREATE TABLE IF NOT EXISTS `results` (
  `id` INTEGER PRIMARY KEY,
  `username` varchar(256) DEFAULT NULL,
  `hintsUsed` int(11) DEFAULT NULL,
  `wrongAnswers` int(11) DEFAULT NULL,
  `cityName` varchar(256) DEFAULT NULL,
  `gameStartTime` datetime DEFAULT current_timestamp,
  `gameEndTime` datetime DEFAULT current_timestamp,
  `gameDuration` double,
  `gameVersion` int(11) DEFAULT NULL,
  `points` int(11) GENERATED ALWAYS AS (100000000 / ((`gameDuration`+180) * (`wrongAnswers`+1) * (`hintsUsed` + 3))) VIRTUAL
)''')

path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'database.db')
if not os.path.isfile(path):
    f = open(path, "w")
    f.close()
SQL_CONNECTION = sqlite3.connect('database.db')
SQL_CONNECTION.execute(tableCreateQuery)
SQL_CONNECTION.commit()
SQL_CONNECTION.close()

app.run(host = '0.0.0.0', port = 8333)