import string

from games.eurojackpot import EuroJackpot


class PowerBall(EuroJackpot):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, randomInput: bool, *args):
        super().__init__(name, debug, min_val, max_val, randomInput, *args)

    def monteCarlo(self, numSpins: int) -> float:
        return super().monteCarlo(numSpins)

    def lasVegas(self, numSpins: int) -> []:
        return super().lasVegas(numSpins)
