from collector import fetch_articles
from processor import process_articles
from analyzer import analyze_articles


def run_pipeline(
    query,
    keywords,
    size=20,
    language="en"
):
    # Step 1: collect raw news
    data = fetch_articles(
        query=query,
        size=size
    )

    raw_articles = data.get(
        "results",
        []
    )

    # Step 2: clean and filter
    processed_articles = process_articles(
        raw_articles,
        language=language,
        keywords=keywords
    )

    # Step 3: AI analysis
    analyses = analyze_articles(
        processed_articles
    )

    return analyses
