# CSGOLoungeAPI

## A Quick written CSGOLounge API in python

### Matches API Usage:
```
CSGOLoungeMatches = CSGOLoungeMatchesAPI()

CSGOLoungeMatches.get_todays_matches()

CSGOLoungeMatches.get_upcoming_matches()

CSGOLoungeMatches.get_todays_matches_by_team("Immortals")

CSGOLoungeMatches.get_past_team_results("NIP")

CSGOLoungeMatches.get_past_match_results("Immortals", "NIP")
```

### Trade API Usage:
```
CSGOLoungeTrade = CSGOLoungeTradeAPI("email@email.com", "password")
CSGOLoungeTrade.bump_trades()

for trade_id in CSGOLoungeTrade.get_trade_ids():
    CSGOLoungeTrade.remove_trade(trade_id)

```
