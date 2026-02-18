from flask import Blueprint, render_template, request
from app.services.news_service import NewsService
from app.models.article import Article

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form.get("topic")

        articles = NewsService.fetch_from_newsapi(topic)
        NewsService.save_articles(topic, articles)

    stored_articles = Article.query.order_by(Article.created_at.desc()).all()

    return render_template("index.html", articles=stored_articles)
