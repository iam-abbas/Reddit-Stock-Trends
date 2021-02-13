import StockTrends

scraper = StockTrends.StockTrends()

data = scraper.get_data()


print(data)
