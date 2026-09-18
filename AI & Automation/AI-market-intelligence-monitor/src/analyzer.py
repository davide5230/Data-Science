from ollama import chat

from schemas import ArticleAnalysis


MODEL_NAME = "qwen3.5:4b"


def analyze_article(article):

    prompt = f"""
You are a market intelligence analyst.

Analyze the following news article using ONLY the information
provided in the title and description.

ARTICLE ID:
{article["article_id"]}

TITLE:
{article["title"]}

DESCRIPTION:
{article["description"]}

Your goal is to determine the business and market relevance
of this development.

Rules:

- Do not invent facts.
- Do not assume information that is not present.
- Keep the summary concise.
- Companies must contain only organizations explicitly mentioned.
- Risks must contain concrete potential risks supported by the article.
- Opportunities must contain concrete potential opportunities supported by the article.
- If no company is mentioned, return an empty list.
- If no clear risk exists, return an empty list.
- If no clear opportunity exists, return an empty list.

Importance means:

low:
limited broader market or business relevance.

medium:
meaningful development for a sector, company, technology
or regulatory environment.

high:
major development that could materially affect markets,
industries, large companies, regulation or AI adoption.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=ArticleAnalysis.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    analysis = ArticleAnalysis.model_validate_json(
        response.message.content
    )

    return analysis

def analyze_articles(articles):
    analyses = []

    for article in articles:
        try:
            analysis = analyze_article(
                article
            )

            analyses.append(
                analysis
            )

        except Exception as error:
            print(
                f"Failed to analyze article "
                f"{article['article_id']}: {error}"
            )

    return analyses

    return analyses
