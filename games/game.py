import string
from typing import List
from datetime import datetime
import statistics as stat
import logging
import os
import random
#import matplotlib.pyplot as plt

import boto3


class Game:

    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, randomInput: bool, *args):
        self.name = name
        self.debug = debug
        self.min_val = min_val
        self.max_val = max_val
        self.randomInput = randomInput
        self.games = []
        self.gameResults = []
        if len(args) == 1 and isinstance(args[0], int):
            self.n = args[0]
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self.n = args[0]
            self.m = args[1]
        elif len(args) == 4 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2],
                                                                                                     int) and isinstance(
                args[3], int):
            self.n = args[0]
            self.min_val2 = args[1]
            self.max_val2 = args[2]
            self.m = args[3]

    def monteCarlo(self, numSpins: int) -> float:
        pass

    def lasVegas(self, numSpins: int) -> float:
        pass

    def statistics(self, arr: List[float]) -> (float, float, float):
        mean = stat.mean(arr)
        var = stat.variance(arr)
        sd = stat.stdev(arr)

        print("Rezultat:\n")
        print("srednia, " + str(mean) + "\n")
        print("wariancja, " + str(var) + "\n")
        print("odcylenie standardowe, " + str(sd) + "\n")
        print("---------------------------------------------------------------\n")

        if self.debug:
            logging.info("Wariancja: " + str(var))
            logging.info("Odchylenie standardowe: " + str(sd))
            logging.info("srednia: " + str(mean))
            logging.info("Oczekiwany rezultat dla " + self.name + " to: " + str(round(100 * mean, 3)) + " % +/- " + str(
                round(100 * 1.96 * sd, 3)) + " % z 95% pewnoscia\n\n")

        return mean, var, sd

    def draft(self):
        pass
        #plt.ylabel("prawdopodobienstwo wygranej")
        #plt.xlabel("liczba zakladow: " + self.name)
        #plt.plot(self.games, self.gameResults)
        #plt.show()

    @staticmethod
    def draw(min_val: int, max_val: int, numbers: List[int], numSpins: int) -> bool:
        outcome = random.sample(range(min_val, max_val), numSpins)
        count: int = 0
        for x in outcome:
            if x in numbers:
                count = count + 1
        if count == numSpins:
            return True
        return False

    def save(self, text: string, folder: string) -> bool:
        if folder == '':
            folder = self.name
        try:
            bucket_name = "gryliczbowe"
            file_name = folder + "/" + self.name + "-" + datetime.now().strftime("%H:%M:%S") + str(self.randomInput) + ".csv"
            s3_path = file_name
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=s3_path, Body=text)
        except Exception as e:
            logging.exception(e)
            return False
        return True

    def saveLocally(self, text: string, folder: string) -> bool:
        if folder == '':
            folder = self.name
        try:
            directory = os.path.join("F:\\", "awss3\\", folder)
            with open(directory + "\\" + self.name + "-" + datetime.now().strftime("%H-%M-%S") + str(self.randomInput) + ".csv",
                      'a+', encoding='UTF8') as f:
                f.write(text)

        except Exception as e:
            logging.exception(e)
            return False
        return True

    def loadLocally(self, folder: str) -> bool:

        try:
            fixdata = []
            directory = os.path.join("F:\\", "awss3\\", folder)
            for root, dirs, files in os.walk(directory):
                for file in files:
                    gameResults: string = ""
                    results = []
                    if file.endswith(".csv"):
                        f = open(os.path.join(directory + "\\" + file), 'r')
                        gameResults = f.read().split('\n')[0]
                        results = [float(s) for s in gameResults.split(' ')]
                        self.gameResults = results
                        self.games = range(1, len(self.gameResults) + 1)
                        self.draft()
                        f.close()
                    fixdata += results
                    del gameResults
                    del results
            mean, var, sd = self.statistics(fixdata)
            text: string = "\nsrednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)
            print(text)
            del fixdata
        except Exception as e:
            if self.debug:
                logging.exception(e)
            else:
                print(e)
            return False
        return True

    def load(self) -> bool:

        bucket_name = "gryliczbowe"
        try:
            s3 = boto3.client("s3")
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=self.name + "/", MaxKeys=100)
            fixdata: list = []
            arr = []
            for o in response.get('Contents'):
                data = s3.get_object(Bucket=bucket_name, Key=o.get('Key'))
                gameResults = data['Body'].read().decode("utf-8").split('\n')[0]
                results = [float(s) for s in gameResults.split(' ')]
                arr += results
                self.gameResults = results
                self.games = range(1, len(self.gameResults) + 1)
                self.draft()
                del results
            mean, var, sd = self.statistics(fixdata)
            text: string = "\nsrednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)
            self.save(text, 'statistics')
            del fixdata
        except Exception as e:
            logging.exception(e)
            return False
        return True
