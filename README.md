# Betfair API Client

This package contains a class that acts as an interface to the Betfair Odds API.  It allows you to pull the latest betting market info from any sport.
## Installation
```pip install betfair_api_client```

## Usage

You can use it like this;
```
from betfair_api_client import BetfairApiClient

client = BetfairApiClient(
    username=BETFAIR_USERNAME, 
    password=BETFAIR_PASSWORD,
    apiKey=BETFAIR_API_KEY,
    clientCertificatePath=BETFAIR_CLIENT_CERTIFICATE_PATH,
    certificateKeyPath=BETFAIR_CLIENT_CERTIFICATE_KEY_PATH
)

competitions = client.list_competitions(countryCodes=['GB'], sportTypeIds=[1])

# return a list of "Event" classes
comingEvents = client.get_coming_events(
    sportTypeId=1,
    marketTypes=['MATCH_ODDS', 'HALF_TIME_SCORE'], 
    countryCodes=['GB'],
    textQuery='Liverpool',
    daysAhead=7,
)  

# return a list of "Event" classes with latest runner prices
eventsWithLatestOdds = client.update_prices_for_events(events=comingEvents)

exampleEvent = eventsWithLatestOdds[0]

# print out an "Event" class
print(exampleEvent)
# Liverpool v Tottenham (2020-12-16 20:00:00) - English Premier League (GB)

allEventMarkets = exampleEvent.get_all_markets()

# print a list of "Market" classes
print(allEventMarkets)
# [Market: "Match Odds".  Starts at: 2020-12-16 20:00:00, Market: "Half Time Score".  Starts at: 2020-12-16 20:00:00]

exampleMarket = allEventMarkets[0]

# return a list of "Runner" classes.
allRunners = exampleMarket.get_all_runners()
print(allRunners)
# [Liverpool (56323), Tottenham (48224), The Draw (58805)]

exampleRunner = allRunners[0]

# get the available runner prices (returned as a list of "RunnerPrice" classes)
print(exampleRunner.get_all_available_runner_prices())

# [betType: availableToBack, price: 1.84, size: 834.72,
# betType: availableToBack, price: 1.83, size: 984.71,
# betType: availableToBack, price: 1.82, size: 171.47,
# betType: availableToLay, price: 1.85, size: 221.73,
# betType: availableToLay, price: 1.86, size: 1562.24,
# betType: availableToLay, price: 1.87, size: 1458.99]

print(exampleRunner.get_best_lay_price())
# betType: availableToLay, price: 1.85, size: 221.73

print(exampleRunner.get_best_back_price())
# betType: availableToBack, price: 1.84, size: 834.72

```
