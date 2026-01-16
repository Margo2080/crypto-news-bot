import time
import json
from pathlib import Path

from notifier.rbc import get_strong_rbc_news
from notifier.telegram import send_telegram_message

# ===== НАСТРОЙКИ =====
CHECK_INTERVAL = 30 * 60  # 30 минут
STATE_FILE = Path(__file__).parent / "state.json"


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run_rbc_auto():
    print("🔔 Автомат RBC запущен")
    state = load_state()

    last_rbc_link = state.get("rbc_last_link")

    while True:
        try:
            news = get_strong_rbc_news()

            if not news:
                print("— Нет сильных новостей РБК")
            else:
                if news["link"] != last_rbc_link:
                    message = (
                        "🚨 <b>СИЛЬНАЯ КРИПТОНОВОСТЬ (РБК)</b>\n\n"
                        f"📰 <b>{news['title']}</b>\n\n"
                        f"🔗 {news['link']}\n\n"
                        "⚠️ Новость может вызвать сильную волатильность рынка."
                    )

                    send_telegram_message(message)
                    print("✅ Отправлена новая сильная новость РБК")

                    state["rbc_last_link"] = news["link"]
                    save_state(state)
                else:
                    print("— Новость уже отправлялась")

        except Exception as e:
            print(f"❌ Ошибка в автомате РБК: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_rbc_auto()
