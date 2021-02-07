import re
from collections import Counter
from functools import reduce
from operator import add
from typing import Set

import pandas as pd
import praw
import yfinance as yf
from tqdm import tqdm

WEBSCRAPER_LIMIT = 2_000
CLIENT_ID = "9Aq-wTeGLJBKsQ"
CLIENT_SECRET = "EclWNx5qOyIZLiRkd10Oln0iNPUXvQ"
USER_AGENT = "ScrapeStocks"

# Stop words and Blacklist containing jargon/acronyms
# I added GME and AMC in there lmao, tired of seeing those
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "you're", "you've", "you'll", "you'd", "your", "yours",
              "yourself", "yourselves", "he", "him", "his", "himself", "she", "she's", "her", "hers", "herself", "it", "it's", "its",
              "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "that'll",
              "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
              "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
              "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from",
              "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when",
              "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
              "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should", "should've",
              "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't", "didn", "didn't", "doesn",
              "doesn't", "hadn", "hadn't", "hasn", "hasn't", "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "must",
              "mustn", "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't",
              "won", "won't", "wouldn", "wouldn't"]
block_words = ["DIP", "", "$", "RH", "YOLO", "PORN", "BEST", "MOON", "HOLD", "FAKE", "WISH", "USD", "EV", "MARK", "RELAX", "LOL", "LMAO",
               "LMFAO", "EPS", "DCF", "NYSE", "FTSE", "APE", "CEO", "CTO", "FUD", "DD", "AM", "PM", "FDD", "EDIT", "TA", "UK", "AMC", "GME"]


# Scrape subreddits `r/robinhoodpennystocks` and `r/pennystocks`
# Current it does fetch a lot of additional data like upvotes, comments, awards etc but not using anything apart from title for now
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)
new_bets = reddit.subreddit("robinhoodpennystocks+pennystocks").new(limit=WEBSCRAPER_LIMIT)

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


# Extract tickers from all titles and creae a new column
posts["Tickers"] = posts["title"].apply(extract_ticker)
ticker_sets = posts.Tickers.to_list()

# Count number of occurances of the Ticker and verify id the Ticker exists
counts = reduce(add, map(Counter, ticker_sets))

verified_tics = {}
for ticker, ticker_count in tqdm(counts.items(), desc="Filtering verified ticks"):
    if ticker_count > 3:  # If ticker is found more than 3 times
        try:
            _ = yf.Ticker(ticker).info
            verified_tics[ticker] = ticker_count
        except KeyError:  # Non-existant ticker
            pass

# Create Datable of just mentions
tick_df = pd.DataFrame(verified_tics.items(), columns=["Ticker", "Mentions"])
tick_df.sort_values(by=["Mentions"], inplace=True, ascending=False)
tick_df.reset_index(inplace=True, drop=True)

tick_df.to_csv("./data/tick_df.csv", index=False)  # Save to file to load into yahoo analysis script
print(tick_df.head())
