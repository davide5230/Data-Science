import time

import schedule

from delivery import deliver_report
from logger import logger
from pipeline import run_pipeline


KEYWORDS = [
    "artificial intelligence",
    "AI",
    "machine learning",
    "generative AI",
    "LLM"
]

SCHEDULE_TIME = "08:00"


def run_monitor():
    logger.info(
        "Scheduled monitor execution started."
    )

    try:
        result = run_pipeline(
            query="artificial intelligence",
            keywords=KEYWORDS,
            size=20
        )

        if result["report"] is None:
            logger.info(
                "Scheduled run completed: no new articles."
            )
            print(
                "No new articles to report."
            )
            return

        deliver_report(
            statistics=result["statistics"],
            report=result["report"]
        )

        logger.info(
            "Report delivered successfully."
        )

        print(
            "New market intelligence report "
            "generated and delivered."
        )

    except Exception as error:
        logger.exception(
            "Scheduled monitor failed: %s",
            error
        )
        print(
            f"Monitor execution failed: {error}"
        )


schedule.every().day.at(
    SCHEDULE_TIME
).do(run_monitor)


if __name__ == "__main__":
    print(
        f"Market Intelligence Monitor started. "
        f"Scheduled daily at {SCHEDULE_TIME}."
    )

    while True:
        schedule.run_pending()
        time.sleep(30)
