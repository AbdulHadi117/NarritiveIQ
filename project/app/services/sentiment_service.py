"""
sentiment_service.py

Provides sentiment analysis utilities for NarrativeIQ.

Responsibilities:
    - Compute sentiment polarity for news articles
    - Generate both numeric sentiment scores and categorical labels
    - Serve as the NLP layer connecting data ingestion (NewsService)
      to analytics (BiasService and Dashboard visualizations)

Implementation Notes:
    - Uses NLTK's VADER SentimentIntensityAnalyzer
    - Labels are determined using compound score thresholds:
        Positive: compound > 0.1
        Negative: compound < -0.1
        Neutral: otherwise

Position in Pipeline:
    Article Text → SentimentService → Sentiment Score & Label → Database Storage → Bias Metrics → Dashboard
"""

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer (pre-trained)
sia = SentimentIntensityAnalyzer()


class SentimentService:
    """
    SentimentService

    Provides static NLP utilities for analyzing text sentiment.
    """

    @staticmethod
    def analyze_sentiment(text):
        """
        Analyze the sentiment of a given text.

        Args:
            text (str): Text to be analyzed (e.g., article title + description).

        Returns:
            tuple:
                - sentiment_score (float): Compound sentiment score (-1.0 to 1.0)
                - sentiment_label (str): Categorical label ("Positive", "Neutral", "Negative")

        Workflow:
            1. Handle empty or None text by returning neutral score
            2. Compute VADER polarity scores
            3. Determine compound score
            4. Assign categorical label based on threshold
        """

        if not text:
            return 0.0, "Neutral"

        # Compute sentiment scores
        scores = sia.polarity_scores(text)
        compound = scores['compound']

        # Determine label based on compound score
        if compound > 0.1:
            label = "Positive"
        elif compound < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return round(compound, 2), label