from analyzer import analyze_articles
from collector import fetch_articles
from logger import logger
from metrics import calculate_statistics
from processor import process_articles
from reporter import generate_market_report
from storage import (
    get_seen_article_ids,
    init_database,
    save_report,
    save_seen_articles
)


EMPTY_STATISTICS = {
    "total_articles": 0,
    "importance": {},
    "categories": {},
    "companies": {}
}


def run_pipeline(
    query,
    keywords,
    size=20,
    language="en"
):
    logger.info(
        "Pipeline started for query: %s",
        query
    )

    init_database()

    data = fetch_articles(
        query=query,
        size=size
    )

    raw_articles = data.get(
        "results",
        []
    )

    logger.info(
        "Collected %s raw articles.",
        len(raw_articles)
    )

    processed_articles = process_articles(
        raw_articles,
        language=language,
        keywords=keywords
    )

    logger.info(
        "Processed %s articles.",
        len(processed_articles)
    )

    seen_article_ids = get_seen_article_ids()

    new_articles = [
        article
        for article in processed_articles
        if article["article_id"] not in seen_article_ids
    ]

    logger.info(
        "Found %s new articles.",
        len(new_articles)
    )

    if not new_articles:
        logger.info(
            "No new articles found."
        )
        return {
            "statistics": EMPTY_STATISTICS.copy(),
            "report": None
        }

    analyses = analyze_articles(
        new_articles
    )

    logger.info(
        "Generated %s analyses.",
        len(analyses)
    )

    if not analyses:
        logger.warning(
            "No analyses were generated."
        )
        return {
            "statistics": EMPTY_STATISTICS.copy(),
            "report": None
        }

    statistics = calculate_statistics(
        analyses
    )

    report = generate_market_report(
        analyses
    )

    save_report(
        query=query,
        statistics=statistics,
        report=report
    )

    analyzed_article_ids = {
        analysis.article_id
        for analysis in analyses
    }

    successfully_analyzed_articles = [
        article
        for article in new_articles
        if article["article_id"] in analyzed_article_ids
    ]

    save_seen_articles(
        successfully_analyzed_articles
    )

    logger.info(
        "Report generated and saved successfully."
    )

    return {
        "statistics": statistics,
        "report": report
    }


if __name__ == "__main__":
    keywords = [
        "artificial intelligence",
        "AI",
        "machine learning",
        "generative AI",
        "LLM"
    ]

    result = run_pipeline(
        query="artificial intelligence",
        keywords=keywords,
        size=20
    )

    if result["report"] is not None:
        print(
            "\nMARKET INTELLIGENCE REPORT"
        )
        print(
            result["report"].model_dump_json(
                indent=2
            )
        )
    else:
        print(
            "\nNo new articles to report."
        )
