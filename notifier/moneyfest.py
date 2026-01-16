from datetime import datetime
from notifier.telegram import send_telegram_message

# Ключевые макро-события
MACRO_EVENTS = {
    "cpi": "📉 CPI (Инфляция США)",
    "fomc": "🏦 FOMC / Решение ФРС",
    "interest rate": "📊 Процентная ставка",
    "rate decision": "📊 Решение по ставке",
    "non-farm": "👷 Non-Farm Payrolls",
    "unemployment": "👥 Безработица США"
}

# Ручной список важных дат (можно расширять)
IMPORTANT_DATES = {
    # формат: YYYY-MM-DD
    # пример:
    # "2026-01-31": "📉 CPI (Инфляция США)"
}

def get_strong_moneyfest_event():
    """
    Возвращает сильное макро-событие или None
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if today in IMPORTANT_DATES:
        return {
            "title": IMPORTANT_DATES[today],
            "date": today
        }

    return None
