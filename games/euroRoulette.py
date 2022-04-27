import random
import string
import logging
import statistics as stat
import time

from games.game import Game


class EuroRoulette(Game):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, randomInput: bool, *args):
        super().__init__(name, debug, min_val, max_val, randomInput, *args)

    def monteCarlo(self, numSpins: int) -> float:
        wins: int = 0
        numbers = []
        if not self.randomInput:
            numbers = random.sample(range(self.min_val, self.max_val), self.n)
        for i in range(0, numSpins):
            if self.randomInput:
                numbers = random.sample(range(self.min_val, self.max_val), self.n)
            if super().draw(self.min_val, self.max_val, numbers, self.n):
                wins = wins + 1
            self.games.append(i + 1)
            self.gameResults.append(wins / (i + 1))
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany wynik wylosowania w " + self.name + ": " + str(numbers) + " , to: " + str(100 * wins / numSpins) + "%\n")
            logging.info(
                "liczba wygranych: " + str(wins) + "\n\n")
        return wins/numSpins

    def lasVegas(self, numSpins: int) -> []:
        count: int = 0
        numbers = []
        start_time = time.time()
        self.gameResults, self.games = self.loadTempDataIfExists()
        if not self.randomInput:
            numbers = random.sample(range(self.min_val, self.max_val), self.n)
        for i in range(len(self.games), numSpins):
            while True:
                if (time.time() - start_time) > 870:
                    self.save(str(i) + " " + str(" ".join([str(g) for g in self.gameResults])), self.name, True)
                    exit(0)
                if self.randomInput:
                    numbers = random.sample(range(self.min_val, self.max_val), self.n)
                count += 1
                if super().draw(self.min_val, self.max_val, numbers, len(numbers)):
                    break
            self.games.append(i + 1)
            self.gameResults.append(count)
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany sredni czas wygranej w " + self.name + ": " + str(numbers) + " , to: " + str(stat.mean(self.gameResults)) + "%\n")

        return stat.mean(self.gameResults)
