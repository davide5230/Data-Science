import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


def format_report_email(
    statistics,
    report
):
    lines = [
        "AI MARKET INTELLIGENCE REPORT",
        "",
        "EXECUTIVE SUMMARY",
        report.executive_summary,
        "",
        "TOP DEVELOPMENTS"
    ]

    lines.extend(
        f"- {item}"
        for item in report.top_developments
    )

    lines.extend([
        "",
        "EMERGING TRENDS"
    ])

    lines.extend(
        f"- {item}"
        for item in report.emerging_trends
    )

    lines.extend([
        "",
        "COMPANIES TO WATCH"
    ])

    lines.extend(
        f"- {company}"
        for company in report.companies_to_watch
    )

    lines.extend([
        "",
        "KEY RISKS"
    ])

    lines.extend(
        f"- {risk}"
        for risk in report.key_risks
    )

    lines.extend([
        "",
        "KEY OPPORTUNITIES"
    ])

    lines.extend(
        f"- {opportunity}"
        for opportunity in report.key_opportunities
    )

    lines.extend([
        "",
        "STATISTICS",
        f"Articles analyzed: {statistics['total_articles']}",
        f"Importance: {statistics['importance']}",
        f"Categories: {statistics['categories']}"
    ])

    return "\n".join(lines)


def send_email(
    subject,
    body
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    required_values = {
        "SMTP_HOST": smtp_host,
        "SMTP_USER": smtp_user,
        "SMTP_PASSWORD": smtp_password,
        "EMAIL_FROM": email_from,
        "EMAIL_TO": email_to
    }

    missing = [
        key
        for key, value in required_values.items()
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
    message.set_content(body)

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
        subject="AI Market Intelligence Report",
        body=body
    )
