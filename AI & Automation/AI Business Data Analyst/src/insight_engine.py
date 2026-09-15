def generate_business_insights(analysis_output: dict) -> list[dict]:
    insights = []
    kpis = analysis_output["kpis"]
    products = analysis_output["product_performance"]
    regions = analysis_output["region_performance"]
    months = analysis_output["monthly_performance"]
    anomalies = analysis_output["anomalies"]

    loss_count = anomalies["loss_making_transactions"]
    if loss_count > 0:
        insights.append({
            "severity": "high",
            "type": "profitability",
            "message": f"{loss_count} transactions generated negative profit.",
        })

    worst_product = anomalies["worst_product_by_margin"]
    insights.append({
        "severity": "medium",
        "type": "product_margin",
        "message": (
            f"{worst_product['product']} has the lowest overall "
            f"margin at {worst_product['margin']:.1%}."
        ),
    })

    best_region = max(regions, key=lambda x: x["revenue"])
    insights.append({
        "severity": "info",
        "type": "regional_performance",
        "message": (
            f"{best_region['region']} generated the highest regional "
            f"revenue at €{best_region['revenue']:,.2f}."
        ),
    })

    worst_month_name = anomalies["worst_month_by_revenue_growth"]
    worst_month_data = next(
        m for m in months if m["month"] == worst_month_name
    )
    worst_growth = worst_month_data["revenue_growth_pct"]

    if worst_growth < 0:
        insights.append({
            "severity": "high" if worst_growth <= -20 else "medium",
            "type": "revenue_trend",
            "message": (
                f"Revenue declined by {abs(worst_growth):.1f}% "
                f"in {worst_month_name} compared with the previous month."
            ),
        })

    portfolio_margin = kpis["average_margin"]
    low_margin_products = [
        p for p in products if p["margin"] < portfolio_margin
    ]

    if low_margin_products:
        weakest = min(low_margin_products, key=lambda x: x["margin"])
        gap = portfolio_margin - weakest["margin"]

        insights.append({
            "severity": "medium",
            "type": "relative_margin",
            "message": (
                f"{weakest['product']} is {gap:.1%} below "
                f"the portfolio average margin."
            ),
        })

    return insights
