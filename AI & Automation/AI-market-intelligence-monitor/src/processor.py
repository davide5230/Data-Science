def normalize_article(article):
    return {
        "article_id": article.get("id"),
        "title": article.get("title"),
        "description": article.get("description"),
        "source": article.get("host"),
        "published_at": article.get("published_at"),
        "language": article.get("lang"),
        "url": article.get("url")
    }


def normalize_articles(articles):
    return [
        normalize_article(article)
        for article in articles
    ]
