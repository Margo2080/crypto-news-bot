import datetime

from notifier.forklog import get_strong_forklog_news
from notifier.rbc import get_strong_rbc_news
from notifier.coinmarketcap import get_strong_coinmarketcap_news
from notifier.moneyfest import get_strong_moneyfest_event

from notifier.telegram import send_telegram_message
from notifier.state import is_sent, mark_sent

# =========================
# НАСТРОЙКИ
# =========================

# Ночное окно (по ТВОЕМУ локальному времени)
NIGHT_START = 0   # 00:00
NIGHT_END = 7     # 07:00

# Ключевые слова для EMERGENCY (глобальных) новостей
EMERGENCY_KEYWORDS = [
    # Регуляторы и законы
    "sec", "cftc", "regulator", "regulation", "law",
    "закон", "регулятор", "запрет", "запрещ", "ban",
    "approval", "lawsuit",

    # Макроэкономика
    "fomc", "cpi", "inflation", "interest rate",
    "ставк", "ставки", "инфляц",

    # ETF и институционалы
    "etf", "spot etf",
    "blackrock", "fidelity", "vanguard",
    "institutional", "fund",

    # Рынок и риски
    "crash", "dump", "pump", "volatility",
    "крах", "обвал", "волатиль",

    # Банки и системные события
    "bank", "bankruptcy", "default",
    "банк", "банкрот", "дефолт",

    # Чрезвычайные события
    "emergency", "black swan",
    "черный лебедь"
]


# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def is_night_now() -> bool:
    now = datetime.datetime.now()
    return NIGHT_START <= now.hour < NIGHT_END


def is_emergency(text: str) -> bool:
    text_lower = text.lower()
    return any(word in text_lower for word in EMERGENCY_KEYWORDS)


# =========================
# ГЛОБАЛЬНЫЙ ЗАПУСК
# =========================

def main():
    print("🌍 Глобальный мониторинг запущен")

    night_mode = is_night_now()

    if night_mode:
        print("🌙 Сейчас НОЧЬ — разрешены ТОЛЬКО EMERGENCY новости")
    else:
        print("☀️ Сейчас ДЕНЬ — разрешены сильные и emergency новости")

    # Приоритет источников (СТРОГО)
    sources = [
        ("RBC", get_strong_rbc_news),
        ("Forklog", get_strong_forklog_news),
        ("CoinMarketCap", get_strong_coinmarketcap_news),
        ("Moneyfest", get_strong_moneyfest_event),
    ]

    for source_name, getter in sources:
        try:
            result = getter()
        except Exception as e:
            print(f"⚠️ Ошибка источника {source_name}: {e}")
            continue

        if not result:
            continue

        title = result.get("title", "")
        link = result.get("link", "")

        if not title or not link:
            continue

        # Проверка повторов
        if is_sent(source_name, link):
            print(f"⏭ Уже отправляли: {source_name}")
            continue

        emergency = is_emergency(title)

        # Логика ночь / день
        if night_mode and not emergency:
            print(f"🌙 Пропуск (не emergency): {source_name}")
            continue

        # Формируем сообщение
        prefix = "🚨 EMERGENCY" if emergency else "🔥 СИЛЬНАЯ НОВОСТЬ"

        message = (
            f"{prefix}\n\n"
            f"Источник: {source_name}\n\n"
            f"{title}\n\n"
            f"{link}"
        )

        send_telegram_message(message)

        # ❗ ВАЖНО: сохраняем СО СOURCE + LINK
        mark_sent(source_name, link)

        print(f"📨 Отправлена глобальная новость ({source_name})")

        # ГАРАНТИЯ: только одно сообщение за запуск
        return

    print("📭 Нет подходящих глобальных новостей")


if __name__ == "__main__":
    main()
