import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str):
    """
    Отправка сообщения в Telegram через HTTP API
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    response = requests.post(url, data=payload, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Ошибка Telegram API: {response.status_code} | {response.text}"
        )
