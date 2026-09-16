from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal


app = FastAPI(
    title="AI Support Ticket Automation API",
    description=(
        "API for automated support ticket analysis, "
        "classification and routing."
    ),
    version="1.0.0"
)


class TicketInput(BaseModel):
    customer_id: str
    subject: str
    message: str


class TicketResponse(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    status: Literal["received"]


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketInput):
    return TicketResponse(
        ticket_id="TKT-0001",
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        status="received"
    )
