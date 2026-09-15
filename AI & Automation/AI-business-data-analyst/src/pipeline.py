import json
from pathlib import Path

from src.data_generator import generate_business_data
from src.analytics import (
    add_economic_metrics,
    build_analysis_output,
    calculate_kpis,
    grouped_performance,
    monthly_performance,
)
from src.insight_engine import generate_business_insights
from src.llm_report import generate_ai_report


def main():
    df = generate_business_data()
    df = add_economic_metrics(df)

    kpis = calculate_kpis(df)
    product_perf = grouped_performance(df, "product")
    region_perf = grouped_performance(df, "region")
    monthly_perf = monthly_performance(df)

    analysis_output = build_analysis_output(
        df,
        kpis,
        product_perf,
        region_perf,
        monthly_perf,
    )

    analysis_output["insights"] = generate_business_insights(
        analysis_output
    )

    report = generate_ai_report(analysis_output)

    output_path = Path("outputs/business_report.json")
    output_path.parent.mkdir(exist_ok=True)

    output_path.write_text(
        report.model_dump_json(indent=4),
        encoding="utf-8",
    )

    print(
        json.dumps(
            report.model_dump(),
            indent=4,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
