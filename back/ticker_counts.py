import configparser
import json
import os
import re
from collections import Counter
from datetime import datetime
from functools import reduce
from operator import add
from typing import Set

import pandas as pd
import praw
from tqdm import tqdm


class TickerCounts:
    WEBSCRAPER_LIMIT = 2000
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    stop_words = json.loads(config['FilteringOptions']['StopWords'])
    block_words = json.loads(config['FilteringOptions']['BlockWords'])

    def verify_ticker(self, tick):
        with open('./config/tickers.json') as f:
            tickers = json.load(f)
        try:
            if tickers[tick]:
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
                    res.add(tick)
                except Exception as e:
                    print(e)
        return res

    def get_data(self):
        # Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
        # Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
        reddit = praw.Reddit('ClientSecrets')
        subreddits = '+'.join(json.loads(self.config['FilteringOptions']['Subreddits']))
        new_bets = reddit.subreddit(subreddits).new(limit=self.WEBSCRAPER_LIMIT)

        posts = [
            [
                post.id,
                post.title,
                post.score,
                post.num_comments,
                post.upvote_ratio,
                post.total_awards_received
            ] for post in tqdm(new_bets, desc='Selecting relevant data from webscraper', total=self.WEBSCRAPER_LIMIT)
        ]
        df_posts = pd.DataFrame(posts, columns=['id',
                                                'title',
                                                'score',
                                                'comments',
                                                'upvote_ratio',
                                                'total_awards'])

        # Extract tickers from all titles and create a new column
        df_posts['Tickers'] = df_posts['title'].apply(self.extract_ticker)
        tickers = df_posts['Tickers'].to_list()

        # Count number of occurrences of the Ticker and verify id the Ticker exists
        counts = reduce(add, map(Counter, tickers))

        verified_ticks = {}
        for ticker, ticker_count in tqdm(counts.items(), desc='Filtering verified ticks'):
            # If ticker is found more than 3 times and ticker is valid
            if ticker_count > 3 and self.verify_ticker(ticker):
                verified_ticks[ticker] = ticker_count

        # Create Datable of just mentions
        df_tick = pd.DataFrame(verified_ticks.items(), columns=['Ticker', 'Mentions'])
        df_tick.sort_values(by=['Mentions'], inplace=True, ascending=False)
        df_tick.reset_index(inplace=True, drop=True)

        date_created = datetime.today().strftime('%Y-%m-%d')
        filename = f'{date_created}_tick_df'
        data_directory = './data'

        if not os.path.exists(data_directory):
            os.mkdir(data_directory)

        output_path = f'{data_directory}/{filename}.csv'
        df_tick.to_csv(output_path, index=False)
        print(df_tick.head())


if __name__ == '__main__':
    ticket = TickerCounts()
    ticket.get_data()
