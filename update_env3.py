new_token = "cfut_utB2tDXCqW7qhegPhL0U32kY42IGtn2twwU3FE2n253eec6a"

with open('.env', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = [l for l in lines if not l.startswith('CLOUDFLARE_API_TOKEN=')]
lines.append(f"CLOUDFLARE_API_TOKEN={new_token}\n")

with open('.env', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Token cusub la geliyay")
