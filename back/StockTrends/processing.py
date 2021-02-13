from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from . import main_utils

class DataProcessor:

    def __init__(self, NLP=False, cuda=False):
        self.ScraperUtils = main_utils.ScraperUtils()
        if NLP:
            tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            model = AutoModelForSequenceClassification.from_pretrained(
                "ProsusAI/finbert")
            device = -1 if not cuda else 0
            self.nlp_model = pipeline('sentiment-analysis', model=model,
                                      tokenizer=tokenizer, return_all_scores=True, device=0)
        else:
            self.nlp_model = None

    def userCredibility(self, author):
        linkKarma = author.link_karma
        commentKarma = author.comment_karma
        isVerified = 1 if author.has_verified_email else 0.2
        suspicious = 1
        currentTickers = []
        for comment in author.comments.new(limit=10):
            tickers = list(self.ScraperUtils.extract_ticker(comment.body))
            for ticker in tickers:
                if self.ScraperUtils.isTickerValid(ticker):
                    if ticker in currentTickers or ticker.lower() in comment.body.lower():
                        suspicious -= 0.1
                    else:
                        suspicious += 0.1
                currentTickers.append(ticker)
        karmaPower = ((linkKarma*1.1)+(commentKarma*1.25))/2000
        userMeasure = karmaPower*isVerified*suspicious
        return userMeasure

    def postRating(self, post):
        comments = post.num_comments
        upvotes = post.score
        awards = post.total_awards_received
        upvoteRatio = post.upvote_ratio
        rating = ((comments*1.1)+(upvotes*0.9)+(awards*2))*upvoteRatio
        return rating

    def commentSentiment(self, post, limit=10):
        if not self.nlp_model:
            return "No Analysis"
        count = 0
        sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
        comments = post.comments.list()[:4]
        if len(comments) <= 3:
            return 'Insufficient Comments'
        for comment in post.comments:
            if count == limit:
                break
            if 'upvote' in comment.body or 'bot' in comment.body:
                continue
            try:
                commentSentiment = self.nlp_model(comment.body)
            except:
                continue
            commentSentiment = dict((data['label'], data['score'])
                                    for data in commentSentiment[0])
            for label in sentiments:
                sentiments[label] += commentSentiment[label]
            count += 1
        if count <= 5:
            score = (sentiments['positive'] + sentiments['neutral'] / 2.2
                     - sentiments['negative']) / count * 90
        else:
            score = (sentiments['positive'] + sentiments['neutral'] / 1.8
                     - sentiments['negative']) / count * 100
        verdict = 'N/A'
        verdict_range = {
            '0-20': 'Negative',
            '20-30': 'Mostly Negative',
            '30-45': 'Neutral',
            '45-65': 'Mostly Positive',
            '65-80': 'Positive',
            '80-101': 'Very Positive',
        }
        for vrange in verdict_range:
            vrange = [int(x) for x in vrange.split('-')]
            if score >= vrange[0] and score <= vrange[1]:
                verdict = verdict_range['-'.join([str(l) for l in vrange])]
        print(post.id, verdict)
        return verdict
