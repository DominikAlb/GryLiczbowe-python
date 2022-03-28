import string
from typing import List
from datetime import datetime
import statistics as stat
import logging
import os
import random
import plotly.express as px
import pandas as pd


class Game:

    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, *args):
        self.name = name
        self.debug = debug
        self.min_val = min_val
        self.max_val = max_val
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

    def play(self, numSpins: int, *args) -> float:
        pass

    def statistics(self, arr: List[float]) -> (float, float, float):
        mean = stat.mean(arr)
        var = stat.variance(arr)
        sd = stat.stdev(arr)
        arr = sorted(arr, key=float)
        arr2 = list(set(arr))
        arr2.sort()
        print("Rezultat:\n")
        print("srednia, " + str(mean) + "\n")
        print("wariancja, " + str(var) + "\n")
        print("odcylenie standardowe, " + str(sd) + "\n")
        print("---------------------------------------------------------------\n")

        if self.debug:
            logging.info("Wariancja: " + str(var))
            logging.info("Odchylenie standardowe: " + str(sd))
            logging.info("srednia: " + str(mean))
            logging.info("Oczekiwany rezultat dla ruletki to: " + str(round(100 * mean, 3)) + " % +/- " + str(
                round(100 * 1.96 * sd, 3)) + " % z 95% pewnoscia\n\n")
        arr.sort()
        x = list(dict.fromkeys(arr))
        y = [arr.count(i) for i in x]
        print("X: " + str(x) + "\n")
        print("Y: " + str(y) + "\n")
        df = pd.DataFrame(dict(x=x, y=y))
        fig = px.line(df, x="x", y="y", title="Unsorted Input")
        fig.show()

        df = df.sort_values(by="x")
        fig = px.line(df, x="x", y="y", title="Sorted Input")
        fig.show()
        return mean, var, sd

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
            file_name = folder + "/" + self.name + "-" + datetime.now().strftime("%H:%M:%S") + ".csv"
            s3_path = file_name
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=s3_path, Body=text)
        except Exception as e:
            logging.exception(e)
            return False
        return True

    @staticmethod
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def load(self, folder: str) -> bool:

        bucket_name = "gryliczbowe"
        try:
            fixdata: list = []
            s: string = ""
            directory = os.path.join("F:\\", "awss3\\", folder)
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".csv"):
                        f = open(os.path.join(directory + "\\" + file), 'r')
                        contents = f.read().split('\n')[0]
                        s = contents.replace(',', ' ').replace(']', ' ')
                        for i in s.split():
                            if self.isfloat(i):
                                fixdata.append(float(i))
                        del contents
                        del s
                        f.close()
            mean, var, sd = self.statistics(fixdata)
            text: string = str(fixdata) + "\nsrednia: " + str(mean) + "\nwariancja: " + str(
                var) + "\nodchylenie standardowe: " + str(sd)

        except Exception as e:
            logging.exception(e)
            return False
        return True
