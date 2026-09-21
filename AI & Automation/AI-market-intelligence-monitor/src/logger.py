import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_PATH = LOG_DIR / "market_monitor.log"


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


logger = logging.getLogger(
    "market_monitor"
)
