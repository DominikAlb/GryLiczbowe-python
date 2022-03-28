# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from datetime import datetime
import logging
import string

from games.euroRoulette import EuroRoulette
from games.eurojackpot import EuroJackpot
from games.game import Game
from games.lotto import Lotto
from games.multi import MultiMulti
from games.powerball import PowerBall


def play(length: int, game: Game):
    arr: list = [game.play(100) for _ in range(0, length)]
    mean, var, sd = game.statistics(arr)
    text: string = str(arr) + "\nsrednia: " + str(mean) + "\nwariancja: " + str(
        var) + "\nodchylenie standardowe: " + str(sd)
    game.save(text, game.name)


if __name__ == '__main__':
    logging.info(datetime.now())
    length = 5

    game: Game = EuroRoulette("EuroRoulette", True, 0, 36)
    game.load('EuroRoulette')

    game = Lotto("Lotto", True, 1, 49, 6)
    game.load('Lotto')

    game = MultiMulti("MultiMulti", True, 1, 80, 20, 10)
    game.load("MultiMulti")

    game = EuroJackpot("EuroJackpot", True, 1, 50, 5, 1, 10, 2)
    game.load("EuroJackpot")

    game = PowerBall("PowerBall", True, 1, 69, 5, 1, 26, 1)
    game.load("PowerBall")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
