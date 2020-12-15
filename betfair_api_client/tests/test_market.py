from datetime import datetime
from unittest import TestCase

from betfair_api_client.betfair_api_client.datamodel.market import Market
from betfair_api_client.betfair_api_client.datamodel.runner import Runner


class TestMarket(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestMarket, self).__init__(methodName=methodName)
        self.firstTestRunner = Runner(runnerId=1234, runnerName='firstTestRunner', handicap=1.0)
        self.secondTestRunner = Runner(runnerId=5678, runnerName='secondTestRunner', handicap=-2.0)

    def setUp(self):
        super().setUp()
        self.testMarket = Market(marketId='1.17234', marketName='testMarket', marketStartTime=datetime(year=1970, month=1, day=1))

    def test_add_runner(self):
        self.testMarket.add_runner(runner=self.firstTestRunner)
        self.assertEqual(len(self.testMarket.runners), 1)
        addedRunnerClass = list(self.testMarket.runners.values())[0]
        self.assertEqual(addedRunnerClass.runnerId, self.firstTestRunner.runnerId)

    def test_add_runner_duplicate(self):
        self.testMarket.add_runner(runner=self.firstTestRunner)
        self.testMarket.add_runner(runner=self.firstTestRunner)
        self.assertEqual(len(self.testMarket.runners), 1)
        addedRunnerClass = list(self.testMarket.runners.values())[0]
        self.assertEqual(addedRunnerClass.runnerId, self.firstTestRunner.runnerId)

    def test_add_runner_multiple(self):
        self.testMarket.add_runner(runner=self.firstTestRunner)
        self.testMarket.add_runner(runner=self.secondTestRunner)
        self.assertEqual(len(self.testMarket.runners), 2)
        addedRunnerClassIds = {runner.runnerId for runner in self.testMarket.runners.values()}
        self.assertTrue(addedRunnerClassIds == {self.firstTestRunner.runnerId, self.secondTestRunner.runnerId})

    def test_get_all_runners(self):
        self.testMarket.add_runner(runner=self.firstTestRunner)
        self.testMarket.add_runner(runner=self.secondTestRunner)
        allRunners = self.testMarket.get_all_runners()
        self.assertEqual(len(allRunners), 2)
        addedRunnerClassIds = {runner.runnerId for runner in allRunners}
        self.assertTrue(addedRunnerClassIds == {self.firstTestRunner.runnerId, self.secondTestRunner.runnerId})
