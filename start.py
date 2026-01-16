import time
from notifier.global_runner import main

print("🚀 Global crypto news bot started")

while True:
    try:
        main()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    # 30 минут
    time.sleep(1800)
