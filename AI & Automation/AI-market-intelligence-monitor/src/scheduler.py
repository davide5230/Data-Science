import time
import schedule
from logger import logger
from pipeline import run_pipeline
from delivery import deliver_report


KEYWORDS = [
    "artificial intelligence",
    "AI",
    "machine learning",
    "generative AI",
    "LLM"
]

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
                "Scheduled run completed: "
                "no new articles."
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
            f"Scheduled monitor failed: {error}"
        )

        print(
            f"Monitor execution failed: {error}"
        )


schedule.every().day.at("08:00"
                       ).do(run_monitor)

if __name__ == "__main__":
    print(
        "Market Intelligence Monitor started."
    )

    while True:
        schedule.run_pending()
        time.sleep(30)
