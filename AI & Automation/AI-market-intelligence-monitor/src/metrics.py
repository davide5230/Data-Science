from collections import Counter


def calculate_statistics(analyses):

    importance_counter = Counter()
    category_counter = Counter()
    company_counter = Counter()

    for analysis in analyses:

        importance_counter[
            analysis.importance
        ] += 1

        category_counter[
            analysis.category
        ] += 1

        for company in analysis.companies:
            company_counter[
                company
            ] += 1

    return {
        "total_articles": len(analyses),

        "importance": dict(
            importance_counter
        ),

        "categories": dict(
            category_counter
        ),

        "companies": dict(
            company_counter.most_common()
        )
    }
