from notifier.global_runner import main

print("🚀 Crypto news bot run started")

try:
    main()
    print("✅ Run completed successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    raise
