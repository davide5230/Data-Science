from metrics import calculate_statistics
from collector import fetch_articles
from processor import process_articles
from analyzer import analyze_articles
from reporter import generate_market_report
from storage import (
    init_database,
    save_report
)


def run_pipeline(
    init_database()
    query,
    keywords,
    size=20,
    language="en"
):
    data = fetch_articles(
        query=query,
        size=size
    )

    raw_articles = data.get(
        "results",
        []
    )

    processed_articles = process_articles(
        raw_articles,
        language=language,
        keywords=keywords
    )
    
    analyses = analyze_articles(
        processed_articles
        )
    
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

    print("\nSTATISTICS")
    print(
        result["statistics"]
    )

    print("\nMARKET INTELLIGENCE REPORT")
    print(
        result["report"].model_dump_json(
            indent=2
        )
    )
