from textblob import TextBlob

class SentimentService:

    @staticmethod
    def analyze_sentiment(text):
        if not text:
            return 0.0, "Neutral"
        
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity

        if score > 0.1:
            label = "Positive"
        elif score < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return score.round(2), label