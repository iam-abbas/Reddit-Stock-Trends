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
import yfinance as yf

from . import main_utils
from . import processing
from . import yfinance_analysis


class StockTrends:

    def __init__(self, NLP=False):
        self.WEBSCRAPER_LIMIT = 2000
        self.ScraperUtils = main_utils.ScraperUtils()
        self.Processor = processing.DataProcessor(NLP)

    def scrape_posts(self, scrape_hours=24, flairs=["DD", "News", "Discussion", "Catalyst", "Tips", "Stock"]):
        # Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
        # Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
        reddit = praw.Reddit('ClientSecrets')
        subreddits = "pennystocks+robinhoodpennystocks"
        subData = reddit.subreddit(subreddits).new(limit=self.WEBSCRAPER_LIMIT)
        current_time = int(time.time())
        posts = []
        print("Fetching Posts...")
        for post in subData:
            post_age = (current_time - post.created_utc) / \
                60 / 60 / scrape_hours
            flair = post.link_flair_text if post.link_flair_text else "None"
            if post_age < 1 and any(sub in flair for sub in flairs):
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

        return df_posts

    def TickersFromPosts(self, df_posts):

        try:
            tickers = df_posts.tickers.to_list()
        except:
            tickers = self.scrape_posts().tickers.to_list()
        print("Processing Tickers...")
        # Count number of occurrences of the Ticker and verify id the Ticker exists
        counts = reduce(add, map(Counter, tickers))

        # Create Datable of just mentions
        df_tick = pd.DataFrame(counts.items(),
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

        return df_tick

    def getFinanceData(self, df_tick):

        Finance = yfinance_analysis.FinanceAnalysis(df_tick)

        finance_df = Finance.analyze()

        return finance_df

    def dataWithStats(self, data_df, df_posts):
        df_posts.tickers = df_posts.tickers.apply(list)
        res = df_posts.set_index(["id",	"title", "rating", "sentiment",	"flair", "credibility"])[
            'tickers'].apply(pd.Series).stack()
        res = res.reset_index()
        res.rename(columns={0: 'Tickers'}, inplace=True)
        res = res.sort_values(by=["rating"], ascending=False)
        res.loc[:, ~res.columns.str.startswith('level')]
        res = res[res.flair.str.contains("DD|Catalyst").astype('bool')]
        catalyst_df = res[res.flair.str.contains("Catalyst").astype('bool')]
        dd_df = res[res.flair.str.contains("DD").astype('bool')]
        final_df = data_df.copy()
        final_df["DD"] = final_df.Ticker.map(dd_df.set_index('Tickers')['title'].to_dict(
        ))+"::"+final_df.Ticker.map(dd_df.set_index('Tickers')['id'].to_dict())
        final_df["Catalyst"] = final_df.Ticker.map(catalyst_df.set_index('Tickers')['title'].to_dict(
        ))+"::"+final_df.Ticker.map(catalyst_df.set_index('Tickers')['id'].to_dict())
        final_df["isOTC"] = final_df.Ticker.apply(
            lambda t: "Yes" if yf.Ticker(t).info["exchange"] == "PNK" else "No")
        final_df["Rating"] = final_df.Ticker.map(
            dd_df.set_index('Tickers')['rating'].to_dict())
        final_df["Author Reliability"] = final_df.Ticker.map(
            dd_df.set_index('Tickers')['credibility'].to_dict())
        final_df["Author Reliability"] = final_df["Author Reliability"].apply(
            lambda x: round(x, 2) if x != "N/A" else "N/A")
        final_df["Comment Sentiment"] = final_df.Ticker.map(
            dd_df.set_index('Tickers')['sentiment'].to_dict())
        final_df.fillna("N/A", inplace=True)
        return final_df

    def get_data(self, withFinance=False, withStats=False):
        df_posts = self.scrape_posts()
        data_df = self.TickersFromPosts(df_posts)

        if withFinance:
            data_df = self.getFinanceData(data_df)
        if withStats:
            data_df = self.dataWithStats(data_df, df_posts)

        return data_df
