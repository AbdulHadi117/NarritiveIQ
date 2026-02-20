from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

class SentimentService:

    @staticmethod
    def analyze_sentiment(text):
        if not text:
            return 0.0, "Neutral"
        
        scores = sia.polarity_scores(text)
        compound = scores['compound']

        if compound > 0.1:
            label = "Positive"
        elif compound < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return round(compound, 2), label