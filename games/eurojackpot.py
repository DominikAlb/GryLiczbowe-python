import random
import string
import logging
import statistics as stat

from games.game import Game


class EuroJackpot(Game):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, randomInput: bool, *args):
        super().__init__(name, debug, min_val, max_val, randomInput, *args)

    def monteCarlo(self, numSpins: int) -> float:
        wins: int = 0
        numbers1 = []
        numbers2 = []
        if not self.randomInput:
            numbers1 = random.sample(range(self.min_val, self.max_val), self.n)
            numbers2 = random.sample(range(self.min_val2, self.max_val2), self.m)
        for i in range(0, numSpins):
            if self.randomInput:
                numbers1 = random.sample(range(self.min_val, self.max_val), self.n)
                numbers2 = random.sample(range(self.min_val2, self.max_val2), self.m)
            if super().draw(self.min_val, self.max_val, numbers1, len(numbers1)) and \
               super().draw(self.min_val2, self.max_val2, numbers2, len(numbers2)):
                wins = wins + 1
            self.games.append(i + 1)
            self.gameResults.append(wins / (i + 1))
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany wynik wylosowania w " + self.name + ": " + str(numbers1) + " - " + str(numbers2) + " , to: " + str(
                    100 * wins / numSpins) + "%\n")
            logging.info(
                "liczba wygranych: " + str(wins) + "\n\n")

        return wins/numSpins

    def lasVegas(self, numSpins: int) -> []:
        numbers1 = []
        numbers2 = []
        if not self.randomInput:
            numbers1 = random.sample(range(self.min_val, self.max_val), self.n)
            numbers2 = random.sample(range(self.min_val2, self.max_val2), self.m)
        count: int = 0
        for i in range(0, numSpins):
            while True:
                if self.randomInput:
                    numbers1 = random.sample(range(self.min_val, self.max_val), self.n)
                    numbers2 = random.sample(range(self.min_val2, self.max_val2), self.m)
                #print("nu1 " + str(numbers1) + " - " + str(self.n) + " - " + str(self.min_val) + " - " + str(self.max_val))
                #print("nu2 " + str(numbers1) + " - " + str(self.n) + " - " + str(self.min_val) + " - " + str(
                #    self.max_val))
                count += 1
                if super().draw(self.min_val, self.max_val, numbers1, len(numbers1)) and \
                        super().draw(self.min_val2, self.max_val2, numbers2, len(numbers2)):
                    break
            print("BREAK!")
            self.games.append(i)
            self.gameResults.append(count + 1)
        super().draft(len(self.gameResults)-numSpins, len(self.gameResults))
        if self.debug:
            logging.info(
                "Oczekiwany sredni czas wygranej w " + self.name + ": " + str(numbers1) + ", " + str(numbers2) +
                " , to: " + str(stat.mean(self.gameResults)) + "%\n")

        return self.gameResults
