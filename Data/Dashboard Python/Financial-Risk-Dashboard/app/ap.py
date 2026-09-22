from dash import Dash

from app.callbacks import register_callbacks
from app.layout import create_layout


app = Dash(
    __name__,
    title="Financial Risk Dashboard"
)

app.layout = create_layout()

register_callbacks(
    app
)


if __name__ == "__main__":
    app.run(
        debug=True
    )
