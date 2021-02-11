import sys
from datetime import datetime

import pandas as pd
import yfinance as yf


class FinanceAnalysis:

    def analyze(self, best_n=25):
        # Load data from file, generate data by running the `ticker_counts.py` script
        date_created = datetime.today().strftime('%Y-%m-%d')
        filename = f'{date_created}_tick_df'
        data_directory = './data'

        input_path = f'{data_directory}/{filename}.csv'

        df_tick = pd.read_csv(input_path).sort_values(by=['Mentions', 'Ticker'], ascending=False)
        df_tick.dropna(axis=1)

        columns = ['Name', 'Industry', 'Previous Close', '5d Low', '5d High', '1d Change (%)', '5d Change (%)',
                   '1mo Change (%)']
        df_best = df_tick.head(best_n)
        df_best[columns] = df_best['Ticker'].apply(self.get_ticker_info)

        # Save to file to load into yahoo analysis script
        filename = f'df_best_{best_n}'
        output_path = f'{data_directory}/{filename}.csv'

        df_best.to_csv(output_path, index=False)
        print(df_best.head())

    def calculate_change(self, start: float, end: float) -> float:
        """Use Yahoo Finance API to get the relevant data."""
        return round(((end - start) / start) * 100, 2)

    def get_change(self, ticker: str, period: str = '1d') -> float:
        return self.calculate_change(
            yf.Ticker(ticker).history(period)['Open'].to_list()[0],
            yf.Ticker(ticker).history(period)['Close'].to_list()[-1]
        )

    def get_ticker_info(self, ticker):
        # Standard Data
        info = yf.Ticker(ticker).info
        ticker_name = info.get('longName')
        ticker_industry = info.get('industry')

        # previous Day close
        ticker_close = yf.Ticker(ticker).history(period='1d')['Close'].to_list()[-1]

        # Highs and Lows
        high_low = yf.Ticker(ticker).history(period='5d')
        low5d = min(high_low['Low'].to_list())
        high5d = max(high_low['High'].to_list())

        # Changes
        change1d = self.get_change(ticker)
        change5d = self.get_change(ticker, '5d')
        change1mo = self.get_change(ticker, '1mo')

        return pd.Series([ticker_name, ticker_industry, ticker_close, low5d, high5d, change1d, change5d, change1mo])


if __name__ == '__main__':
    analyzer = FinanceAnalysis()
    if len(sys.argv) > 1:
        analyzer.analyze(int(sys.argv[1]))
    else:
        analyzer.analyze()
