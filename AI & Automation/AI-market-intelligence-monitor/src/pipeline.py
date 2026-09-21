from logger import logger
from metrics import calculate_statistics
from collector import fetch_articles
from processor import process_articles
from analyzer import analyze_articles
from reporter import generate_market_report
from storage import (
    init_database,
    save_report,
    get_seen_article_ids,
    save_seen_articles
)


def run_pipeline(
    query,
    keywords,
    size=20,
    language="en"
):
    logger.info(
        f"Pipeline started for query: {query}"
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
        f"Collected {len(raw_articles)} raw articles."
    )

    processed_articles = process_articles(
        raw_articles,
        language=language,
        keywords=keywords
    )

    seen_article_ids = get_seen_article_ids()
    
    new_articles = [
        article
        for article in processed_articles
        if article["article_id"]
        not in seen_article_ids
        ]

    logger.info(
        f"Found {len(new_articles)} new articles."
    )

    logger.info(
        f"Processed {len(processed_articles)} articles."
    )

    analyses = analyze_articles(
        new_articles
    )

    save_seen_articles(
        new_articles
    )

    logger.info(
        f"Generated {len(analyses)} analyses."
    )

    statistics = calculate_statistics(
        analyses
    )

    if not analyses:
        logger.info(
            "No new articles found. "
            "Pipeline completed without generating a report."
            )

    return {
        "statistics": {
            "total_articles": 0,
            "importance": {},
            "categories": {},
            "companies": {}
            },
        "report": None
        }
    
    report = generate_market_report(
        analyses
    )

    save_report(
        query=query,
        statistics=statistics,
        report=report
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
        print("\nMARKET INTELLIGENCE REPORT")
        print(
            result["report"].model_dump_json(
                indent=2
                )
            )
    else:
        print(
            "\nNo new articles to report."
            )
