import requests


GDELT_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_articles(
    query,
    max_records=10,
    timespan="24h"
):
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_records,
        "timespan": timespan,
        "sort": "datedesc"
    }

    response = requests.get(
        GDELT_API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = fetch_articles(
        query="artificial intelligence",
        max_records=10,
        timespan="24h"
    )

    print(data)
