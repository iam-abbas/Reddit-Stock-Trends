<h1 align="center">Reddit Stock Trends 📈</h1>

<p align="center">
See trending stock tickers on Reddit and check Stock perfomance <br><br>
<img style="padding:10px;" src="https://img.shields.io/badge/Open%20Source-💕%20-9cf?style=for-the-badge"><br>
<img style="padding:10px;" src="https://img.shields.io/github/contributors/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/stars/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/forks/iam-abbas/Reddit-Stock-Trends?label=Forks&style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/license/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/iam-abbas/Reddit-Stock-Trends?style=flat-square">

</p>

## Usage

#### Reddit API
- Get your reddit API credentials from [here](https://www.reddit.com/prefs/apps)
- Follow [this](https://towardsdatascience.com/scraping-reddit-with-praw-76efc1d1e1d9) article to get your credentials.

#### Running Scripts
- Go to `src/` directory.
- Create a `praw.ini` file with the following
```
[ClientSecrets]
client_id=<your client id>
client_secret=<your client secret>
user_agent=<your user agent>
```
Note that the title of this section, `ClientSecrets`, is important because `ticker_counts.py` will specifically look for that title in the `praw.ini` file.
- Install required modules using `pip install -r requirements.txt`
- Run `ticker_counts.py` first
- Now run `yfinance_analysis.py`
- You will be able to find your results in `data/` directory.

#### Ticker Symbol API - EOD Historical Data
Included for potential future use is a csv file that contains all the listed ticker symbols for stocks, ETFs, and
mutual funds (~50,000 tickers). This was retrieved from https://eodhistoricaldata.com/. You can register for a free api key and get up to 20 api calls every 24 hours.

To retrieve a csv of all USA ticker symbols, use the following:

https://eodhistoricaldata.com/api/exchange-symbol-list/US?api_token={YOUR_API_KEY}

## Contribution 
I would love to see more work done on this, I think this could be something very useful at some point. All contributions are welcome. Go ahead and open a PR.
- Join the [Discord](https://discord.gg/USsBfc97RM) to discuss development and suggestions.

<a href="https://discord.gg/USsBfc97RM" ><img src="https://preview.redd.it/tpvewx1950311.png?width=1487&format=png&auto=webp&s=be429e3b5e7e51c777497c95b63c5011f9a906b6" width="150px"></a>


### To Do
See [this](https://github.com/iam-abbas/Reddit-Stock-Trends/labels/feature) page.

Suggestions are appreciated.

### Donation
If you like what I am doing, consider buying me a coffee this helps me give more time to this project and improve. <br><br>
<a href="https://www.buymeacoffee.com/abbas" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

----

If you decide to use this anywhere please give a credit to [@abbasmdj](https://twitter.com/abbasmdj) on twitter, also If you like my work, check out other projects on my [Github](https://github.com/iam-abbas) and my [personal blog](https://abbasmj.com).
