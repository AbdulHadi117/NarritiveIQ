from app import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    source = db.Column(db.String(100))
    topic = db.Column(db.String(100))
    sentiment_score = db.Column(db.Float)
    sentiment_label = db.Column(db.String(20))
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
