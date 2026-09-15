import pandas as pd

def add_economic_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["revenue"] = df["units"] * df["unit_price"]
    df["cost"] = df["units"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]
    df["margin"] = df["profit"] / df["revenue"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

def calculate_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_revenue": df["revenue"].sum(),
        "total_profit": df["profit"].sum(),
        "average_margin": df["profit"].sum() / df["revenue"].sum(),
        "total_units": df["units"].sum(),
        "average_order_value": df["revenue"].mean(),
    }

def grouped_performance(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    result = (
        df.groupby(group_column)
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            units=("units", "sum"),
            costs=("cost", "sum"),
        )
    )
    result["margin"] = result["profit"] / result["revenue"]
    return result.sort_values("revenue", ascending=False)

def monthly_performance(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            units=("units", "sum"),
            costs=("cost", "sum"),
        )
    )
    result["margin"] = result["profit"] / result["revenue"]
    result["revenue_growth_pct"] = result["revenue"].pct_change() * 100
    result["profit_growth_pct"] = result["profit"].pct_change() * 100
    return result


def build_analysis_output(
    df: pd.DataFrame,
    kpis: dict,
    product_performance: pd.DataFrame,
    region_performance: pd.DataFrame,
    monthly: pd.DataFrame,
) -> dict:
    """Create the structured analytical payload consumed by the LLM."""

    worst_product = product_performance["margin"].idxmin()
    worst_product_margin = product_performance.loc[
        worst_product, "margin"
    ]
    worst_month = monthly["revenue_growth_pct"].idxmin()

    return {
        "metadata": {
            "rows": int(len(df)),
            "period_start": df["date"].min().strftime("%Y-%m-%d"),
            "period_end": df["date"].max().strftime("%Y-%m-%d"),
            "products": int(df["product"].nunique()),
            "regions": int(df["region"].nunique()),
        },
        "kpis": {
            "total_revenue": round(float(kpis["total_revenue"]), 2),
            "total_profit": round(float(kpis["total_profit"]), 2),
            "average_margin": round(float(kpis["average_margin"]), 4),
            "total_units": int(kpis["total_units"]),
            "average_order_value": round(
                float(kpis["average_order_value"]), 2
            ),
        },
        "product_performance": (
            product_performance.reset_index()
            .round(4)
            .to_dict(orient="records")
        ),
        "region_performance": (
            region_performance.reset_index()
            .round(4)
            .to_dict(orient="records")
        ),
        "monthly_performance": (
            monthly.reset_index()
            .round(4)
            .to_dict(orient="records")
        ),
        "best_product_by_revenue": product_performance.index[0],
        "anomalies": {
            "loss_making_transactions": int(
                (df["profit"] < 0).sum()
            ),
            "worst_product_by_margin": {
                "product": worst_product,
                "margin": round(float(worst_product_margin), 4),
            },
            "worst_month_by_revenue_growth": worst_month,
        },
    }
