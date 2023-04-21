import requests
from bs4 import BeautifulSoup


def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    search_results = []
    for result in soup.find_all("div", class_="g"):
        link = result.find("a").get("href")
        title = result.find("h3").text
        description = result.find("span", class_="aCOpRe").text
        search_results.append((title, link, description))
    return search_results


google_search("cat")
