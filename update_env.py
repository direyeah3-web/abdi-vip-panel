new_token = "8006326548:AAFPhCrZLrJBR8eUNZYAbwFcU-NDI-3d-Kc"
chat_id = "6898834443"

with open('.env', 'w', encoding='utf-8') as f:
    f.write(f"TELEGRAM_BOT_TOKEN={new_token}\n")
    f.write(f"TELEGRAM_ADMIN_CHAT_ID={chat_id}\n")

print("✅ .env la cusboonaysiiyay")
print(f"Token: {new_token[:20]}...")
