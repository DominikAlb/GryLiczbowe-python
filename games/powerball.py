import string

from games.eurojackpot import EuroJackpot


class PowerBall(EuroJackpot):
    def __init__(self, name: string, debug: bool, min_val: int, max_val: int, *args):
        super().__init__(name, debug, min_val, max_val, *args)

    def play(self, numSpins: int, *args) -> float:
        return super().play(numSpins, *args)
