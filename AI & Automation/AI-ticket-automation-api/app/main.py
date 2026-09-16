from fastapi import FastAPI
from pydantic import BaseModel

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


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }
