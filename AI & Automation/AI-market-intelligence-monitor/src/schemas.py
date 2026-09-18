from typing import Literal
from pydantic import BaseModel


class ArticleAnalysis(BaseModel):
    article_id: str

    category: Literal[
        "models",
        "infrastructure",
        "business",
        "regulation",
        "research",
        "safety",
        "applications",
        "other"
    ]

    importance: Literal[
        "low",
        "medium",
        "high"
    ]

    summary: str
    companies: list[str]
    business_impact: str
    risks: list[str]
    opportunities: list[str]


class MarketIntelligenceReport(BaseModel):
    executive_summary: str

    top_developments: list[str]

    emerging_trends: list[str]

    companies_to_watch: list[str]

    key_risks: list[str]

    key_opportunities: list[str]
