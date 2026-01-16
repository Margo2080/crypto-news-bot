import time
import json
from datetime import datetime

from notifier.forklog import get_strong_forklog_news
from notifier.telegram import send_telegram_message

STATE_FILE = "notifier/state.json"
CHECK_INTERVAL = 30 * 60  # 30 минут

# Ключевые слова для НОЧНЫХ супер-новостей
NIGHT_KEYWORDS = [
    "etf", "sec", "регулятор", "запрет",
    "одобрил", "крах", "обвал", "резкое падение"
]


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_forklog_link": None}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_night():
    hour = datetime.now().hour
    return hour >= 23 or hour < 8


def is_night_important(title: str) -> bool:
    title_lower = title.lower()
    return any(word in title_lower for word in NIGHT_KEYWORDS)


def run():
    print("▶ Автомат Forklog запущен")

    while True:
        try:
            state = load_state()
            last_link = state.get("last_forklog_link")

            news = get_strong_forklog_news()

            if not news:
                print("— Нет сильных новостей Forklog")
            else:
                title = news["title"]
                link = news["link"]

                if link == last_link:
                    print("— Новость уже отправлялась")
                else:
                    if is_night() and not is_night_important(title):
                        print("🌙 Ночь — новость не глобальная, пропускаем")
                    else:
                        message = (
                            "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (Forklog)</b>\n\n"
                            f"📰 {title}\n\n"
                            f"🔗 {link}\n\n"
                            "⚠ Может вызвать резкую волатильность рынка."
                        )

                        send_telegram_message(message)
                        print("✅ Новость отправлена")

                        state["last_forklog_link"] = link
                        save_state(state)

        except Exception as e:
            print(f"❌ Ошибка Forklog автомата: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
