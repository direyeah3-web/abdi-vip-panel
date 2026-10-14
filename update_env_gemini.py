new_key = "AQ.Ab8RN6LIKQOlkmyF56Orb9lHNbnqLkCsD-m_1eQgkYd2v3DYTQ"

with open('.env', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = [l for l in lines if not l.startswith('GEMINI_')]
lines.append(f"GEMINI_API_KEY={new_key}\n")

with open('.env', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Gemini API Key la geliyay .env")
