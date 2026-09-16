from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4


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

class TicketResponse(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    category: str
    route_to: str
    status: Literal["routed"]


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketInput):
    category = classify_ticket(
        ticket.subject,
        ticket.message
    )

    route_to = CATEGORY_ROUTES[category]

    ticket_id = f"TKT-{uuid4().hex[:8].upper()}"

    return TicketResponse(
        ticket_id=ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        category=category,
        route_to=route_to,
        status="routed"
    )
