# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from datetime import datetime
import logging
import time
import string

from games.euroRoulette import EuroRoulette
from games.eurojackpot import EuroJackpot
from games.game import Game
from games.lotto import Lotto
from games.multi import MultiMulti
from games.powerball import PowerBall


def play(length: int, game: Game, gameName: string):
    arr = []
    if gameName == "MonteCarlo":
        print("Monte Carlo")
        start_time = time.time()
        arr = [game.monteCarlo(3000) for _ in range(0, length)]
        print("--- %s minutes ---" % ((time.time() - start_time) / 60))
    elif gameName == "LasVegas":
        print("Las Vegas")
        start_time = time.time()
        arr = [game.lasVegas(4) for _ in range(0, 3)]
        print("--- %s minutes ---" % ((time.time() - start_time)/60))
    mean, var, sd = game.statistics(arr)
    text: string = str(arr) + "\nsrednia: " + str(mean) + "\nwariancja: " + str(
        var) + "\nodchylenie standardowe: " + str(sd)
    print(text)
    game.saveLocally(" ".join([str(i) for i in arr]), game.name)


if __name__ == '__main__':
    logging.info(datetime.now())
    length = 100

    #game: Game = EuroRoulette("EuroRoulette-MonteCarlo", True, 0, 36, True,  1)
    #play(length, game, "MonteCarlo")
    #game.loadLocally('EuroRoulette-MonteCarlo')

    #game: Game = EuroRoulette("EuroRoulette-LasVegas", True, 0, 36, True, 1)
    #play(length, game, "LasVegas")
    #game.save('EuroRoulette-LasVegas')

    #game = Lotto("Lotto-MonteCarlo", True, 1, 49, True, 6)
    #play(length, game, "MonteCarlo")
    #game.save('Lotto-MonteCarlo')

    #game = Lotto("Lotto-LasVegas", True, 1, 49, True, 6)
    #play(length, game, "LasVegas")
    #game.save('Lotto-LasVegas')

    #game = MultiMulti("MultiMulti-MonteCarlo", True, 1, 80, True, 20, 10)
    #play(length, game, "MonteCarlo")
    #game.save('MultiMulti-MonteCarlo')

    game = MultiMulti("MultiMulti-LasVegas", True, 1, 80, True, 20, 10)
    play(length, game, "LasVegas")
    #game.save('MultiMulti-LasVegas')

    game = EuroJackpot("EuroJackpot-MonteCarlo", True, 1, 50, True, 5, 1, 10, 2)
    play(length, game, "MonteCarlo")
    #game.save('EuroJackpot-MonteCarlo')

    game = EuroJackpot("EuroJackpot-LasVegas", True, 1, 50, True, 5, 1, 10, 2)
    play(length, game, "LasVegas")
    #game.save('EuroJackpot-LasVegas')

    game = PowerBall("PowerBall-MonteCarlo", True, 1, 69, True, 5, 1, 26, 1)
    play(length, game, "MonteCarlo")
    #game.save('PowerBall-MonteCarlo')

    game = PowerBall("PowerBall-LasVegas", True, 1, 69, True, 5, 1, 26, 1)
    play(length, game, "LasVegas")
    #game.save('PowerBall-LasVegas')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
