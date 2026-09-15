from typing import Literal
from pydantic import BaseModel

class Finding(BaseModel):
    title: str
    evidence: str
    interpretation: str

class Risk(BaseModel):
    title: str
    evidence: str
    hypothesis_to_investigate: str | None = None

class Opportunity(BaseModel):
    title: str
    evidence: str
    action: str

class Recommendation(BaseModel):
    priority: Literal["high", "medium", "low"]
    action: str
    rationale: str

class BusinessReport(BaseModel):
    executive_summary: str
    key_findings: list[Finding]
    risks: list[Risk]
    opportunities: list[Opportunity]
    recommendations: list[Recommendation]
