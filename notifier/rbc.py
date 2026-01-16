import requests
from bs4 import BeautifulSoup

RBC_CRYPTO_URL = "https://www.rbc.ru/crypto/"

# 🔴 ТОЛЬКО СИЛЬНЫЕ МАКРО / РЕГУЛЯТОРНЫЕ ТРИГГЕРЫ
STRONG_KEYWORDS = [
    "bitcoin",
    "btc",
    "etf",
    "sec",
    "регулятор",
    "запрет",
    "разрешил",
    "одобрил",
    "закон",
    "суд",
    "санкц",
    "фрс",
    "fomc",
    "ставк",
    "инфляц",
    "cpi",
    "обвал",
    "крах",
    "резкое падение",
    "резкий рост",
    "черный лебедь",
    "государств",
    "центробанк",
]


def get_strong_rbc_news():
    """
    Возвращает одну СИЛЬНУЮ новость RBC Crypto или None
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(RBC_CRYPTO_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", class_="item__link")
    if not articles:
        return None

    for article in articles:
        title = article.get_text(strip=True)
        link = article.get("href")

        if not title or not link:
            continue

        title_lower = title.lower()

        # 🔍 ФИЛЬТР ТОЛЬКО СИЛЬНЫХ НОВОСТЕЙ
        if any(word in title_lower for word in STRONG_KEYWORDS):
            if link.startswith("/"):
                link = "https://www.rbc.ru" + link

            return {
                "title": title,
                "link": link
            }

    return None
