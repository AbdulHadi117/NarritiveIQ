"""
bias_service.py

Implements analytical computations used to estimate narrative bias and
sentiment divergence across different news sources.

This module operates on the processed dataset (Article records enriched
with sentiment scores) and derives aggregate metrics that are used for:

- Source-level sentiment comparison
- Bias index estimation
- Narrative polarization measurement
- Dashboard visualizations

Position in Pipeline:
    External APIs → Sentiment Processing → Database Storage → Bias Analytics → Visualization

The metrics produced here do not represent absolute political bias,
but rather relative sentiment variation across sources for a given topic.
"""

from collections import defaultdict
import statistics


class BiasService:
    """
    BiasService

    Provides static analytical utilities for computing aggregate sentiment
    statistics across news sources.

    These metrics help quantify how differently various sources portray
    the same topic.
    """

    @staticmethod
    def compute_source_metrics(articles):
        """
        Compute average sentiment statistics per news source.

        Aggregates sentiment scores from the article dataset and groups
        them by source to produce summary metrics.

        Args:
            articles (list[Article]):
                List of Article model instances containing sentiment scores.

        Returns:
            list[dict]:
                A list of source-level metrics where each item contains:
                    - source (str): Source name
                    - avg_sentiment (float): Average sentiment polarity
                    - article_count (int): Number of contributing articles

        Notes:
            Articles without sentiment scores are ignored to ensure
            statistical validity.
        """

        # Group sentiment scores by source
        source_score = defaultdict(list)

        for article in articles:
            if article.sentiment_score is not None:
                source_score[article.source].append(article.sentiment_score)

        # Compute aggregate metrics per source
        source_metrics = []
        for source, scores in source_score.items():
            avg = sum(scores) / len(scores)

            source_metrics.append({
                'source': source,
                'avg_sentiment': round(avg, 3),
                'article_count': len(scores)
            })

        return source_metrics

    @staticmethod
    def compute_bias_index(source_metrics):
        """
        Compute Bias Index across sources.

        The bias index represents the sentiment spread between the most
        positive and most negative sources for a given dataset.

        Formula:
            bias_index = max(avg_sentiment) - min(avg_sentiment)

        Args:
            source_metrics (list[dict]): Output from compute_source_metrics().

        Returns:
            float:
                Numeric value representing sentiment deviation across sources.

        Interpretation:
            Higher values indicate stronger narrative divergence.
        """

        if not source_metrics:
            return 0.0

        values = [s['avg_sentiment'] for s in source_metrics]

        return round(max(values) - min(values), 3)

    @staticmethod
    def compute_polarization(source_metrics):
        """
        Compute Narrative Polarization Score.

        Uses statistical standard deviation of source sentiment averages
        to estimate how polarized narrative tones are across sources.

        Args:
            source_metrics (list[dict]): Output from compute_source_metrics().

        Returns:
            float:
                Standard deviation of sentiment distribution.

        Interpretation:
            Higher values indicate greater narrative polarization.
        """

        if len(source_metrics) < 2:
            return 0.0

        values = [s['avg_sentiment'] for s in source_metrics]

        return round(statistics.stdev(values), 3)