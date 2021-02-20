<h1 align="center">Reddit Stock Trends 📈</h1>

<p align="center">
See trending stock tickers on Reddit and check Stock perfomance <br><br>
<img style="padding:10px;" src="https://img.shields.io/github/contributors/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/stars/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/forks/iam-abbas/Reddit-Stock-Trends?label=Forks&style=flat-square">
<img style="padding:10px;" src="https://img.shields.io/github/license/iam-abbas/Reddit-Stock-Trends?style=flat-square">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/iam-abbas/Reddit-Stock-Trends?style=flat-square">

</p>

## Backend

### Reddit API

- Get your reddit API credentials from [here](https://www.reddit.com/prefs/apps).
- Follow [this](https://towardsdatascience.com/scraping-reddit-with-praw-76efc1d1e1d9) article to get your credentials.
- Go to `back/` directory.
- Create a `praw.ini` file with the following

```
[ClientSecrets]
client_id=<your client id>
client_secret=<your client secret>
user_agent=<your user agent>
```

Note that the title of this section, `ClientSecrets`, is important because `ticker_counts.py` will specifically look for that title in the `praw.ini` file.

### Local usage

- Install required modules using `pip install -r requirements.txt`.
- Run `ticker_counts.py` first.
- Now run `yfinance_analysis.py`.
- You will be able to find your results in `data/` directory.
- [Optional] Run `wsgi.py` to start a server that returns the data in JSON format. This step will generate the csv files if they don't already exist.

### Docker usage

- Requires Docker 17.09.0+ and docker-compose 1.17.0+
- Run `docker-compose up backend` to generate csv files and start the backend sever.

---

## Frontend - Vue

There's also a JavaScript web app that shows some data visualizations.

### Local usage

Start the local server. This server will generate the csv files if they don't already exist.

```bash
cd back
python wsgi.py
```

Then, launch the client

```bash
cd front
cp .env.example .env
npm install
npm run serve
```

You can change the env variables if you need to

### Docker usage

- Requires Docker 17.09.0+ and docker-compose 1.17.0+
- Run `docker-compose up frontend` and navigate to http://localhost:8080/. This requires the backend server to already be running. If the backend is not running, run ` docker-compose up` to start both services.

---

## Frontend - React

There's also a React JavaScript web app that has +3 more features than the vue app.

- shows all available data on one site/table
- you can sort the data by clicking the header name, if you want see what ticker had the most 5d Change for example
- the tickername is a direct link to the tradeview overview site for the ticker if you find a ticker interesting and want to analyse it

### Local usage

Start the local server. This server will generate the csv files if they don't already exist.

```bash
cd back
python wsgi.py
```

Then, launch the client

```bash
cd react-front
cp .env.example .env
npm install
npm start
```

You can change the env variables if you need to

**No Docker solution for the react app.**

---

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

---

If you decide to use this anywhere please give a credit to [@abbasmdj](https://twitter.com/abbasmdj) on twitter, also If you like my work, check out other projects on my [Github](https://github.com/iam-abbas) and my [personal blog](https://abbasmj.com).
