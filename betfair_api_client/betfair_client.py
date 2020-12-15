import json
import logging
import requests
import urllib
import urllib.request
import urllib.error

from datetime import datetime
from datetime import timedelta
from typing import List
from warnings import warn

from .datamodel.bet_types import BetTypes
from .datamodel.competition import Competition
from .datamodel.event import Event
from .datamodel.exceptions import BetfairException
from .datamodel.market import Market
from .datamodel.runner import Runner
from .datamodel.runner_price import RunnerPrice


class BetfairApiClient:

    ACCOUNT_ENDPOINT = 'https://api.betfair.com/exchange/account/json-rpc/v1'
    BETTING_ENDPOINT = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
    BETFAIR_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, username: str, password: str, apiKey: str, clientCertificatePath: str, certificateKeyPath: str):
        """
        Client for non-interactive connections to the betfair API.
        Non-interactive (bot) logins require self-signed certificates: https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login

        :param username: (str)
        :param password: (str)
        :param apiKey: (str)
        :param clientCertificatePath: (str)  Path to self-signed client certificate.
        :param certificateKeyPath: (str)  Path to self-signed client certificate key.
        """
        self.username = username
        self.password = password
        self.apiKey = apiKey
        self.clientCertificatePath = clientCertificatePath
        self.certificateKeyPath = certificateKeyPath
        self.sessionToken = None
        self.login()

    def login(self):
        response = requests.post(
            url='https://identitysso-cert.betfair.com/api/certlogin',
            data=f'username={self.username}&password={self.password}',
            cert=(self.clientCertificatePath, self.certificateKeyPath),
            headers={'X-Application': self.apiKey, 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        jsonResponse = response.json()
        logging.info(msg=f"Betfair client login status: {jsonResponse['loginStatus']}")
        if response.status_code == 200:
            self.sessionToken = jsonResponse['sessionToken']
        else:
            logging.exception(msg='Request failed.')
            logging.exception(msg=jsonResponse['loginStatus'])
            raise Exception(jsonResponse['loginStatus'])

    def send_heartbeat(self):
        response = requests.post(
            url='https://identitysso.betfair.com/api/keepAlive',
            headers={'X-Authentication': self.sessionToken, 'Accept': 'application/json'}
        )
        logging.info(msg=response.json()['status'])
        return response

    def _call_api(self, jsonrpcRequest: dict, endpointURL: str):
        try:
            request = urllib.request.Request(
                url=endpointURL,
                data=json.dumps(jsonrpcRequest).encode('utf-8'),
                headers={'X-Application': self.apiKey, 'X-Authentication': self.sessionToken, 'content-type': 'application/json'}
            )
            response = urllib.request.urlopen(request).read()
            decodedResponse = json.loads(response.decode('utf-8'))
            if 'result' in decodedResponse:
                return decodedResponse['result']
            return decodedResponse
        except urllib.error.URLError as ex:
            logging.exception(msg=ex)
            raise ex

    def check_balance(self):
        balanceRequest = {'jsonrpc': '2.0', 'method': 'AccountAPING/v1.0/getAccountFunds'}
        return self._call_api(jsonrpcRequest=balanceRequest, endpointURL=self.ACCOUNT_ENDPOINT)

    def list_competitions(self, countryCodes: List[str], sportTypeIds: List[int]):
        competitionsRequest = {
            "params": {
                "filter": {
                    "eventTypeIds": sportTypeIds,
                    'marketCountries': countryCodes,
                }
            },
            "jsonrpc": "2.0",
            "method": "SportsAPING/v1.0/listCompetitions",
            "id": 1
        }
        rawCompetitionData = self._call_api(jsonrpcRequest=competitionsRequest, endpointURL=self.BETTING_ENDPOINT)
        return [Competition(competitionId=int(competition['competition']['id']), competitionName=competition['competition']['name']) for competition in rawCompetitionData]

    def get_coming_events(self, sportTypeId: int, marketTypes: List[str], countryCodes: List[str] = None, textQuery: str = None, competitionIds: List[int] = None, daysAhead: int = 7):
        parameterDictionary = {
            'eventTypeIds': [sportTypeId],
            'marketTypeCodes': marketTypes,
            'marketStartTime': {
                'from': datetime.now().strftime('%Y-%m-%d'),
                'to': (datetime.now() + timedelta(days=daysAhead + 1)).strftime('%Y-%m-%d')
            }
        }
        if countryCodes is not None:
            parameterDictionary['marketCountries'] = countryCodes
        if textQuery is not None:
            parameterDictionary['textQuery'] = textQuery
        if competitionIds is not None:
            parameterDictionary['competitionIds'] = [int(competitionId) for competitionId in competitionIds]
        catalogueRequest = {
            'jsonrpc': '2.0',
            'method': 'SportsAPING/v1.0/listMarketCatalogue',
            'params': {
                'filter': parameterDictionary,
                'maxResults': 1000,
                'marketProjection': ['COMPETITION', 'EVENT', 'EVENT_TYPE', 'RUNNER_DESCRIPTION', 'RUNNER_METADATA', 'MARKET_START_TIME']
            },
            'id': 1
        }
        rawMarketsData = self._call_api(jsonrpcRequest=catalogueRequest, endpointURL=self.BETTING_ENDPOINT)
        if 'error' in rawMarketsData:
            raise BetfairException(rawMarketsData['error']['message'])
        processedEvents = self._process_raw_markets_data(rawMarketsData=rawMarketsData)
        return processedEvents

    def _process_raw_markets_data(self, rawMarketsData: List[dict]):
        processedEvents = {}
        for rawMarket in rawMarketsData:
            eventId = rawMarket['event']['id']
            if eventId not in processedEvents:
                competition = Competition(competitionId=int(rawMarket['competition']['id']), competitionName=rawMarket['competition']['name'])
                processedEvents[eventId] = Event(
                    eventId=int(eventId),
                    eventName=rawMarket['event']['name'],
                    eventDate=datetime.strptime(rawMarket['event']['openDate'], self.BETFAIR_DATETIME_FORMAT),
                    competition=competition,
                    countryCode=rawMarket['event']['countryCode']
                )
            market = Market(
                marketId=rawMarket['marketId'],
                marketName=rawMarket['marketName'],
                marketStartTime=datetime.strptime(rawMarket['marketStartTime'], self.BETFAIR_DATETIME_FORMAT)
            )
            for selection in rawMarket['runners']:
                market.add_runner(
                    runner=Runner(runnerId=int(selection['selectionId']), runnerName=selection['runnerName'], handicap=selection['handicap'])
                )
            processedEvents[eventId].add_market(market=market)
        return list(processedEvents.values())

    def update_prices_for_events(self, events: List[Event]):
        for i, event in enumerate(events):
            bookRequest = {
                'jsonrpc': '2.0',
                'method': 'SportsAPING/v1.0/listMarketBook',
                'params': {
                    'marketIds': list(event.markets.keys()),
                    'priceProjection': {'priceData': ['EX_BEST_OFFERS']},
                    'maxResults': '1000'
                },
                'id': 1
            }
            recentMarketData = self._call_api(jsonrpcRequest=bookRequest, endpointURL=self.BETTING_ENDPOINT)
            if i == 0 and len(recentMarketData):
                if recentMarketData[0]['isMarketDataDelayed']:
                    warn(message='Market data is delayed.  You may need to upgrade your Betfair Developer account to access live data.')
            for marketData in recentMarketData:
                marketIdUpdate = str(marketData['marketId'])
                for runnerInfo in marketData['runners']:
                    runnerUpdateId = int(runnerInfo['selectionId'])
                    backPrices = [RunnerPrice(betType=BetTypes.BACK, price=p['price'], size=p['size']) for p in runnerInfo['ex'][BetTypes.BACK]]
                    layPrices = [RunnerPrice(betType=BetTypes.LAY, price=p['price'], size=p['size']) for p in runnerInfo['ex'][BetTypes.LAY]]
                    # TODO(Mike): this is horrible
                    event.markets[marketIdUpdate].runners[runnerUpdateId].update_back_odds(availableToBack=backPrices)
                    event.markets[marketIdUpdate].runners[runnerUpdateId].update_lay_odds(availableToLay=layPrices)
            return events

    def place_bet(self, market: Market, runner: Runner, oddsToPlace: float, side: str, betSize: float):
        placeOrderRequest = {
            'jsonrpc': '2.0',
            'method': 'SportsAPING/v1.0/placeOrders',
            'params': {
                'marketId': market.marketId,
                'instructions': [{
                    'selectionId': runner.runnerId,
                    'side': side,
                    'orderType': 'LIMIT',
                    'limitOrder': {
                           'size': float(betSize),
                           'price': float(oddsToPlace),
                           'persistenceType': 'LAPSE'
                       }
                   }]
            },
            'id': 1
        }
        response = self._call_api(jsonrpcRequest=placeOrderRequest, endpointURL=self.BETTING_ENDPOINT)
        if response['status'] == 'FAILURE':
            logging.exception(msg=response)
            raise BetfairException(response['errorCode'])
        return response
