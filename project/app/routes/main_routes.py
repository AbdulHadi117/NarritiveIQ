"""
main_routes.py

Defines the primary application routes for NarrativeIQ.

This module acts as the orchestration layer between:
- User interactions (frontend templates)
- Data ingestion services (news APIs)
- Analytical processing services (sentiment & bias computation)
- Database storage (Article model)

Routes in this module manage the high-level workflow of the system:
    Topic Input → Data Collection → NLP Processing → Bias Analytics → Visualization
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.services.news_service import NewsService
from app.models.article import Article
from app.services.bias_service import BiasService


# Blueprint for main application routes
main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    """
    Home Route (Landing Page)

    Handles:
        - Display of the topic input interface
        - Triggering the data ingestion pipeline when a topic is submitted

    Workflow:
        1. User submits a topic.
        2. Articles are fetched from multiple news APIs.
        3. Articles are normalized, enriched with sentiment, and stored.
        4. User is redirected to the dashboard for analytics visualization.

    Returns:
        home.html template for GET requests.
        Redirect to dashboard after POST processing.
    """

    if request.method == "POST":
        topic = request.form.get("topic")

        if topic:
            # Fetch articles from multiple external sources
            articles_newsapi = NewsService.fetch_from_newsapi(topic)
            articles_gnews = NewsService.fetch_from_gnews(topic)

            # Combine datasets and persist processed articles
            combined_articles = articles_newsapi + articles_gnews
            NewsService.save_articles(topic, combined_articles)

        # Redirect to analytics dashboard after data processing
        return redirect(url_for("main.dashboard"))

    return render_template("home.html")


@main.route("/dashboard")
def dashboard():
    """
    Dashboard Route (Analytics View)

    Responsible for:
        - Retrieving stored articles
        - Computing source-level sentiment metrics
        - Computing bias and polarization indicators
        - Passing visualization-ready data to the frontend

    This route represents the analytical core of the NarrativeIQ UI layer.

    Returns:
        dashboard.html template with:
            - Article dataset
            - Bias metrics
            - Chart-ready sentiment distributions
    """

    # Retrieve dataset ordered by latest ingestion time
    stored_articles = Article.query.order_by(
        Article.created_at.desc()
    ).all()

    # Compute analytical metrics from dataset
    source_metrics = BiasService.compute_source_metrics(stored_articles)
    bias_index = BiasService.compute_bias_index(source_metrics)
    polarization = BiasService.compute_polarization(source_metrics)

    return render_template(
        "dashboard.html",
        articles=stored_articles,
        source_metrics=source_metrics,
        bias_index=bias_index,
        polarization=polarization,

        # Data formatted for frontend chart rendering
        chart_labels=[s['source'] for s in source_metrics],
        chart_values=[s['avg_sentiment'] for s in source_metrics]
    )


@main.route("/articles")
def articles():
    """
    Articles Explorer Route

    Displays the stored dataset of processed articles.

    This page allows users to:
        - Inspect collected news data
        - View sentiment classifications per article
        - Understand how analytics are derived from raw inputs

    Returns:
        articles.html template containing all stored articles.
    """

    stored_articles = Article.query.order_by(
        Article.created_at.desc()
    ).all()

    return render_template(
        "articles.html",
        articles=stored_articles
    )


@main.route("/about")
def about():
    """
    About Route

    Static informational page describing:
        - Project motivation
        - Data pipeline architecture
        - NLP methodology
        - External APIs used

    Returns:
        about.html template.
    """
    return render_template("about.html")