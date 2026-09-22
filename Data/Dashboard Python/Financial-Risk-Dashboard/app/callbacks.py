import plotly.graph_objects as go

from dash import Input, Output

from src.analytics import (
    calculate_correlation_matrix,
    calculate_rolling_volatility,
    compare_with_benchmark,
    get_drawdown_series
)

from src.database import (
    fetch_risk_metrics
)


TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "SPY"
]


def register_callbacks(app):

    @app.callback(
        Output("total-return", "children"),
        Output("annualized-return", "children"),
        Output("volatility", "children"),
        Output("max-drawdown", "children"),
        Output("var-95", "children"),
        Output("sharpe-ratio", "children"),
        Output("price-chart", "figure"),
        Output("drawdown-chart", "figure"),
        Output(
            "rolling-volatility-chart",
            "figure"
        ),
        Output("benchmark-chart", "figure"),
        Output("correlation-chart", "figure"),
        Input("ticker-dropdown", "value")
    )
    def update_dashboard(ticker):

        metrics = fetch_risk_metrics()

        selected = metrics[
            metrics["ticker"] == ticker
        ].iloc[0]

        total_return = (
            f"{selected['total_return']:.1%}"
        )

        annualized_return = (
            f"{selected['annualized_return']:.1%}"
        )

        volatility = (
            f"{selected['annualized_volatility']:.1%}"
        )

        max_drawdown = (
            f"{selected['max_drawdown']:.1%}"
        )

        var_95 = (
            f"{selected['var_95']:.2%}"
        )

        sharpe = (
            f"{selected['sharpe_ratio']:.2f}"
        )

        price_data = get_drawdown_series(
            ticker
        )

        price_figure = go.Figure()

        price_figure.add_trace(
            go.Scatter(
                x=price_data["trade_date"],
                y=price_data["adjusted_close"],
                mode="lines",
                name=ticker
            )
        )

        price_figure.update_layout(
            title=f"{ticker} Adjusted Price",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white"
        )

        drawdown_figure = go.Figure()

        drawdown_figure.add_trace(
            go.Scatter(
                x=price_data["trade_date"],
                y=price_data["drawdown"],
                mode="lines",
                fill="tozeroy",
                name="Drawdown"
            )
        )

        drawdown_figure.update_layout(
            title=f"{ticker} Drawdown",
            xaxis_title="Date",
            yaxis_tickformat=".0%",
            template="plotly_white"
        )

        rolling = calculate_rolling_volatility(
            ticker
        )

        volatility_figure = go.Figure()

        volatility_figure.add_trace(
            go.Scatter(
                x=rolling["trade_date"],
                y=rolling["rolling_volatility"],
                mode="lines",
                name="30D Volatility"
            )
        )

        volatility_figure.update_layout(
            title="30-Day Rolling Volatility",
            xaxis_title="Date",
            yaxis_tickformat=".0%",
            template="plotly_white"
        )

        benchmark = compare_with_benchmark(
            ticker
        )

        benchmark_figure = go.Figure()

        benchmark_figure.add_trace(
            go.Scatter(
                x=benchmark["trade_date"],
                y=benchmark["asset_cumulative"],
                mode="lines",
                name=ticker
            )
        )

        if ticker != "SPY":
            benchmark_figure.add_trace(
                go.Scatter(
                    x=benchmark["trade_date"],
                    y=benchmark[
                        "benchmark_cumulative"
                    ],
                    mode="lines",
                    name="SPY"
                )
            )

        benchmark_figure.update_layout(
            title=(
                "SPY Cumulative Return"
                if ticker == "SPY"
                else f"{ticker} vs SPY"
            ),
            xaxis_title="Date",
            yaxis_title="Cumulative Return",
            yaxis_tickformat=".0%",
            template="plotly_white"
        )

        correlation = (
            calculate_correlation_matrix(
                TICKERS
            )
        )

        correlation_figure = go.Figure(
            data=go.Heatmap(
                z=correlation.values,
                x=correlation.columns,
                y=correlation.index,
                zmin=-1,
                zmax=1,
                text=correlation.round(2).values,
                texttemplate="%{text}"
            )
        )

        correlation_figure.update_layout(
            title="Daily Return Correlation Matrix",
            template="plotly_white"
        )

        return (
            total_return,
            annualized_return,
            volatility,
            max_drawdown,
            var_95,
            sharpe,
            price_figure,
            drawdown_figure,
            volatility_figure,
            benchmark_figure,
            correlation_figure
        )
