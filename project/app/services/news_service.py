"""
news_service.py

Handles external news data ingestion for NarrativeIQ.

Responsibilities:
    - Fetch news articles from multiple APIs (NewsAPI, GNews)
    - Normalize article data for internal storage
    - Enrich articles with NLP sentiment analysis
    - Persist processed articles into the database

Position in Pipeline:
    User Input (Topic) → NewsService → SentimentService → Database (Article) → BiasService → Visualization

Notes:
    - Each API has its own rate limits and response structures
    - Only English articles are fetched
    - Duplicate titles are skipped to maintain dataset integrity
"""

import requests
from flask import current_app
from app.models.article import Article
from app import db
from datetime import datetime
from app.services.sentiment_service import SentimentService


class NewsService:
    """
    NewsService

    Provides static utilities to fetch, process, and persist news data.
    Acts as the ingestion layer of the NarrativeIQ architecture.
    """

    @staticmethod
    def fetch_from_newsapi(topic):
        """
        Fetch articles from NewsAPI for a given topic.

        Args:
            topic (str): Keyword for searching relevant news articles.

        Returns:
            list[dict]: Normalized list of articles containing:
                - title (str)
                - description (str)
                - source (str)
                - published_at (str ISO timestamp)
        
        Notes:
            - Limits results to 10 articles
            - Only English articles are fetched
        """

        url = "https://newsapi.org/v2/everything"

        params = {
            'q': topic,
            'apiKey': current_app.config['NEWS_API_KEY'],
            'language': 'en',
            'pageSize': 10
        }

        response = requests.get(url, params=params)
        data = response.json()

        articles = []

        if data.get('status') == 'ok':
            for item in data.get('articles', []):
                article = {
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'source': item.get('source', {}).get('name'),
                    'published_at': item.get('publishedAt')                    
                }
                articles.append(article)

        return articles

    @staticmethod
    def fetch_from_gnews(topic):
        """
        Fetch articles from GNews API for a given topic.

        Args:
            topic (str): Keyword for searching relevant news articles.

        Returns:
            list[dict]: Normalized list of articles with:
                - title
                - description
                - source
                - published_at

        Notes:
            - Limits results to 10 articles
            - Only English articles are fetched
        """

        url = 'https://gnews.io/api/v4/search'
        params = {
            'q': topic,
            'token': current_app.config['GNEWS_API_KEY'],
            'lang': 'en',
            'max': 10
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        articles = []

        for item in data.get('articles', []):
            article = {
                'title': item.get('title'),
                'description': item.get('description'),
                'source': item.get('source', {}).get('name'),
                'published_at': item.get('publishedAt')
            }
            articles.append(article)

        return articles

    @staticmethod
    def save_articles(topic, articles):
        """
        Persist fetched articles into the database after NLP enrichment.

        Args:
            topic (str): The search topic used for these articles.
            articles (list[dict]): List of articles fetched from APIs.

        Workflow:
            1. Skip articles without titles
            2. Check for duplicates based on title
            3. Combine title + description for sentiment analysis
            4. Use SentimentService to generate sentiment score & label
            5. Store enriched Article object in database

        Notes:
            - Converts ISO timestamp from API to datetime
            - Commits all valid articles in a single transaction
        """

        for item in articles:
            if not item['title']:
                continue

            # Skip duplicates
            existing = Article.query.filter_by(
                title=item['title'],
            ).first()
            if existing:
                continue

            # Prepare text for sentiment analysis
            full_text = f"{item['title']} {item['description']}"
            sentiment_score, sentiment_label = SentimentService.analyze_sentiment(full_text)

            # Create Article instance
            article = Article(
                title=item["title"],
                description=item["description"],
                source=item["source"],
                topic=topic,
                published_at=datetime.fromisoformat(
                    item["published_at"].replace("Z", "+00:00")
                ) if item["published_at"] else None,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label
            )

            db.session.add(article)

        # Commit all new articles to the database
        db.session.commit()