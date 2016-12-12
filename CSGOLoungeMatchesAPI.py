import requests
import re
import json
from bs4 import BeautifulSoup


class CSGOLoungeMatchesAPI:
    def __init__(self):
        self.lounge_url = "https://csgolounge.com/"
        self.lounge_page_source = requests.get(self.lounge_url).text
        self.lounge_api = "http://csgolounge.com/api/matches"
        self.api_data = requests.get(self.lounge_api).text

    def get_past_team_results(self, team_name):
        team = team_name.lower()
        matches = json.loads(self.api_data)
        team_matches = []

        for match in matches:
            if team in match['a'].lower() or team in match['b'].lower():
                team_matches.append(match)

        return team_matches

    def get_past_match_results(self, team_name_a, team_name_b):
        teama = team_name_a.lower()
        teamb = team_name_b.lower()
        matches = json.loads(self.api_data)
        team_matches = []

        for match in matches:
            if (teama in match['a'].lower() and teamb in match['b'].lower()) or \
                    (teamb in match['a'].lower() and teama in match['b'].lower()):
                team_matches.append(match)

        return team_matches

    def get_upcoming_matches(self):
        upcoming_matches = []
        matches = json.loads(self.get_todays_matches())

        for match in matches:
            if "from now" in match['time']:
                upcoming_matches.append(match)

        return upcoming_matches

    def get_todays_matches_by_team(self, team_name):
        team_matches = []
        team = team_name.lower()
        matches = json.loads(self.get_todays_matches())

        for match in matches:
            if team in match['team1'].lower() or team in match['team2'].lower():
                team_matches.append(match)

        return team_matches

    def get_todays_matches(self):
        json_array = []

        soup = BeautifulSoup(self.lounge_page_source, "html.parser")

        matches = soup.find_all("div", "matchmain")

        for match in matches:
            match = str(match)
            index = 0
            match_event = self.get_todays_match_events(match)
            match_teams = self.get_todays_match_teams(match)
            match_time = self.get_todays_match_time(match)
            match_bestof = self.get_todays_match_bestof(match)
            match_odds = self.get_todays_match_odds(match)

            if match_event:
                matches = {'team1': match_teams[index], 'team2': match_teams[index + 1],
                           'team1_odds': match_odds[index], 'team2_odds': match_odds[index + 1],
                           # TODO get live attribute
                           'event': match_event, 'time': match_time, 'bestof': match_bestof, 'live': 'false'}

                json_array.append(matches)

        return json.dumps(json_array)

    def get_todays_match_teams(self, match):
        team_pattern = "class=\"teamtext\"><b>(.*)</b>"
        team_matches = re.findall(team_pattern, match)

        return team_matches

    def get_todays_match_time(self, match):
        when_pattern = "class=\"whenm\">(.*)<span"
        when_matches = re.search(when_pattern, match)

        if when_matches:
            return when_matches.group(1)

        else:
            return

    def get_todays_match_events(self, match):
        event_pattern = "class=\"eventm\">(.*)</div>"
        event_matches = re.search(event_pattern, match)

        if event_matches:
            return event_matches.group(1)

        else:
            return

    def get_todays_match_bestof(self, match):
        bestof_pattern = "<span class=\"format\">(.*)</span>"
        bestof_matches = re.search(bestof_pattern, match)

        if bestof_matches:
            return bestof_matches.group(1)

        else:
            return

    def get_todays_match_odds(self, match):
        odds_pattern = "</b><br><i>(.*)</i>"
        odds_matches = re.findall(odds_pattern, match)

        return odds_matches

CSGOLoungeMatches = CSGOLoungeMatchesAPI()

print CSGOLoungeMatches.get_upcoming_matches()
