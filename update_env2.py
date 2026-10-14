# Akhri .env hadda jira
with open('.env', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ka saar Cloudflare variables haddii ay jiraan
lines = [l for l in lines if not l.startswith('CLOUDFLARE_')]

# Ku dar Cloudflare variables
lines.append("CLOUDFLARE_API_TOKEN=cfut_40YyoAbsSIw99AGdJORgopTJwTZvFwGYRl8DwpBfb87c1f29\n")
lines.append("CLOUDFLARE_ACCOUNT_ID=7d0d21fd2b1d22ec1fb646812f6f779d\n")
lines.append("CLOUDFLARE_WORKER_NAME=a\n")

with open('.env', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ .env la cusboonaysiiyay")
