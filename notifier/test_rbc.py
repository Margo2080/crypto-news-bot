from notifier.rbc import get_strong_rbc_news
from notifier.telegram import send_telegram_message


def main():
    news = get_strong_rbc_news()

    if not news:
        send_telegram_message("ℹ️ Сильных макро/регуляторных новостей РБК сейчас нет.")
        return

    message = (
        "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (РБК)</b>\n\n"
        f"📰 {news['title']}\n\n"
        f"🔗 {news['link']}\n\n"
        "⚠️ Новость может вызвать резкую волатильность рынка."
    )

    send_telegram_message(message)


if __name__ == "__main__":
    main()
