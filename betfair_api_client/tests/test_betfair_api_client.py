import os
from datetime import datetime
from unittest import TestCase

from betfair_api_client.betfair_api_client import BetfairApiClient
from betfair_api_client.betfair_api_client.datamodel.competition import Competition
from betfair_api_client.betfair_api_client.datamodel.event import Event
from betfair_api_client.betfair_api_client.datamodel.exceptions import TooMuchData
from betfair_api_client.betfair_api_client.datamodel.market import Market
from betfair_api_client.betfair_api_client.datamodel.market_types import MarketTypes
from betfair_api_client.betfair_api_client.datamodel.runner import Runner
from betfair_api_client.betfair_api_client.datamodel.runner_price import RunnerPrice


TEST_COMPETITION = Competition(competitionId=12117172, competitionName='Australian A-League')
TEST_EVENT = Event(
    eventId=29939806,
    eventName='Western Sydney Wanderers v Perth Glory',
    eventDate=datetime(year=2020, month=8, day=4, hour=9, minute=30, second=0),
    competition=TEST_COMPETITION,
    countryCode='AU'
)
TEST_MARKET = Market(marketId='1.171796736', marketName='Match Odds', marketStartTime=datetime(year=2020, month=8, day=4, hour=9, minute=30, second=0))
FIRST_TEST_RUNNER = Runner(runnerId=6480414, runnerName='Western Sydney Wanderers', handicap=0.0)
SECOND_TEST_RUNNER = Runner(runnerId=370132, runnerName='Perth Glory', handicap=-2.0)
THIRD_TEST_RUNNER = Runner(runnerId=58805, runnerName='The Draw', handicap=1.0)
ALL_TEST_RUNNERS = [FIRST_TEST_RUNNER, SECOND_TEST_RUNNER, THIRD_TEST_RUNNER]


