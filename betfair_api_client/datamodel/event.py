from datetime import datetime

from .competition import Competition
from .market import Market


class Event:

    def __init__(self, eventId: int, eventName: str, eventDate: datetime, competition: Competition, countryCode: str):
        super().__init__()
        self.eventId = eventId
        self.eventName = eventName
        self.eventDate = eventDate
        self.competition = competition
        self.countryCode = countryCode
        self.markets = {}

    def __str__(self):
        return f'{self.eventName} ({self.eventDate}) - {self.competition.competitionName} ({self.countryCode})'

    def __repr__(self):
        return self.__str__()

    def add_market(self, market: Market):
        if market.marketId not in self.markets:
            self.markets[market.marketId] = market

    def get_all_markets(self):
        return list(self.markets.values())
