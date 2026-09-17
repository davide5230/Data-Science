import requests


NEWS_API_URL = "https://freenewsapi.ai/v1/search"


def fetch_articles(
    query,
    size=10,
    date="today"
):
    params = {
        "q": query,
        "size": size,
        "date": date
    }

    response = requests.get(
        NEWS_API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = fetch_articles(
        query="artificial intelligence",
        size=10
    )

    print(data)
