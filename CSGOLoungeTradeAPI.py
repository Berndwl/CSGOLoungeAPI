import re
import requests


class CSGOLoungeTradeAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.token = self.login()

    def login(self):
        with self.session as s:
            response = s.get("https://csgolounge.com").text

            token = re.search("lngSlt = \'(.*)\';", response)

            if token:
                post_data = {"em": self.username,
                             "pass": self.password,
                             "llss": token.group(1)}

                s.post("https://csgolounge.com/ajax/logIn.php", data=post_data)

                return token

        return

    def bump_trades(self):
        with self.session as s:
            response = s.get("https://csgolounge.com/mytrades").text

            trade_ids = re.findall("bumpTrade\(\'(.*)\'\)", response)

            for trade_id in trade_ids:
                post_data = {"trade": trade_id}

                s.post("https://csgolounge.com/ajax/bumpTrade.php", data=post_data)

    def get_trade_ids(self):
        with self.session as s:
            response = s.get("https://csgolounge.com/mytrades").text

            trade_ids = re.findall("href=\"trade\?t=(.*)\">", response)

            return trade_ids

    def remove_trade(self, trade_id):
        with self.session as s:

            post_data = {"trade": trade_id}
            s.post("https://csgolounge.com/ajax/removeTrade.php", data=post_data)

