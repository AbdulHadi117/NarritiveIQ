import requests
from flask import current_app
from app.models.article import Article
from app import db
from datetime import datetime
from app.services.sentiment_service import SentimentService

class NewsService:

    @staticmethod
    def fetch_from_newsapi(topic):
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
        for item in articles:
            if not item['title']:
                continue

            existing = Article.query.filter_by(
                title=item['title'],
            ).first()

            if existing:
                continue

            full_text = f"{item['title']} {item['description']}"
            sentiment_score, sentiment_label = SentimentService.analyze_sentiment(full_text)

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
        db.session.commit()