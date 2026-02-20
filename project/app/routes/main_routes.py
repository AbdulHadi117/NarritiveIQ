from flask import Blueprint, render_template, request, redirect, url_for
from app.services.news_service import NewsService
from app.models.article import Article
from app.services.bias_service import BiasService

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        topic = request.form.get("topic")

        if topic:
            articles_newsapi = NewsService.fetch_from_newsapi(topic)
            articles_gnews = NewsService.fetch_from_gnews(topic)

            combined_articles = articles_newsapi + articles_gnews
            NewsService.save_articles(topic, combined_articles)

        return redirect(url_for("main.dashboard"))

    return render_template("home.html")

@main.route("/dashboard")
def dashboard():

    stored_articles = Article.query.order_by(
        Article.created_at.desc()
    ).all()

    source_metrics = BiasService.compute_source_metrics(stored_articles)
    bias_index = BiasService.compute_bias_index(source_metrics)
    polarization = BiasService.compute_polarization(source_metrics)

    return render_template(
        "dashboard.html",
        articles=stored_articles,
        source_metrics=source_metrics,
        bias_index=bias_index,
        polarization=polarization,
        chart_labels=[s['source'] for s in source_metrics],
        chart_values=[s['avg_sentiment'] for s in source_metrics]
    )

@main.route("/articles")
def articles():

    stored_articles = Article.query.order_by(
        Article.created_at.desc()
    ).all()

    return render_template(
        "articles.html",
        articles=stored_articles
    )

@main.route("/about")
def about():
    return render_template("about.html")