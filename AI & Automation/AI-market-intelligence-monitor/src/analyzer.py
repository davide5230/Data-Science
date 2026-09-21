from ollama import chat
from schemas import ArticleAnalysis
import time

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

Category definitions:

models:
new AI models, model releases, capabilities or benchmarks.

infrastructure:
chips, data centers, compute, cloud infrastructure or hardware.

business:
funding, acquisitions, company strategy, revenue, partnerships
or major commercial developments.

regulation:
laws, government policy, regulation or institutional governance.

research:
academic research, scientific results or research institutions.

safety:
AI safety, alignment, misuse, security or existential risk.

applications:
practical adoption or use of AI in products, services or workflows.

other:
use only when none of the above clearly applies.

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

JSON SCHEMA:

{ArticleAnalysis.model_json_schema()}

Return only a valid JSON object matching this schema.
Do not include explanations, markdown or additional text.
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
    think=False,
    options={
        "temperature": 0
    }
)

   content = response.message.content

if not content or not content.strip():
    raise ValueError(
        f"Empty LLM response for article {article['article_id']}"
    )

return ArticleAnalysis.model_validate_json(
    content
)


def analyze_articles(
    articles,
    max_retries=1
):
    analyses = []

    for index, article in enumerate(
        articles,
        start=1
    ):
        print(
            f"Analyzing article "
            f"{index}/{len(articles)}..."
        )

        for attempt in range(
            max_retries + 1
        ):
            try:
                analysis = analyze_article(
                    article
                )

                analyses.append(
                    analysis
                )

                break

            except Exception as error:

                if attempt < max_retries:

                    wait_time = 2 * (
                        attempt + 1
                    )

                    print(
                        f"Retrying article "
                        f"{article['article_id']} "
                        f"in {wait_time}s..."
                    )

                    time.sleep(
                        wait_time
                    )

                else:
                    print(
                        f"Failed to analyze article "
                        f"{article['article_id']}: "
                        f"{error}"
                    )

    return analyses
