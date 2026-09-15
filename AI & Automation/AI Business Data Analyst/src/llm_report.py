import json
from ollama import chat
from .schemas import BusinessReport

SYSTEM_PROMPT = """
You are a senior business data analyst.

Analyze the provided structured business performance data.

STRICT RULES:
- Use only facts and numerical values explicitly contained in the data.
- Never invent numerical values.
- Never claim causality unless the data directly proves it.
- Do not infer seasonality from a single year.
- If a cause is unknown, state that it is unknown.
- Possible explanations must be placed only in hypothesis_to_investigate.
- Evidence must contain only information supported by the data.
- Recommendations must follow logically from observed evidence.
- Accuracy is more important than creativity.

CAUSALITY RULES:
- Never explain WHY a metric changed unless the provided data directly demonstrates the cause.
- A lower margin does not automatically imply higher logistics, pricing problems, sourcing inefficiency, marketing issues, customer acquisition costs or operational inefficiency.
- A monthly decline does not prove seasonality or recurring behavior unless multiple years of data are available.
- When proposing a possible explanation, place it in hypothesis_to_investigate.
"""

def generate_ai_report(
    analysis_output: dict,
    model: str = "qwen3.5:4b",
) -> BusinessReport:
    analysis_json = json.dumps(analysis_output, indent=2)

    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Analyze the following business performance data:\n\n"
                    f"{analysis_json}"
                ),
            },
        ],
        format=BusinessReport.model_json_schema(),
        think=False,
        options={
            "num_ctx": 8192,
            "num_predict": 1500,
            "temperature": 0,
        },
    )

    return BusinessReport.model_validate_json(
        response.message.content
    )
