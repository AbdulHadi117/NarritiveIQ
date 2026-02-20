"""
article.py

Defines the Article database model used to store processed news data
within the NarrativeIQ pipeline.

Each record represents a normalized news article fetched from external
news APIs (e.g., NewsAPI, GNews) and enriched with NLP-derived metadata
such as sentiment score and sentiment label.

This model acts as the central storage structure connecting:
- Data ingestion (API services)
- NLP processing (sentiment analysis)
- Bias analytics (source-level metrics)
- Frontend visualization (dashboard and article explorer)
"""

from app import db
from datetime import datetime


class Article(db.Model):
    """
    Article Model

    Stores metadata and analytical attributes for each collected news article.

    Fields:
        id (int): Primary key identifier for the article.
        title (str): Headline of the article (required).
        description (str): Short summary or excerpt of the article.
        source (str): News source or publisher name.
        topic (str): Topic keyword used during data collection.
        sentiment_score (float): Numeric sentiment polarity score (-1 to 1).
        sentiment_label (str): Sentiment classification (Positive, Neutral, Negative).
        published_at (datetime): Original publication timestamp from the source.
        created_at (datetime): Timestamp when the record was stored locally.

    Role in System:
        This model functions as the structured dataset layer for:
        - Source sentiment aggregation
        - Bias index computation
        - Dashboard analytics visualization
    """

    id = db.Column(db.Integer, primary_key=True)

    # Article headline fetched from external APIs
    title = db.Column(db.Text, nullable=False)

    # Short summary or description provided by the news source
    description = db.Column(db.Text)

    # Publisher or source name (e.g., BBC, CNN)
    source = db.Column(db.String(100))

    # Topic keyword used for querying articles (e.g., "AI", "Elections")
    topic = db.Column(db.String(100))

    # Sentiment polarity score computed by NLP engine (VADER)
    sentiment_score = db.Column(db.Float)

    # Sentiment classification label derived from the polarity score
    sentiment_label = db.Column(db.String(20))

    # Original publication timestamp from the news provider
    published_at = db.Column(db.DateTime)

    # Timestamp representing when the record was inserted into the database
    created_at = db.Column(db.DateTime, default=datetime.utcnow)