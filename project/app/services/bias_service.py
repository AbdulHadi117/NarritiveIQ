from collections import defaultdict
import statistics

class BiasService:

    @staticmethod
    def compute_source_metrics(articles):
        source_score = defaultdict(list)

        for article in articles:
            if article.sentiment_score is not None:
                source_score[article.source].append(article.sentiment_score)
            
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
        if not source_metrics:
            return 0.0
        
        values = [s['avg_sentiment'] for s in source_metrics]

        return round(max(values) - min(values), 3)
    
    @staticmethod
    def compute_polarization(source_metrics):
        if len(source_metrics) < 2:
            return 0.0
        
        values = [s['avg_sentiment'] for s in source_metrics]

        return round(statistics.stdev(values), 3)
    