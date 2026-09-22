from pathlib import Path

from dash import Dash

from app.callbacks import register_callbacks
from app.layout import create_layout


PROJECT_ROOT = Path(__file__).resolve().parent.parent


app = Dash(
    __name__,
    title="Financial Risk Dashboard",
    assets_folder=str(PROJECT_ROOT / "assets")
)

app.layout = create_layout()

register_callbacks(
    app
)


if __name__ == "__main__":
    app.run(
        debug=False
    )
