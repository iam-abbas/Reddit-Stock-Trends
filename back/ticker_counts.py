import configparser
import json
import pandas as pd
import praw
import re
import os
import yfinance as yf

from collections import Counter
from functools import reduce
from operator import add
from typing import Set
from datetime import datetime
from tqdm import tqdm


# JB 02/07/2021 - Configparser introduced to scrape out some hardcode and allow removal of sensitive passwords

WEBSCRAPER_LIMIT = 2000

config = configparser.ConfigParser()
config.read('./config/config.ini')



stop_words = json.loads(config['FilteringOptions']['StopWords'])
block_words = json.loads(config['FilteringOptions']['BlockWords'])


with open('./config/tickers.json') as tickerFile:
    tickerList = json.load(tickerFile)


# Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
# Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
reddit = praw.Reddit('ClientSecrets')
subreddits = "+".join(json.loads(config['FilteringOptions']['Subreddits']))
new_bets = reddit.subreddit(subreddits).new(limit=WEBSCRAPER_LIMIT)

posts = [[post.id,
          post.title,
          post.score,
          post.num_comments,
          post.upvote_ratio,
          post.total_awards_received] for post in tqdm(new_bets, desc="Selecting relevant data from webscraper", total=WEBSCRAPER_LIMIT)]
posts = pd.DataFrame(posts, columns=["id",
                                     "title",
                                     "score",
                                     "comments",
                                     "upvote_ratio",
                                     "total_awards"])


def verify_ticker(tic):
    try:
        if tickerList[tic]:
            return True
    except:
        pass
    return False


def extract_ticker(body: str, re_string: str = "[$][A-Za-z]*|[A-Z][A-Z]{1,}") -> Set[str]:
    """Simple Regex to get tickers from text."""
    ticks = set(re.findall(re_string, str(body)))
    res = set()
    for item in ticks:
        if item not in block_words and item.lower() not in stop_words and item:
            try:
                tic = item.replace("$", "").upper()
                res.add(tic)
            except Exception as e:
                print(e)
    return res


# Extract tickers from all titles and create a new column
posts["Tickers"] = posts["title"].apply(extract_ticker)
ticker_sets = posts.Tickers.to_list()

# Count number of occurances of the Ticker and verify id the Ticker exists
counts = reduce(add, map(Counter, ticker_sets))

verified_tics = {}
for ticker, ticker_count in tqdm(counts.items(), desc="Filtering verified ticks"):
    # If ticker is found more than 3 times and ticker is valid
    if ticker_count > 3 and verify_ticker(ticker):
        verified_tics[ticker] = ticker_count


# Create Datable of just mentions
tick_df = pd.DataFrame(verified_tics.items(), columns=["Ticker", "Mentions"])
tick_df.sort_values(by=["Mentions"], inplace=True, ascending=False)
tick_df.reset_index(inplace=True, drop=True)

date_created = datetime.today().strftime('%Y-%m-%d')
csv_filename = f"{date_created}_tick_df"
directory_output = "./data"

if not os.path.exists(directory_output):
    os.mkdir(directory_output)

full_output_path = f"{directory_output}/{csv_filename}.csv"

with open(full_output_path, "w+") as file:  # Use file to refer to the file object
    # Save to file to load into yahoo analysis script
    tick_df.to_csv(full_output_path, index=False)
    print(tick_df.head())
