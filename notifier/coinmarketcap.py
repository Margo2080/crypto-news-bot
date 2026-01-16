import requests
from bs4 import BeautifulSoup

CMC_URL = "https://coinmarketcap.com/headlines/news/"

# Ключевые слова — сильные рыночные триггеры
STRONG_KEYWORDS = [
    "etf",
    "sec",
    "approval",
    "approved",
    "lawsuit",
    "regulation",
    "ban",
    "listing",
    "delisting",
    "hack",
    "exploit",
    "crash",
    "collapse",
    "pump",
    "dump",
    "bitcoin",
    "ethereum",
    "btc",
    "eth",
]

def get_strong_coinmarketcap_news():
    """
    Возвращает одну сильную новость CoinMarketCap или None
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(CMC_URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", href=True)

    for a in articles:
        title = a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        title_lower = title.lower()

        if any(word in title_lower for word in STRONG_KEYWORDS):
            if link.startswith("/"):
                link = "https://coinmarketcap.com" + link

            return {
                "title": title,
                "link": link
            }

    return None
