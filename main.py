# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from datetime import datetime
import logging
import time
import string
import statistics as stat

from games.euroRoulette import EuroRoulette
from games.eurojackpot import EuroJackpot
from games.game import Game
from games.lotto import Lotto
from games.multi import MultiMulti
from games.powerball import PowerBall


def play(length: int, game: Game, gameName: string):
    arr = []
    print(game.name)
    if gameName == "MonteCarlo":
        print("Monte Carlo")
        start_time = time.time()
        arr = [game.monteCarlo(3000) for _ in range(0, length)]
        print("--- %s minutes ---" % ((time.time() - start_time) / 60))
        game.show()
        mean, var, sd = game.statistics(arr)
        text: string = str(arr) + "\nsrednia: " + str(mean) + "\nwariancja: " + str(
            var) + "\nodchylenie standardowe: " + str(sd)
        print(text)
        #game.save(" ".join([str(i) for i in game.gameResults]), game.name, False)
    elif gameName == "LasVegas":
        print("Las Vegas")
        start_time = time.time()
        _tuple = [game.lasVegas(50) for _ in range(0, 100)]
        unzip = list(zip(*_tuple))
        arr, timeToWin = unzip[0], unzip[1]
        print("--- %s minutes ---" % ((time.time() - start_time)/60))
        game.show()
        temp = []
        for i in arr:
            #game.save(" ".join([str(j) for j in game.gameResults]), game.name, False)
            temp += i

        mean, var, sd = game.statistics(temp)
        text: string = "srednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)
        print("sredni czas oczekiwania: ", stat.mean(timeToWin), " dni.")
        print(text)

if __name__ == '__main__':
    logging.info(datetime.now())
    length = 1000

    #game: Game = EuroRoulette("EuroRoulette-MonteCarlo", True, 0, 37, True,  1)
    #play(length, game, "MonteCarlo")
    #game.load(False)
    #game.loadLocally(game.name)
    #game.show()

    game: Game = EuroRoulette("EuroRoulette-LasVegas", True, 0, 36, True, 1)
    #play(length, game, "LasVegas")
    game.load(False)
    game.show()

    #game = Lotto("Lotto-MonteCarlo", True, 1, 49, False, 6)
    #play(length, game, "MonteCarlo")
    #game.load(False)
    #game.show()

    game = Lotto("Lotto-LasVegas", True, 1, 49, True, 6)
    #play(length, game, "LasVegas")
    game.load(False)
    game.show()

    #game = MultiMulti("MultiMulti-MonteCarlo", True, 1, 80, False, 20, 10)
    #play(length, game, "MonteCarlo")
    #game.load()
    #game.show()

    game = MultiMulti("MultiMulti-LasVegas", True, 1, 80, True, 20, 10)
    #play(length, game, "LasVegas")
    game.load(False)
    game.show()

    #game = EuroJackpot("EuroJackpot-MonteCarlo", True, 1, 50, False, 5, 1, 10, 2)
    #play(length, game, "MonteCarlo")
    #game.load()
    #game.show()

    game = EuroJackpot("EuroJackpot-LasVegas", True, 1, 50, True, 5, 1, 12, 2)
    #play(length, game, "LasVegas")
    game.load(False)
    game.show()

    #game = PowerBall("PowerBall-MonteCarlo", True, 1, 69, False, 5, 1, 26, 1)
    #play(length, game, "MonteCarlo")
    #game.load()
    #game.show()

    game = PowerBall("PowerBall-LasVegas", True, 1, 69, True, 5, 1, 26, 1)
    #play(length, game, "LasVegas")
    game.load(False)
    game.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/