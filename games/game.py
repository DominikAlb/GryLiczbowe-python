import calendar
import string
import time
from typing import List
from datetime import datetime, timedelta
import statistics as stat
import logging
import os
import random
import matplotlib.pyplot as plt

import boto3


class Game:

    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, randomInput: bool, *args):
        self.name: string = name
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

    def lasVegas(self, numSpins: int) -> []:
        pass

    def statistics(self, arr: List[float]) -> (float, float, float):
        mean = stat.mean(arr)
        var = stat.variance(arr)
        sd = stat.stdev(arr)

        print("Rezultat:\n")
        print("srednia, " + str(mean) + "\n")
        print("wariancja, " + str(var) + "\n")
        print("odchylenie standardowe, " + str(sd) + "\n")
        print("---------------------------------------------------------------\n")

        if self.debug:
            logging.info("Wariancja: " + str(var))
            logging.info("Odchylenie standardowe: " + str(sd))
            logging.info("srednia: " + str(mean))
            logging.info("Oczekiwany rezultat dla " + self.name + " to: " + str(round(100 * mean, 3)) + " % +/- " + str(
                round(100 * 1.96 * sd, 3)) + " % z 95% pewnoscia\n\n")

        return mean, var, sd

    def draft(self, min, max):
        #pass
        plt.ylabel("prawdopodobienstwo wygranej")
        plt.xlabel("liczba zakladow: " + self.name)
        plt.plot(self.games[min:max], self.gameResults[min:max])
        if "LasVegas" in self.name:
            self.timeToWin()

    def show(self):
        #pass
        plt.show()

    @staticmethod
    def draw(min_val: int, max_val: int, numbers: List[int], numSpins: int) -> bool:
        outcome = random.sample(range(min_val, max_val), numSpins)
        # print("OUT: " + str(outcome) + " : " + str(numSpins))
        count: int = 0
        for x in outcome:
            if x in numbers:
                count = count + 1
        if count == numSpins:
            return True
        return False

    def save(self, text: string, folder: string, isTemp: bool) -> bool:

        tempFolder = self.isTemporaryData(isTemp)
        if folder == '':
            folder = self.name
        try:
            bucket_name = "gryliczbowe"
            file_name = ""
            if not isTemp:
                file_name = tempFolder + folder + "/" + self.name + "-" + datetime.now().strftime("%H-%M-%S") + str(
                    self.randomInput) + ".csv"
            else:
                file_name = "temp/" + self.name + "/temp.csv"
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=file_name, Body=text)
        except Exception as e:
            logging.exception(e)
            return False
        return True

    def saveLocally(self, text: string, folder: string) -> bool:
        if folder == '':
            folder = self.name
        try:
            directory = os.path.join("D:\\", "awss3\\", folder)
            with open(directory + "\\" + self.name + "-" + datetime.now().strftime("%H-%M-%S") + str(
                    self.randomInput) + ".csv",
                      'a+', encoding='UTF8') as f:
                f.write(text)
                f.close()

        except Exception as e:
            print(e)
            return False
        return True

    def loadLocally(self, folder: str) -> bool:

        try:
            fixdata = []
            directory = os.path.join("D:\\", "awss3\\", folder)
            for root, dirs, files in os.walk(directory):
                for file in files:
                    gameResults: string = ""
                    results = []
                    if file.endswith(".csv"):
                        f = open(os.path.join(directory + "\\" + file), 'r')
                        gameResults = f.read().split('\n')[0]
                        for s in gameResults.split(' '):
                            try:
                                results.append(float(s))
                            except Exception as e:
                                continue

                        self.gameResults = results
                        self.games = range(1, len(self.gameResults) + 1)
                        self.draft(0, len(self.gameResults))
                        f.close()
                    fixdata += results
                    del gameResults
                    del results
            mean, var, sd = self.statistics(fixdata)
            text: string = "\nsrednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)
            #print(text)
            del fixdata
        except Exception as e:
            print(e)
            return False
        return True

    def load(self, isTemp: bool) -> bool:

        tempFolder = self.isTemporaryData(isTemp)
        bucket_name = "gryliczbowe"
        try:
            s3 = boto3.client("s3")
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=tempFolder + self.name + "/", MaxKeys=100)
            fixdata: list = []
            context = [obj for obj in response.get('Contents') if obj['Key'].endswith(str(self.randomInput) + '.csv')]
            for o in context:
                data = s3.get_object(Bucket=bucket_name, Key=o.get('Key'))
                gameResults = data['Body'].read().decode("utf-8").split('\n')[0]
                results = [0.0] + [float(s.replace('[', '').replace(',', '').replace(']', '')) for s in gameResults.split(' ')]
                if len(results) > 4:
                    continue
                for i in range(len(results)-1):
                    if results[i+1] < results[i]:
                        results[i+1] += results[i]
                self.gameResults = results
                self.games = range(0, len(results))
                self.draft(0, len(results))
                fixdata += results
                del gameResults
                del results
            mean, var, sd = self.statistics(fixdata)
            text: string = "\nsrednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)
            del fixdata
        except Exception as e:
            logging.exception(e)
            return False
        return True

    def isTemporaryData(self, isTemp: bool) -> string:
        tempFolder = ""
        if isTemp:
            tempFolder = "temp/"
        return tempFolder

    def loadTempDataIfExists(self) -> (list, list, int):
        bucket_name = "gryliczbowe"
        count = 0
        try:
            s3 = boto3.client("s3")
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix="temp/" + self.name + "/", MaxKeys=100)
            for o in response.get('Contents'):
                data = s3.get_object(Bucket=bucket_name, Key=o.get('Key'))
                gameResults = data['Body'].read().decode("utf-8").split('\n')[0]
                results = []
                try:
                    results = [int(s) for s in gameResults.split(' ')]
                except Exception as e:
                    print(e)
                    results = [int(gameResults)]
                previousGames = numberOfPreviousGames = []
                if len(results) == 1:
                    count = results[0]
                else:
                    previousGames: [] = results[1:len(results)]
                    numberOfPreviousGames: [] = list(range(1, len(previousGames)))
                    count = results[0]
                    # if len(numberOfPreviousGames) == 0:
                    #    numberOfPreviousGames.append(0)
                self.gameResults += previousGames
                self.games += numberOfPreviousGames
                del gameResults
                del results
            # s3.Object(bucket_name, "temp/" + self.name + "/temp.csv").delete()
        except Exception as e:
            print(e)
            #print(self.gameResults, self.games, count)
            return [], [], 0
        return self.gameResults, self.games, count

    def deleteTempFile(self):
        s3 = boto3.resource('s3')
        s3.Object('gryliczbowe', "temp/" + self.name + "/temp.csv").delete()

    def timeToWin(self) -> timedelta | None:

        drawPerWeek: int = 0
        drawPerDay: int = 0
        drawPerMinute: int = 0
        endDate: timedelta | None

        if "EuroRoulette" in self.name:
            drawPerMinute = 2
        elif "Lotto" in self.name:
            drawPerDay = 1
            drawPerWeek = 2
        elif "MultiMulti" in self.name:
            drawPerDay = 2
            drawPerWeek = 7
        elif "EuroJackpot" in self.name:
            drawPerDay = 1
            drawPerWeek = 2
        elif "PowerBall" in self.name:
            drawPerDay = 1
            drawPerWeek = 2

        if drawPerMinute != 0:
            tempValue = self.gameResults[-1] * drawPerMinute
            endDate = timedelta(days=tempValue / 1440)
        elif drawPerDay != 0 and drawPerWeek != 0:
            tempValue = self.gameResults[-1] / (drawPerDay * drawPerWeek)
            endDate = timedelta(weeks=tempValue)

        #print("Czas do wygranej: ", endDate.year, " lat, ", endDate.month, " miesięcy, ", endDate.day, " dni, ", endDate.hour, " godzin, ", endDate.minute, " minut.")
        #print("Oczekiwany wynik okolo: ", datetime.now() + timedelta(days=endDate.year * 365 * endDate.month * 30 + endDate.day, hours=endDate.hour, minutes=endDate.minute))
        print("Czas do wygranej: ", endDate.seconds / 1440, " dni, ")
        print("Oczekiwany wynik okolo: ", datetime.now() + timedelta(days=endDate.seconds / 1440))

        return endDate
