from flask import Blueprint, render_template, request
from app.services.news_service import NewsService
from app.models.article import Article

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form.get("topic")

        articles_newsapi = NewsService.fetch_from_newsapi(topic)
        articles_gnews = NewsService.fetch_from_gnews(topic)
        
        all_articles = articles_newsapi + articles_gnews
        NewsService.save_articles(topic, all_articles)

    stored_articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("index.html", articles=stored_articles)
