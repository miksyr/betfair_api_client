from datetime import datetime
from unittest import TestCase

from betfair_api_client.betfair_api_client.datamodel.competition import Competition
from betfair_api_client.betfair_api_client.datamodel.event import Event
from betfair_api_client.betfair_api_client.datamodel.market import Market


class TestEvent(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestEvent, self).__init__(methodName=methodName)
        self.firstTestMarket = Market(marketId='1.234567', marketName='firstTestMarket', marketStartTime=datetime(year=1970, month=1, day=1))
        self.secondTestMarket = Market(marketId='7.654321', marketName='secondTestMarket', marketStartTime=datetime(year=1980, month=12, day=12))

    def setUp(self):
        super().setUp()
        self.testEvent = Event(
            eventId=97531,
            eventName='testEvent',
            eventDate=datetime(year=1990, month=6, day=6),
            competition=Competition(competitionName='testCompetition', competitionId=24),
            countryCode='GB'
        )

    def test_add_market_single(self):
        self.testEvent.add_market(market=self.firstTestMarket)
        self.assertEqual(len(self.testEvent.markets), 1)
        addedMarketClass = list(self.testEvent.markets.values())[0]
        self.assertEqual(addedMarketClass.marketId, self.firstTestMarket.marketId)

    def test_add_market_duplicate(self):
        self.testEvent.add_market(market=self.firstTestMarket)
        self.testEvent.add_market(market=self.firstTestMarket)
        self.assertEqual(len(self.testEvent.markets), 1)
        addedMarketClass = list(self.testEvent.markets.values())[0]
        self.assertEqual(addedMarketClass.marketId, self.firstTestMarket.marketId)

    def test_add_market_multiple(self):
        self.testEvent.add_market(market=self.firstTestMarket)
        self.testEvent.add_market(market=self.secondTestMarket)
        self.assertEqual(len(self.testEvent.markets), 2)
        addedMarketClassIds = {market.marketId for market in self.testEvent.markets.values()}
        self.assertTrue(addedMarketClassIds == {self.firstTestMarket.marketId, self.secondTestMarket.marketId})

    def test_get_all_markets(self):
        self.testEvent.add_market(market=self.firstTestMarket)
        self.testEvent.add_market(market=self.secondTestMarket)
        allMarkets = self.testEvent.get_all_markets()
        self.assertEqual(len(allMarkets), 2)
        addedMarketClassIds = {market.marketId for market in allMarkets}
        self.assertTrue(addedMarketClassIds == {self.firstTestMarket.marketId, self.secondTestMarket.marketId})
