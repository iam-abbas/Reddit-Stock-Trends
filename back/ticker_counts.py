import configparser
import datetime as dt
import json
import re
from collections import Counter, namedtuple
from functools import reduce
from operator import add
from pathlib import Path
from typing import Set

import pandas as pd
import praw
from tqdm import tqdm

Post = namedtuple('Post', 'id,title,score,comments,upvote_ratio,total_awards')


class TickerCounts:
    WEBSCRAPER_LIMIT = 2000
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    stop_words = json.loads(config['FilteringOptions']['StopWords'])
    block_words = json.loads(config['FilteringOptions']['BlockWords'])
    subreddits = json.loads(config['FilteringOptions']['Subreddits'])
    with open('./config/tickers.json') as f:
        tickers = json.load(f)

    def verify_ticker(self, tick):
        return tick in self.tickers

    def extract_ticker(self, text: str, pattern: str = r'(?<=\$)[A-Za-z]+|[A-Z]{2,}') -> Set[str]:
        """Simple Regex to get tickers from text."""
        ticks = set(re.findall(pattern, str(text)))
        res = set()
        for tick in ticks:
            tick = tick.upper()
            if tick in self.block_words or tick in self.stop_words:
                continue

            if not self.verify_ticker(tick):
                continue
            res.add(tick)
        return res

    def _get_posts(self):
        # Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
        # Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
        reddit = praw.Reddit('ClientSecrets')
        subreddits = '+'.join(self.subreddits)
        new_bets = reddit.subreddit(subreddits).new(limit=self.WEBSCRAPER_LIMIT)

        for post in tqdm(new_bets, desc='Selecting relevant data from webscraper', total=self.WEBSCRAPER_LIMIT):
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

        # Extract tickers from all titles and create a new column
        df_posts['Tickers'] = df_posts['title'].apply(self.extract_ticker)
        tickers = df_posts['Tickers']

        # Count number of occurrences of the Ticker and verify id the Ticker exists
        counts = reduce(add, map(Counter, tickers))

        verified_ticks = {}
        for ticker, ticker_count in tqdm(counts.items(), desc='Filtering verified ticks'):
            # If ticker is found more than 3 times and ticker is valid
            if ticker_count > 3:
                verified_ticks[ticker] = ticker_count

        # Create Datable of just mentions
        df_tick = pd.DataFrame(verified_ticks.items(), columns=['Ticker', 'Mentions'])
        df_tick = df_tick.sort_values(by=['Mentions'], ascending=False)

        data_directory = Path('./data')
        data_directory.mkdir(parents=True, exist_ok=True)

        output_path = data_directory / f'{dt.date.today()}_tick_df.csv'
        df_tick.to_csv(output_path, index=False)
        print(df_tick.head())


if __name__ == '__main__':
    ticket = TickerCounts()
    ticket.get_data()
