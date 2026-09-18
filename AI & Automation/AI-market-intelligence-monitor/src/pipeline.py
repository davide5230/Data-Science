from collector import fetch_articles
from processor import process_articles
from analyzer import analyze_articles
from reporter import generate_market_report


def run_pipeline(
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

    report = generate_market_report(
        analyses
    )

    return report

if __name__ == "__main__":

    keywords = [
        "artificial intelligence",
        "AI",
        "machine learning",
        "generative AI",
        "LLM"
    ]

    report = run_pipeline(
        query="artificial intelligence",
        keywords=keywords,
        size=20
    )

    print(
        report.model_dump_json(
            indent=2
        )
    )
