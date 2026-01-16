from notifier.coinmarketcap import get_strong_coinmarketcap_news
from notifier.telegram import send_telegram_message

def main():
    news = get_strong_coinmarketcap_news()

    if not news:
        send_telegram_message("ℹ️ Сейчас нет сильных новостей CoinMarketCap.")
        return

    message = (
        "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (CoinMarketCap)</b>\n\n"
        f"📰 {news['title']}\n\n"
        f"🔗 {news['link']}\n\n"
        "⚠️ Возможное влияние на рынок."
    )

    send_telegram_message(message)

if __name__ == "__main__":
    main()
