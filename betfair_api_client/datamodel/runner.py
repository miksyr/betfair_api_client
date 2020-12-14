from typing import List

from .bet_types import BetTypes
from .runner_price import RunnerPrice


class Runner:

    def __init__(self, runnerId: int, runnerName: str, handicap: float):
        super().__init__()
        self.runnerId = runnerId
        self.runnerName = runnerName.strip()
        self.handicap = float(handicap)
        self.availableToBack = []
        self.availableToLay = []

    def __str__(self):
        return f'{self.runnerName} ({self.runnerId})'

    def __repr__(self):
        return self.__str__()

    def get_best_back_price(self):
        if len(self.availableToBack) == 0:
            return RunnerPrice(betType=BetTypes.BACK, price=0, size=0)
        return sorted(self.availableToBack, key=lambda x: x.price, reverse=True)[0]

    def get_best_lay_price(self):
        if len(self.availableToLay) == 0:
            return RunnerPrice(betType=BetTypes.LAY, price=0, size=0)
        return sorted(self.availableToLay, key=lambda x: x.price)[0]

    def get_all_available_runner_prices(self):
        return self.availableToBack + self.availableToLay

    def update_back_odds(self, availableToBack: List[RunnerPrice]):
        self.availableToBack = availableToBack

    def update_lay_odds(self, availableToLay: List[RunnerPrice]):
        self.availableToLay = availableToLay
