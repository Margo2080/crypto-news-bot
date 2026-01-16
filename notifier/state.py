import json
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_new_event(source: str, event_id: str) -> bool:
    """
    True — если событие новое
    """
    state = load_state()
    last_id = state.get(source)
    return last_id != event_id


def save_event(source: str, event_id: str):
    """
    Сохраняет событие как последнее отправленное
    """
    state = load_state()
    state[source] = event_id
    save_state(state)


# --- Алиасы для глобального раннера (совместимость с ТЗ) ---

def is_sent(source: str, event_id: str) -> bool:
    """
    True — если событие уже отправлялось
    """
    return not is_new_event(source, event_id)


def mark_sent(source: str, event_id: str):
    """
    Помечает событие как отправленное
    """
    save_event(source, event_id)
