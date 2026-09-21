import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


def format_report_email(
    statistics,
    report
):
    lines = []

    lines.append(
        "AI MARKET INTELLIGENCE REPORT"
    )

    lines.append("")
    lines.append("EXECUTIVE SUMMARY")
    lines.append(
        report.executive_summary
    )

    lines.append("")
    lines.append("TOP DEVELOPMENTS")

    for item in report.top_developments:
        lines.append(
            f"- {item}"
        )

    lines.append("")
    lines.append("EMERGING TRENDS")

    for item in report.emerging_trends:
        lines.append(
            f"- {item}"
        )

    lines.append("")
    lines.append("COMPANIES TO WATCH")

    for company in report.companies_to_watch:
        lines.append(
            f"- {company}"
        )

    lines.append("")
    lines.append("KEY RISKS")

    for risk in report.key_risks:
        lines.append(
            f"- {risk}"
        )

    lines.append("")
    lines.append("KEY OPPORTUNITIES")

    for opportunity in report.key_opportunities:
        lines.append(
            f"- {opportunity}"
        )

    lines.append("")
    lines.append("STATISTICS")

    lines.append(
        f"Articles analyzed: "
        f"{statistics['total_articles']}"
    )

    lines.append(
        f"Importance: "
        f"{statistics['importance']}"
    )

    lines.append(
        f"Categories: "
        f"{statistics['categories']}"
    )

    return "\n".join(lines)

def send_email(
    subject,
    body
):
    smtp_host = os.getenv(
        "SMTP_HOST"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_user = os.getenv(
        "SMTP_USER"
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )

    email_from = os.getenv(
        "EMAIL_FROM"
    )

    email_to = os.getenv(
        "EMAIL_TO"
    )

    required_values = {
        "SMTP_HOST": smtp_host,
        "SMTP_USER": smtp_user,
        "SMTP_PASSWORD": smtp_password,
        "EMAIL_FROM": email_from,
        "EMAIL_TO": email_to
    }

    missing = [
        key
        for key, value
        in required_values.items()
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing email configuration: "
            + ", ".join(missing)
        )

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = email_to

    message.set_content(
        body
    )

    with smtplib.SMTP(
        smtp_host,
        smtp_port,
        timeout=30
    ) as server:

        server.starttls()

        server.login(
            smtp_user,
            smtp_password
        )

        server.send_message(
            message
        )

def deliver_report(
    statistics,
    report
):
    body = format_report_email(
        statistics,
        report
    )

    send_email(
        subject=(
            "AI Market Intelligence Report"
        ),
        body=body
    )
