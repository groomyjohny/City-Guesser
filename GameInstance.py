import random
from cities import cities
from shared import *
import datetime

class GameInstance:
    def __init__(self) -> None:
        self.reset()
        pass

    def reset(self):        
        slidePaths = []
        chosenCity =  random.choice(cities)
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
        
        self.slidePaths = slidePaths
        self.chosenCity = chosenCity
        self.hint = hint
        self.hintNot = hintNot
        self.cityCoords = cityCoords
        self.hintsUsed = hintsUsed
        self.gameWon = False
        self.gameStartTime = datetime.datetime()
        pass

    def getHint(self):
        if len(self.hint) > 2:
            el = random.choice(self.hint)
            self.hintNot.append(el)
            self.hint.remove(el)
            self.hintsUsed += 1
    pass

    def checkGuess(self, guess):
        self.gameWon = guess == self.chosenCity
        if self.gameWon:
            self.gameEndTime = datetime.datetime()
            self.gameDuration = (self.gameEndTime-self.gameStartTime).total_seconds()
        return self.gameWon
    