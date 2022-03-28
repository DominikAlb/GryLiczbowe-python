import random
import string
import logging

from games.game import Game


class EuroJackpot(Game):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, *args):
        super().__init__(name, debug, min_val, max_val, *args)

    def play(self, numSpins: int, *args) -> float:
        wins: int = 0
        numbers1 = random.sample(range(self.min_val, self.max_val), self.n)
        numbers2 = random.sample(range(self.min_val2, self.max_val2), self.m)
        for x in range(0, numSpins):
            if super().draw(self.min_val, self.max_val, numbers1, len(numbers1)) and \
               super().draw(self.min_val2, self.max_val2, numbers2, len(numbers2)):
                wins = wins + 1
        if self.debug:
            logging.info(
                "Oczekiwany wynik wylosowania w " + self.name + ": " + str(numbers1) + " - " + str(numbers2) + " , to: " + str(
                    100 * wins / numSpins) + "%\n")
            logging.info(
                "liczba wygranych: " + str(wins) + "\n\n")

        return wins/numSpins
