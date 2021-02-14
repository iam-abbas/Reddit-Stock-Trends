import StockTrends

scraper = StockTrends.StockTrends()

# def get_data (with_finance=False)
data = scraper.get_data()


print(data)
