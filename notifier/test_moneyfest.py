from notifier.moneyfest import get_strong_moneyfest_event
from notifier.telegram import send_telegram_message

def main():
    print("📅 Тест Moneyfest запущен")

    event = get_strong_moneyfest_event()

    if not event:
        print("— Сегодня нет сильных макро-событий")
        return

    message = (
        "🚨 СИЛЬНОЕ МАКРО-СОБЫТИЕ\n\n"
        f"{event['title']}\n"
        f"Дата: {event['date']}\n\n"
        "⚠ Может вызвать резкую волатильность рынка"
    )

    send_telegram_message(message)
    print("✔ Макро-событие отправлено")

if __name__ == "__main__":
    main()
