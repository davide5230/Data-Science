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

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "News API request timed out."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Unable to connect to the News API."
        ) from error

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"News API returned an HTTP error: {error}"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"News API request failed: {error}"
        ) from error
