import requests
import re
import json


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

        index = 0
        match_events = self.get_todays_match_events()
        match_teams = self.get_todays_match_teams()
        match_time = self.get_todays_match_time()
        match_bestof = self.get_todays_match_bestof()
        match_odds = self.get_todays_match_odds()

        if match_events:
            while index < len(match_events):
                matches = {'team1': match_teams[index], 'team2': match_teams[index + 1],
                           'team1_odds': match_odds[index], 'team2_odds': match_odds[index+1],
                           'event': match_events[index], 'time': match_time[index], 'bestof': match_bestof[index]}

                json_array.append(matches)
                index += 1

        return json.dumps(json_array)

    def get_todays_match_teams(self):
        team_pattern = "class=\"teamtext\"><b>(.*)</b>"
        team_matches = re.findall(team_pattern, self.lounge_page_source)

        return team_matches

    def get_todays_match_time(self):
        when_pattern = "class=\"whenm\">(.*)<span"
        when_matches = re.findall(when_pattern, self.lounge_page_source)

        return when_matches

    def get_todays_match_events(self):
        event_pattern = "class=\"eventm\">(.*)</div>"
        event_matches = re.findall(event_pattern, self.lounge_page_source)

        return event_matches

    def get_todays_match_bestof(self):
        bestof_pattern = "<span class=\"format\">(.*)</span>"
        bestof_matches = re.findall(bestof_pattern, self.lounge_page_source)

        return bestof_matches

    def get_todays_match_odds(self):
        odds_pattern = "</b><br><i>(.*)</i>"
        odds_matches = re.findall(odds_pattern, self.lounge_page_source)

        return odds_matches
