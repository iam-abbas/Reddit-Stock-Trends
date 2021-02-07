import yfinance as yf
import pandas as pd

BEST_N = 25  # The first N stocks, ordered by number of mentions


def calculate_change(start: float, end: float) -> float:
    """Use Yahoo Finance API to get the relevent data."""
    return round(((end - start) / start) * 100, 2)


def get_change(ticker: str, period: str = "1d") -> float:
    return calculate_change(yf.Ticker(ticker).history(period)["Open"].to_list()[0],
                            yf.Ticker(ticker).history(period)["Close"].to_list()[-1])


# Load data from file, generate data by running the `ticker_counts.py` script
tick_df = pd.read_csv("./data/tick_df.csv").sort_values(by=["Mentions", "Ticker"], ascending=False)
tick_df.dropna(axis=1)

df_best = tick_df.head(BEST_N)
df_best["Name"] = df_best.Ticker.apply(lambda x: yf.Ticker(x).info["longName"])
df_best["Bid"] = df_best.Ticker.apply(lambda x: yf.Ticker(x).info["previousClose"])
df_best["5d Low"] = df_best.Ticker.apply(lambda x: min(yf.Ticker(x).history(period="5d")["Low"].to_list()))
df_best["5d High"] = df_best.Ticker.apply(lambda x: max(yf.Ticker(x).history(period="5d")["High"].to_list()))
df_best["1d Change (%)"] = df_best.Ticker.apply(get_change)
df_best["5d Change (%)"] = df_best.Ticker.apply(lambda x: get_change(x, "5d"))
df_best["1mo Change (%)"] = df_best.Ticker.apply(lambda x: get_change(x, "1mo"))
df_best["Industry"] = df_best.Ticker.apply(lambda x: yf.Ticker(x).info["industry"])

df_best.rename(columns={"Bid ":  "Price - 2/5"}, inplace=True)
df_best.to_csv(f"./data/df_best_{BEST_N}.csv", index=False)  # Save to file to load into yahoo analysis script
print(df_best.head())
