from notifier.forklog import get_strong_forklog_news
from notifier.telegram import send_telegram_message


def main():
    news = get_strong_forklog_news()

    if not news:
        send_telegram_message("ℹ️ Сейчас нет сильных новостей Forklog.")
        return

    message = (
        "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (Forklog)</b>\n\n"
        f"📰 <b>{news['title']}</b>\n\n"
        f"🔗 {news['link']}\n\n"
        "⚠️ Новость может вызвать высокую волатильность рынка."
    )

    send_telegram_message(message)


if __name__ == "__main__":
    main()
