from services.web_search_service import search_wikipedia


results = search_wikipedia(
    "Taj Mahal built Shah Jahan"
)

for result in results:
    print("\nTITLE:", result["title"])
    print("SNIPPET:", result["snippet"])
    print("URL:", result["url"])