import requests
from bs4 import BeautifulSoup

FORKLOG_URL = "https://forklog.com/news"

# КЛЮЧЕВЫЕ СЛОВА — ТОЛЬКО СИЛЬНЫЕ ТРИГГЕРЫ РЫНКА
STRONG_KEYWORDS = [
    "bitcoin",
    "btc",
    "etf",
    "sec",
    "регулятор",
    "запрет",
    "разрешил",
    "одобрил",
    "fomc",
    "ставк",
    "инфляц",
    "cpi",
    "фрс",
    "черный лебедь",
    "обвал",
    "крах",
    "резкое падение",
    "резкий рост"
]


def get_strong_forklog_news():
    """
    Возвращает одну СИЛЬНУЮ новость Forklog или None
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(FORKLOG_URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")
    if not articles:
        return None

    for article in articles:
        title_tag = article.find("h2")
        link_tag = article.find("a")

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag.get("href")

        title_lower = title.lower()

        # Проверка на СИЛЬНЫЕ ключевые слова
        if any(word in title_lower for word in STRONG_KEYWORDS):
            return {
                "title": title,
                "link": link
            }

    return None
