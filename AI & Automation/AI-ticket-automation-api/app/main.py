from pathlib import Path
import sqlite3
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from ollama import chat
from pydantic import BaseModel


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DB_PATH = Path("data/tickets.db")

CATEGORY_ROUTES = {
    "billing": "billing_team",
    "technical": "technical_support",
    "account": "account_support",
    "shipping": "logistics_team",
    "general": "customer_support"
}


# ---------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------

class TicketInput(BaseModel):
    customer_id: str
    subject: str
    message: str


class TicketAnalysis(BaseModel):
    category: Literal[
        "billing",
        "technical",
        "account",
        "shipping",
        "general"
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    summary: str


class TicketResponse(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    message: str

    category: Literal[
        "billing",
        "technical",
        "account",
        "shipping",
        "general"
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    summary: str
    route_to: str

    analysis_source: Literal[
        "llm",
        "rule_based_fallback"
    ]

    status: Literal["routed"]


# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="AI Support Ticket Automation API",
    description=(
        "API for automated support ticket analysis, "
        "classification and routing."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def init_db():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                summary TEXT NOT NULL,
                route_to TEXT NOT NULL,
                analysis_source TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )


def save_ticket(ticket: TicketResponse):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO tickets (
                ticket_id,
                customer_id,
                subject,
                message,
                category,
                priority,
                summary,
                route_to,
                analysis_source,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.ticket_id,
                ticket.customer_id,
                ticket.subject,
                ticket.message,
                ticket.category,
                ticket.priority,
                ticket.summary,
                ticket.route_to,
                ticket.analysis_source,
                ticket.status
            )
        )


def get_all_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            "SELECT * FROM tickets"
        ).fetchall()

    return [
        TicketResponse.model_validate(dict(row))
        for row in rows
    ]


def get_ticket_by_id(ticket_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT *
            FROM tickets
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        ).fetchone()

    if row is None:
        return None

    return TicketResponse.model_validate(
        dict(row)
    )


init_db()


# ---------------------------------------------------------
# LLM analysis
# ---------------------------------------------------------

TICKET_ANALYSIS_PROMPT = """
You are a customer support ticket classifier.

Analyze the provided customer support ticket.

Classify it into exactly one category:

- billing: payments, invoices, charges, refunds or billing issues
- technical: bugs, crashes, errors or technical malfunctions
- account: account access, password, profile or authentication issues
- shipping: delivery, shipment, package or order delivery issues
- general: requests that do not clearly belong to another category

Assign exactly one priority:

- low: informational request, minor inconvenience or non-urgent question
- medium: standard support issue affecting the customer, but with no major financial, operational or security impact
- high: issue causing significant financial impact, repeated service failure, major disruption or inability to use an important service
- critical: confirmed or strongly indicated security compromise, complete outage affecting essential service, data loss, fraud in progress, or another situation requiring immediate intervention

Priority rules:
- Do not assign high priority only because the customer cannot log in.
- Do not assign high priority only because money is mentioned.
- Use critical only when there is clear evidence of immediate severe impact.
- When severity is uncertain, prefer the lower justified priority.

Write a short factual summary of the ticket.

Do not invent information that is not present in the ticket.
Return the result using the required structured format.
""".strip()


def analyze_ticket(
    ticket: TicketInput,
    model="qwen3.5:4b"
):
    response = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": TICKET_ANALYSIS_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"SUBJECT:\n{ticket.subject}\n\n"
                    f"MESSAGE:\n{ticket.message}"
                )
            }
        ],
        format=TicketAnalysis.model_json_schema(),
        think=False,
        options={
            "temperature": 0
        }
    )

    return TicketAnalysis.model_validate_json(
        response.message.content
    )


# ---------------------------------------------------------
# Deterministic fallback
# ---------------------------------------------------------

def classify_ticket_rule_based(subject, message):
    text = f"{subject} {message}".lower()

    if any(word in text for word in [
        "charged",
        "payment",
        "invoice",
        "refund",
        "billing"
    ]):
        return "billing"

    if any(word in text for word in [
        "error",
        "bug",
        "crash",
        "technical"
    ]):
        return "technical"

    if any(word in text for word in [
        "account",
        "password",
        "profile",
        "login",
        "authentication"
    ]):
        return "account"

    if any(word in text for word in [
        "shipping",
        "delivery",
        "package",
        "shipment"
    ]):
        return "shipping"

    return "general"


def determine_priority_rule_based(subject, message):
    text = f"{subject} {message}".lower()

    critical_terms = [
        "hacked",
        "fraud",
        "security breach",
        "data loss",
        "stolen account"
    ]

    high_terms = [
        "charged twice",
        "multiple charges",
        "complete outage",
        "cannot use service"
    ]

    if any(term in text for term in critical_terms):
        return "critical"

    if any(term in text for term in high_terms):
        return "high"

    return "medium"


def fallback_analysis(ticket: TicketInput):
    category = classify_ticket_rule_based(
        ticket.subject,
        ticket.message
    )

    priority = determine_priority_rule_based(
        ticket.subject,
        ticket.message
    )

    summary = (
        ticket.message[:200]
        if len(ticket.message) > 200
        else ticket.message
    )

    return TicketAnalysis(
        category=category,
        priority=priority,
        summary=summary
    )


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }


@app.post(
    "/tickets",
    response_model=TicketResponse
)
def create_ticket(ticket: TicketInput):

    try:
        analysis = analyze_ticket(ticket)
        analysis_source = "llm"

    except Exception:
        analysis = fallback_analysis(ticket)
        analysis_source = "rule_based_fallback"

    route_to = CATEGORY_ROUTES[
        analysis.category
    ]

    ticket_id = (
        f"TKT-{uuid4().hex[:8].upper()}"
    )

    ticket_response = TicketResponse(
        ticket_id=ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        message=ticket.message,
        category=analysis.category,
        priority=analysis.priority,
        summary=analysis.summary,
        route_to=route_to,
        analysis_source=analysis_source,
        status="routed"
    )

    save_ticket(ticket_response)

    return ticket_response


@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets():
    return get_all_tickets()


@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(ticket_id: str):

    ticket = get_ticket_by_id(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket
