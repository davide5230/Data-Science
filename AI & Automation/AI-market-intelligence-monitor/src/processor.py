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


def filter_articles(
    articles,
    language="en"
):
    filtered_articles = []

    for article in articles:

        if not article["title"]:
            continue

        if not article["description"]:
            continue

        if article["language"] != language:
            continue

        filtered_articles.append(article)

    return filtered_articles


def deduplicate_articles(articles):
    unique_articles = []

    seen_urls = set()

    for article in articles:

        url = article["url"]

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        unique_articles.append(article)

    return unique_articles


def process_articles(
    raw_articles,
    language="en"
):
    articles = normalize_articles(
        raw_articles
    )

    articles = filter_articles(
        articles,
        language=language
    )

    articles = deduplicate_articles(
        articles
    )

    return articles
