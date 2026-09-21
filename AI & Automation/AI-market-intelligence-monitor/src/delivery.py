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
    lines.append(report.executive_summary)

    lines.append("")
    lines.append("TOP DEVELOPMENTS")

    for item in report.top_developments:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("EMERGING TRENDS")

    for item in report.emerging_trends:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("COMPANIES TO WATCH")

    for company in report.companies_to_watch:
        lines.append(f"- {company}")

    lines.append("")
    lines.append("KEY RISKS")

    for risk in report.key_risks:
        lines.append(f"- {risk}")

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
