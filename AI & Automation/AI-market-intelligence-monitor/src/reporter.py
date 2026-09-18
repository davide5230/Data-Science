from ollama import chat

from schemas import MarketIntelligenceReport


MODEL_NAME = "qwen3.5:4b"


def build_report_prompt(analyses):

    analyses_text = []

    for analysis in analyses:
        analyses_text.append(
            analysis.model_dump_json()
        )

    joined_analyses = "\n".join(
        analyses_text
    )

    prompt = f"""
You are a senior market intelligence analyst.

You are given a collection of structured analyses
of recent artificial intelligence news.

Your task is to produce ONE concise market intelligence report.

Use ONLY the supplied analyses.

Do not invent companies, events, risks, opportunities
or market developments.

ARTICLE ANALYSES:

{joined_analyses}

Create the report according to these rules:

EXECUTIVE SUMMARY
Summarize the most important overall developments
and their business significance.

TOP DEVELOPMENTS
Select only the most important developments.
Do not list every article.

EMERGING TRENDS
Identify recurring themes that appear across
multiple developments.

COMPANIES TO WATCH
Include organizations that appear strategically
important based on the supplied analyses.
Do not include a company merely because it is mentioned.

KEY RISKS
Aggregate the most meaningful business,
regulatory, technological or market risks.

KEY OPPORTUNITIES
Aggregate the strongest potential business
or market opportunities.

Avoid repetition.

Be concise and business-oriented.
"""

    return prompt

def generate_market_report(analyses):

    if not analyses:
        raise ValueError(
            "Cannot generate report without analyses."
        )

    prompt = build_report_prompt(
        analyses
    )

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=MarketIntelligenceReport.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    content = response.message.content

    if not content or not content.strip():
        raise ValueError(
            "LLM returned an empty market report."
        )

    return MarketIntelligenceReport.model_validate_json(
        content
    )
