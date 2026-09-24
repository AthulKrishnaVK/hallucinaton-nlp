# import requests
# from urllib.parse import quote


# WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# HEADERS = {
#     "User-Agent": (
#         "HallucinationDetector/0.1 "
#         "(educational NLP research project)"
#     )
# }


# def search_wikipedia(query: str, limit: int = 5):
#     """
#     Search Wikipedia for evidence related to a claim.

#     If Wikipedia is unavailable, return an empty list
#     instead of crashing the complete analysis pipeline.
#     """

#     params = {
#         "action": "query",
#         "list": "search",
#         "srsearch": query,
#         "format": "json",
#         "srlimit": limit
#     }

#     try:

#         response = requests.get(
#             WIKIPEDIA_API,
#             params=params,
#             headers=HEADERS,
#             timeout=10
#         )

#         response.raise_for_status()

#         data = response.json()

#         results = []

#         for item in data.get("query", {}).get("search", []):

#             title = item.get("title", "")

#             results.append({
#                 "title": title,
#                 "snippet": item.get("snippet", ""),
#                 "source": "Wikipedia",
#                 "url": (
#                     "https://en.wikipedia.org/wiki/"
#                     + quote(title.replace(" ", "_"))
#                 )
#             })

#         return results

#     except requests.RequestException as error:

#         print(
#             f"Wikipedia search failed: {error}"
#         )

#         return []


# def get_wikipedia_page(title: str):
#     """
#     Retrieve the plain-text extract of a Wikipedia page.
#     """

#     params = {
#         "action": "query",
#         "prop": "extracts",
#         "explaintext": True,
#         "titles": title,
#         "format": "json"
#     }

#     try:

#         response = requests.get(
#             WIKIPEDIA_API,
#             params=params,
#             headers=HEADERS,
#             timeout=10
#         )

#         response.raise_for_status()

#         data = response.json()

#         pages = data.get(
#             "query",
#             {}
#         ).get(
#             "pages",
#             {}
#         )

#         if not pages:
#             return None

#         page = next(iter(pages.values()))

#         return {
#             "title": page.get("title"),
#             "text": page.get("extract", ""),
#             "source": "Wikipedia",
#             "url": (
#                 "https://en.wikipedia.org/wiki/"
#                 + quote(title.replace(" ", "_"))
#             )
#         }

#     except requests.RequestException as error:

#         print(
#             f"Wikipedia page retrieval failed: {error}"
#         )

#         return None


import requests
import re
import html

from urllib.parse import quote


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"


HEADERS = {
    "User-Agent": (
        "HallucinationDetector/0.1 "
        "(educational NLP research project)"
    )
}


def clean_html(text: str):
    """
    Remove HTML tags from Wikipedia snippets
    and decode HTML entities.
    """

    if not text:
        return ""

    # Decode entities such as &#039;
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # Remove extra whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def search_wikipedia(
    query: str,
    limit: int = 5
):
    """
    Search Wikipedia for evidence related
    to a claim.

    Returns an empty list if Wikipedia
    is unavailable.
    """

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit
    }

    try:

        response = requests.get(
            WIKIPEDIA_API,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get(
            "query",
            {}
        ).get(
            "search",
            []
        ):

            title = item.get(
                "title",
                ""
            )

            snippet = clean_html(
                item.get(
                    "snippet",
                    ""
                )
            )

            results.append({

                "title": title,

                "snippet": snippet,

                "source": "Wikipedia",

                "url": (
                    "https://en.wikipedia.org/wiki/"
                    + quote(
                        title.replace(
                            " ",
                            "_"
                        )
                    )
                )

            })

        return results

    except requests.RequestException as error:

        print(
            f"Wikipedia search failed: {error}"
        )

        return []


def get_wikipedia_page(
    title: str
):
    """
    Retrieve the complete plain-text
    Wikipedia page extract.
    """

    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }

    try:

        response = requests.get(
            WIKIPEDIA_API,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        pages = data.get(
            "query",
            {}
        ).get(
            "pages",
            {}
        )

        if not pages:
            return None

        page = next(
            iter(
                pages.values()
            )
        )

        return {

            "title": page.get(
                "title"
            ),

            "text": page.get(
                "extract",
                ""
            ),

            "source": "Wikipedia",

            "url": (
                "https://en.wikipedia.org/wiki/"
                + quote(
                    title.replace(
                        " ",
                        "_"
                    )
                )
            )

        }

    except requests.RequestException as error:

        print(
            f"Wikipedia page retrieval failed: {error}"
        )

        return None