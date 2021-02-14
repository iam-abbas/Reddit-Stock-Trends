import StockTrends

scraper = StockTrends.StockTrends()

# def get_data (with_finance=False, with_stats=False)
data = scraper.get_data()


print(data)
