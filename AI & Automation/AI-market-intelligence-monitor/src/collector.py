import requests

from processor import normalize_articles


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

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "News API request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to the News API."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"News API returned an HTTP error: {error}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"News API request failed: {error}"
        )


if __name__ == "__main__":
    data = fetch_articles(
        query="artificial intelligence",
        size=10
    )

    raw_articles = data.get("results", [])

    articles = normalize_articles(raw_articles)

    for article in articles:
        print("\n---")
        print(article)    articles = normalize_articles(raw_articles)

    for article in articles:
        print("\n---")
        print(article)
