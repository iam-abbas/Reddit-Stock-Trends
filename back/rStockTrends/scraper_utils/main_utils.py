import json
import os
import re
import json
import configparser
from typing import Set


class ScraperUtils:

    config_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'config/config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    stop_words = json.loads(config['FilteringOptions']['StopWords'])
    block_words = json.loads(config['FilteringOptions']['BlockWords'])
    with open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'config/tickers.json')) as f:
        tickers = json.load(f)

    def isTickerValid(self, tick):
        try:
            if self.tickers[tick]:
                return True
        except Exception as e:
            pass
        return False

    def extract_ticker(self, body: str, re_string: str = r'[$][A-Za-z]*|[A-Z][A-Z]{1,}') -> Set[str]:
        """Simple Regex to get tickers from text."""
        ticks = set(re.findall(re_string, str(body)))
        res = set()
        for item in ticks:
            if item not in self.block_words and item.lower() not in self.stop_words and item:
                try:
                    tick = item.replace('$', '').upper()
                    if self.isTickerValid(tick):
                        res.add(tick)
                except Exception as e:
                    print(e)
        return res
