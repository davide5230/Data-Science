from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4
from ollama import chat


app = FastAPI(
    title="AI Support Ticket Automation API",
    description=(
        "API for automated support ticket analysis, "
        "classification and routing."
    ),
    version="1.0.0"
)

CATEGORY_ROUTES = {
    "billing": "billing_team",
    "technical": "technical_support",
    "account": "account_support",
    "shipping": "logistics_team",
    "general": "customer_support"
}

def classify_ticket(subject, message):
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
        "login",
        "technical"
    ]):
        return "technical"

    if any(word in text for word in [
        "account",
        "password",
        "profile",
        "email"
    ]):
        return "account"

    if any(word in text for word in [
        "shipping",
        "delivery",
        "package",
        "order"
    ]):
        return "shipping"

    return "general"


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
    status: Literal["routed"]

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

- low: informational or minor request with no significant impact
- medium: normal support issue affecting the customer
- high: important issue causing significant disruption or financial impact
- critical: severe issue requiring immediate attention, such as security compromise or complete service failure

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

test_ticket = TicketInput(
    customer_id="CUST-1042",
    subject="I was charged twice",
    message="My credit card shows two charges for the same order."
)

analysis = analyze_ticket(test_ticket)

print(analysis)

print(analysis.category)
print(analysis.priority)
print(analysis.summary)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketInput):

    analysis = analyze_ticket(ticket)

    route_to = CATEGORY_ROUTES[
        analysis.category
    ]

    ticket_id = (
        f"TKT-{uuid4().hex[:8].upper()}"
    )

    return TicketResponse(
        ticket_id=ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        category=analysis.category,
        priority=analysis.priority,
        summary=analysis.summary,
        route_to=route_to,
        status="routed"
    )
