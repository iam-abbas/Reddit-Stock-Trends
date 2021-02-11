import configparser
import datetime as dt
import json
import re
import os

from collections import Counter, namedtuple
from itertools import chain
from pathlib import Path
from collections import Counter
from functools import reduce
from operator import add
from typing import Set

import pandas as pd
import praw
from tqdm import tqdm

Post = namedtuple('Post', 'id,title,score,comments,upvote_ratio,total_awards')


class TickerCounts:

    def __init__(self):
        self.webscraper_limit = 2000
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        self.subreddits = json.loads(config['FilteringOptions']['Subreddits'])

        stop_words = set(json.loads(config['FilteringOptions']['StopWords']))
        block_words = set(json.loads(config['FilteringOptions']['BlockWords']))
        with open('./config/tickers.json') as f:
            tickers = set(json.load(f))
        exclude = stop_words | block_words
        self.keep_tickers = tickers - exclude  # Remove words/tickers in exclude

    def extract_ticker(self, text: str, pattern: str = r'(?<=\$)[A-Za-z]+|[A-Z]{2,}') -> Set[str]:
        """Simple Regex to get tickers from text."""
        ticks = set(re.findall(pattern, str(text)))
        return ticks & self.keep_tickers  # Keep overlap

    def _get_posts(self):
        # Scrape subreddits. Currently it fetches additional data, only using title for now
        reddit = praw.Reddit('ClientSecrets')
        subreddits = '+'.join(self.subreddits)
        new_bets = reddit.subreddit(subreddits).new(limit=self.webscraper_limit)

        for post in tqdm(new_bets, desc='Selecting relevant data from webscraper', total=self.webscraper_limit):
            yield Post(
                post.id,
                post.title,
                post.score,
                post.num_comments,
                post.upvote_ratio,
                post.total_awards_received,
            )

    def get_data(self):
        df_posts = pd.DataFrame(self._get_posts())

        # Extract tickers from titles & count them
        tickers = df_posts['title'].apply(self.extract_ticker)
        counts = Counter(chain.from_iterable(tickers))

        # Create DataFrame of just mentions & remove any occurring less than 3 or less
        df_tick = pd.DataFrame(counts.items(), columns=['Ticker', 'Mentions'])
        df_tick = df_tick[df_tick['Mentions'] > 3]
        df_tick = df_tick.sort_values(by=['Mentions'], ascending=False)

        data_directory = Path('./data')
        data_directory.mkdir(parents=True, exist_ok=True)
        

        output_path = data_directory / f'{dt.date.today()}_tick_df.csv'
        df_tick.to_csv(output_path, index=False)
        print(df_tick.head())

def main():
    ticket = TickerCounts()
    ticket.get_data()

if __name__ == '__main__':
    main()