class TestBetfairClient(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestBetfairClient, self).__init__(methodName=methodName)
        self.betfairClient = BetfairApiClient(
            username=os.environ['BETFAIR_USERNAME'],
            password=os.environ['BETFAIR_PASSWORD'],
            apiKey=os.environ['BETFAIR_API_KEY'],
            clientCertificatePath=os.environ['BETFAIR_CLIENT_CERT'],
            certificateKeyPath=os.environ['BETFAIR_CLIENT_CERT_KEY']
        )
        self.rawMatchOddsData = [
            {
                'marketId': TEST_MARKET.marketId,
                'marketName': TEST_MARKET.marketName,
                'marketStartTime': TEST_MARKET.marketStartTime.strftime(BetfairApiClient.BETFAIR_DATETIME_FORMAT),
                'runners': [
                    {
                        'selectionId': FIRST_TEST_RUNNER.runnerId,
                        'runnerName': FIRST_TEST_RUNNER.runnerName,
                        'handicap': FIRST_TEST_RUNNER.handicap,
                    },
                    {
                        'selectionId': SECOND_TEST_RUNNER.runnerId,
                        'runnerName': SECOND_TEST_RUNNER.runnerName,
                        'handicap': SECOND_TEST_RUNNER.handicap,
                    },
                    {
                        'selectionId': THIRD_TEST_RUNNER.runnerId,
                        'runnerName': THIRD_TEST_RUNNER.runnerName,
                        'handicap': THIRD_TEST_RUNNER.handicap,
                    }
                ],
                'eventType': {'id': '1', 'name': 'Soccer'},
                'competition': {'id': str(TEST_COMPETITION.competitionId), 'name': TEST_COMPETITION.competitionName},
                'event': {
                    'id': str(TEST_EVENT.eventId),
                    'name': TEST_EVENT.eventName,
                    'countryCode': TEST_EVENT.countryCode,
                    'openDate': TEST_EVENT.eventDate.strftime(self.betfairClient.BETFAIR_DATETIME_FORMAT),
                }
            }
        ]
        self.exampleProcessedEvent = TEST_EVENT
        for runner in ALL_TEST_RUNNERS:
            TEST_MARKET.add_runner(runner=runner)
        self.exampleProcessedEvent.add_market(market=TEST_MARKET)

    def test_login(self):
        self.assertIsNotNone(self.betfairClient.sessionToken)
        self.assertNotEqual(self.betfairClient.sessionToken, '')

    def test_send_heartbeat(self):
        response = self.betfairClient.send_heartbeat()
        self.assertTrue(response.ok)

    def test_check_balance(self):
        dictResponse = self.betfairClient.check_balance()
        self.assertTrue('availableToBetBalance' in dictResponse)

    def test_list_competitions(self):
        results = self.betfairClient.list_competitions(countryCodes=['GB'], sportTypeIds=[1])
        self.assertTrue(Competition(competitionId=10932509, competitionName='English Premier League') in results)

    def test_get_coming_events(self):
        try:
            comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, marketTypes=[MarketTypes.MATCH_ODDS], daysAhead=1)
        except TooMuchData:
            try:
                comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, countryCodes=['GB'], marketTypes=[MarketTypes.MATCH_ODDS])
            except TooMuchData:
                comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, marketTypes=[MarketTypes.MATCH_ODDS], daysAhead=0)
        self.assertTrue(isinstance(comingEvents, list))
        self.assertTrue(len(comingEvents) > 0)
        self.assertTrue(isinstance(comingEvents[0], Event))

    def test_process_raw_markets_data(self):
        processedEvent = self.betfairClient._process_raw_markets_data(rawMarketsData=self.rawMatchOddsData)[0]
        self.assertEqual(processedEvent.eventId, self.exampleProcessedEvent.eventId)
        self.assertEqual(processedEvent.eventName, self.exampleProcessedEvent.eventName)
        self.assertEqual(processedEvent.eventDate, self.exampleProcessedEvent.eventDate)
        processedMarket = processedEvent.get_all_markets()[0]
        self.assertEqual(processedMarket.marketId, TEST_MARKET.marketId)
        self.assertEqual(processedMarket.marketName, TEST_MARKET.marketName)
        self.assertEqual(processedMarket.marketStartTime, TEST_MARKET.marketStartTime)
        processedRunners = processedMarket.get_all_runners()
        self.assertEqual({r.runnerId for r in processedRunners}, {r.runnerId for r in ALL_TEST_RUNNERS})
        self.assertEqual({r.runnerName for r in processedRunners}, {r.runnerName for r in ALL_TEST_RUNNERS})
        self.assertEqual({r.handicap for r in processedRunners}, {r.handicap for r in ALL_TEST_RUNNERS})

    def test_update_prices_for_events(self):
        try:
            comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, marketTypes=[MarketTypes.MATCH_ODDS], daysAhead=1)
        except TooMuchData:
            try:
                comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, countryCodes=['GB'], marketTypes=[MarketTypes.MATCH_ODDS], daysAhead=1)
            except TooMuchData:
                comingEvents = self.betfairClient.get_coming_events(sportTypeId=1, marketTypes=[MarketTypes.MATCH_ODDS], daysAhead=0)
        updatedEvents = self.betfairClient.update_prices_for_events(events=comingEvents)
        exampleMarket = updatedEvents[0].get_all_markets()[0]
        marketRunners = exampleMarket.get_all_runners()
        for runner in marketRunners:
            bestBackPrice = runner.get_best_back_price()
            self.assertTrue(isinstance(bestBackPrice, RunnerPrice))
            self.assertTrue(bestBackPrice.price > 0)
            self.assertTrue(bestBackPrice.size > 0)
            bestLayPrice = runner.get_best_lay_price()
            self.assertTrue(isinstance(bestLayPrice, RunnerPrice))
            self.assertTrue(bestLayPrice.price > 0)
            self.assertTrue(bestLayPrice.size > 0)
            self.assertTrue(len(runner.get_all_available_runner_prices()) > 0)
