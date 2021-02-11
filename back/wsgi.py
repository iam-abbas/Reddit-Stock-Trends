from ticker_counts import main as update_reddit_mentions
from yfinance_analysis import main as update_financial_data
from server import app

def main():
    update_reddit_mentions()
    update_financial_data()

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()