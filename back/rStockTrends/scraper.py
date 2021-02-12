from collections import Counter
from datetime import datetime
from functools import reduce
from operator import add
from typing import Set
import time
import pandas as pd
import praw
from tqdm import tqdm
import json
import os

import scraper_utils
import data_processor
import yfinance_utils

class Scraper:

    def __init__(self, NLP=False, scrapeHours=24):
        self.WEBSCRAPER_LIMIT = 2000
        self.ScraperUtils = scraper_utils.ScraperUtils()
        self.Processor = data_processor.DataProcessor(NLP)
        self.scrapeHours = scrapeHours

    def get_data(self):
        # Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
        # Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
        reddit = praw.Reddit('ClientSecrets')
        subreddits = "pennystocks+robinhoodpennystocks"
        subData = reddit.subreddit(subreddits).new(limit=self.WEBSCRAPER_LIMIT)
        current_time = int(time.time())
        posts = []
        for post in subData:
            post_age = (current_time - post.created_utc) / \
                60 / 60 / self.scrapeHours
            flair = post.link_flair_text if post.link_flair_text else "None"
            if post_age < 1 and any(sub in flair for sub in ["DD", "News", "Discussion", "Catalyst", "Tips", "Stock"]):
                credibility = self.Processor.userCredibility(post.author)
                tickers = self.ScraperUtils.extract_ticker(post.title)
                if credibility > 0.75 and len(list(tickers)) > 0:
                    rating = self.Processor.postRating(post)
                    sentiment = self.Processor.commentSentiment(post)
                    posts.append(
                        [
                            post.id,
                            post.title,
                            tickers,
                            rating,
                            sentiment,
                            flair,
                            credibility
                        ]
                    )

        df_posts = pd.DataFrame(posts, columns=['id',
                                                'title',
                                                'tickers',
                                                'rating',
                                                'sentiment',
                                                'flair',
                                                'credibility'])

        df_posts.title.drop_duplicates(keep='first', inplace=True)
        tickers = df_posts.tickers.to_list()

        # Count number of occurrences of the Ticker and verify id the Ticker exists
        counts = reduce(add, map(Counter, tickers))

        # Create Datable of just mentions
        df_tick = pd.DataFrame(counts,
                               columns=['Ticker', 'Mentions'])
        df_tick.sort_values(by=['Mentions'], inplace=True, ascending=False)
        df_tick.reset_index(inplace=True, drop=True)

        date_created = datetime.today().strftime('%Y-%m-%d')
        filename = f'{date_created}_tick_df'
        data_directory = './data'

        if not os.path.exists(data_directory):
            os.mkdir(data_directory)
        print(df_tick)
        output_path = f'{data_directory}/{filename}.csv'
        df_tick.to_csv(output_path, index=False)


        finance_df = yfinance_utils.FinanceAnalysis(df_tick)

        return finance_df




if __name__ == '__main__':
    ticket = Scraper()
    ticket.get_data()
