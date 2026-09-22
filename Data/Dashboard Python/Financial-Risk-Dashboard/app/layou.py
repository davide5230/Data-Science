from dash import dcc, html

from src.database import fetch_risk_metrics


metrics = fetch_risk_metrics()

TICKERS = metrics["ticker"].tolist()


def create_layout():
    return html.Div(
        className="dashboard",
        children=[
            html.Div(
                className="header",
                children=[
                    html.Div([
                        html.H1(
                            "Financial Risk Dashboard"
                        ),
                        html.P(
                            "PostgreSQL-powered market risk analytics"
                        )
                    ]),

                    dcc.Dropdown(
                        id="ticker-dropdown",
                        options=[
                            {
                                "label": ticker,
                                "value": ticker
                            }
                            for ticker in TICKERS
                        ],
                        value="AAPL",
                        clearable=False,
                        className="ticker-dropdown"
                    )
                ]
            ),

            html.Div(
                className="kpi-grid",
                children=[
                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("Total Return"),
                            html.H2(id="total-return")
                        ]
                    ),

                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("Annualized Return"),
                            html.H2(id="annualized-return")
                        ]
                    ),

                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("Volatility"),
                            html.H2(id="volatility")
                        ]
                    ),

                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("Max Drawdown"),
                            html.H2(id="max-drawdown")
                        ]
                    ),

                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("VaR 95%"),
                            html.H2(id="var-95")
                        ]
                    ),

                    html.Div(
                        className="kpi-card",
                        children=[
                            html.P("Sharpe Ratio"),
                            html.H2(id="sharpe-ratio")
                        ]
                    )
                ]
            ),

            html.Div(
                className="chart-grid",
                children=[
                    dcc.Graph(
                        id="price-chart"
                    ),

                    dcc.Graph(
                        id="drawdown-chart"
                    ),

                    dcc.Graph(
                        id="rolling-volatility-chart"
                    ),

                    dcc.Graph(
                        id="benchmark-chart"
                    )
                ]
            ),

            html.Div(
                className="full-chart",
                children=[
                    dcc.Graph(
                        id="correlation-chart"
                    )
                ]
            )
        ]
    )
