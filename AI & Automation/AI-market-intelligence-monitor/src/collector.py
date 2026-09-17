import time
import requests


GDELT_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_articles(
    query,
    max_records=10,
    timespan="24h",
    max_retries=3
):
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_records,
        "timespan": timespan,
        "sort": "datedesc"
    }

    for attempt in range(max_retries):

        response = requests.get(
            GDELT_API_URL,
            params=params,
            timeout=30
        )

        if response.status_code == 429:
            wait_time = 5 * (attempt + 1)

            print(
                f"Rate limit reached. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)
            continue

        response.raise_for_status()

        return response.json()

    raise RuntimeError(
        "GDELT API rate limit exceeded after retries."
    )

if __name__ == "__main__":
    data = fetch_articles(
        query="artificial intelligence",
        max_records=10,
        timespan="24h"
    )

    print(data)
