from unittest import TestCase

from betfair_api_client.betfair_api_client.datamodel.bet_types import BetTypes
from betfair_api_client.betfair_api_client.datamodel.runner import Runner
from betfair_api_client.betfair_api_client.datamodel.runner_price import RunnerPrice


class TestRunner(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestRunner, self).__init__(methodName=methodName)
        self.runnerName = 'testRunner'
        self.runnerId = 12345
        self.betfairRunnerTableId = 100
        self.availableToBack = [RunnerPrice(betType=BetTypes.BACK, price=i, size=i * 100) for i in range(0, 10, 3)]
        self.bestAvailableToBack = RunnerPrice(betType=BetTypes.BACK, price=9, size=900)
        self.availableToLay = [RunnerPrice(betType=BetTypes.LAY, price=i, size=i * 100) for i in range(10, 20, 3)]
        self.bestAvailableToLay = RunnerPrice(betType=BetTypes.LAY, price=10, size=1000)

    def setUp(self):
        super().setUp()
        self.noOddsRunner = Runner(runnerName=self.runnerName, runnerId=self.runnerId, handicap=0.0)
        self.oddsRunner = Runner(runnerName=self.runnerName, runnerId=self.runnerId, handicap=0.0)
        self.oddsRunner.update_back_odds(availableToBack=self.availableToBack)
        self.oddsRunner.update_lay_odds(availableToLay=self.availableToLay)

    def test_get_best_back_price(self):
        bestBackPrice = self.oddsRunner.get_best_back_price()
        self.assertEqual(bestBackPrice, self.bestAvailableToBack)

    def test_get_best_lay_price(self):
        bestLayPrice = self.oddsRunner.get_best_lay_price()
        self.assertEqual(bestLayPrice, self.bestAvailableToLay)

    def test_get_all_available_runner_prices(self):
        allPrices = self.oddsRunner.get_all_available_runner_prices()
        self.assertEqual(set(allPrices), set(self.availableToBack + self.availableToLay))

    def test_update_back_odds(self):
        self.noOddsRunner.update_back_odds(availableToBack=self.availableToBack)
        bestBackPrice = self.noOddsRunner.get_best_back_price()
        self.assertEqual(bestBackPrice, self.bestAvailableToBack)

    def test_update_lay_odds(self):
        self.noOddsRunner.update_lay_odds(availableToLay=self.availableToLay)
        bestLayPrice = self.noOddsRunner.get_best_lay_price()
        self.assertEqual(bestLayPrice, self.bestAvailableToLay)
