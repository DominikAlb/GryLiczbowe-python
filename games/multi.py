import random
import string
import logging
import statistics as stat

from games.game import Game


class MultiMulti(Game):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, *args):
        super().__init__(name, debug, min_val, max_val, *args)

    def monteCarlo(self, numSpins: int) -> float:
        wins: int = 0
        numbers = random.sample(range(self.min_val, self.max_val), self.n)
        for i in range(0, numSpins):
            if super().draw(self.min_val, self.max_val, numbers, self.m):
                wins = wins + 1
            self.games.append(i + 1)
            self.gameResults.append(wins / (i + 1))
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany wynik wylosowania w " + self.name + ": " + str(numbers) + " , to: " + str(100 * wins / numSpins) + "%\n")
            logging.info(
                "liczba wygranych: " + str(wins) + "\n\n")
        return wins / numSpins

    def lasVegas(self, numSpins: int) -> []:
        count: int = 0
        numbers = []
        if not self.randomInput:
            numbers = random.sample(range(self.min_val, self.max_val), self.n)
        for i in range(0, numSpins):
            while True:
                if self.randomInput:
                    numbers = random.sample(range(self.min_val, self.max_val), self.n)
                count += 1
                if super().draw(self.min_val, self.max_val, numbers, self.m):
                    break
            self.games.append(i + 1)
            self.gameResults.append(count)
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany sredni czas wygranej w " + self.name + ": " + str(numbers) + " , to: " + str(
                    stat.mean(self.gameResults)) + "%\n")

        return stat.mean(self.gameResults)
