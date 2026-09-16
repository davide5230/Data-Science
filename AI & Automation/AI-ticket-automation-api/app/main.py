from fastapi import FastAPI

app = FastAPI(
    title="AI Support Ticket Automation API",
    description=(
        "API for automated support ticket analysis, "
        "classification and routing."
    ),
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Support Ticket Automation API"
    }
