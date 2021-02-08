<h1 align="center">Reddit Stock Trends 📈</h1>

<p align="center">
<img style="padding:10px;" src="https://img.shields.io/badge/Open%20Source-💕%20-9cf?style=for-the-badge"><br>
<img style="padding:10px;" src="https://img.shields.io/github/contributors/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/stars/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/forks/iam-abbas/Reddit-Stock-Trends?label=Forks&style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/license/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/iam-abbas/Reddit-Stock-Trends?style=flat-square">

See trending stock tickers on Reddit and check Stock perfomance
</p>

## Usage

#### Reddit API
- Get your reddit API credentials from [here](https://www.reddit.com/prefs/apps)
- Follow [this](https://towardsdatascience.com/scraping-reddit-with-praw-76efc1d1e1d9) article to get your credentials.

#### Running Scripts
- Go to `src/` directory.
- Create a `.env` file and add the following
```
CLIENT_ID=<your client id>
CLIENT_SECRET=<your client secret>
USER_AGENT=<your user agent>
```
- Run `ticker_count.py` first
- Now run `yfinance_analysis.py`
- You will be able to find your results in `data/` directory.


## Contribution
I would love to see more work done on this, I think this could be something very useful at some point. All contributions are welcome. Go ahead and open a PR

### To Do
- [x] Turn it into python executable rather than notebook
- [ ] Turn this into a local module that can be used in notebooks/python scripts
- [ ] Scrape catalysts from DDs
- [ ] Add visualisations 
- [ ] Add time series to figure out at what time did stock trend and what time did posts/comments on reddit spike
- [ ] Scrape comments as well
- [ ] NLP implementation for SA
- [ ] Create a scoring model that takes into account upvotes/comments/awards and mentions

Suggestions are appreciated. 

### Donation
If you like what I am doing, consider buying me a coffee this helps me give more time to this project and improve.
<a href="https://www.buymeacoffee.com/abbas" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

----

If you decide to use this anywhere please give a credit to [@abbasmdj](https://twitter.com/abbasmdj) on twitter, also If you like my work, check out other projects on my [Github](https://github.com/iam-abbas) and my [personal blog](https://abbasmj.com).



