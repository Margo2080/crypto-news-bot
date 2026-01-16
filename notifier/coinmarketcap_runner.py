import json
import os
import time

from notifier.coinmarketcap import get_strong_coinmarketcap_news
from notifier.telegram import send_telegram_message

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def run():
    print("▶ Автомат CoinMarketCap запущен")
    state = load_state()

    news = get_strong_coinmarketcap_news()

    if not news:
        print("— Нет сильных новостей CoinMarketCap")
        return

    last_link = state.get("coinmarketcap_last_link")

    if news["link"] == last_link:
        print("— Новость уже отправлялась")
        return

    message = (
        "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (CoinMarketCap)</b>\n\n"
        f"📰 {news['title']}\n\n"
        f"🔗 {news['link']}\n\n"
        "⚠️ Возможное влияние на рынок."
    )

    send_telegram_message(message)

    state["coinmarketcap_last_link"] = news["link"]
    save_state(state)

    print("✓ Отправлена новая сильная новость CoinMarketCap")

if __name__ == "__main__":
    run()
