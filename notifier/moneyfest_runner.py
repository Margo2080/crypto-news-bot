from notifier.moneyfest import get_strong_moneyfest_event
from notifier.telegram import send_telegram_message
from notifier.state import is_new_event, save_event

def main():
    print("🚀 Автомат Moneyfest запущен")

    event = get_strong_moneyfest_event()
    if not event:
        print("— Нет глобальных макро-событий")
        return

    event_id = event["id"]

    if not is_new_event("moneyfest", event_id):
        print("— Событие уже отправлялось")
        return

    message = (
        "🚨 <b>ГЛОБАЛЬНОЕ МАКРО-СОБЫТИЕ</b>\n\n"
        f"<b>{event['title']}</b>\n"
        f"Валюта: {event['currency']}\n"
        f"Время: {event['time']}\n"
        f"Важность: {event['impact']}"
    )

    send_telegram_message(message)
    save_event("moneyfest", event_id)

    print("📨 Отправлено глобальное событие Moneyfest")

if __name__ == "__main__":
    main()
