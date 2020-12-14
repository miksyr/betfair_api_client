from datetime import datetime

from .runner import Runner


class Market:

    def __init__(self, marketId: str, marketName: str, marketStartTime: datetime):
        self.marketId = marketId
        self.marketName = marketName
        self.marketStartTime = marketStartTime
        self.runners = {}

    def __repr__(self):
        return f'Market: "{self.marketName}".  Starts at: {self.marketStartTime}'

    def __str__(self):
        return self.__repr__()

    def add_runner(self, runner: Runner):
        if runner.runnerId not in self.runners:
            self.runners[runner.runnerId] = runner

    def get_all_runners(self):
        return list(self.runners.values())
