import shutil

shutil.copy('public/index.html', 'public/index.html.safe14')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tallaabo 1: Tirtir fulIname:f, (khaladka ugu weyn)
count1 = c.count("fulIname:f,")
if count1 > 0:
    c = c.replace("fulIname:f,", "")
    print(f"1. fulIname:f, la tirtiray: {count1} meelood")
else:
    print("1. fulIname:f, LAMA HELIN")

# Tallaabo 2: Tirtir fullname:f, (haddii uu jiro)
count2 = c.count("fullname:f,")
if count2 > 0:
    c = c.replace("fullname:f,", "")
    print(f"2. fullname:f, la tirtiray: {count2} meelood")
else:
    print("2. fullname:f, LAMA HELIN")

# Tallaabo 3: Tirtir var f=document.getElementById('reg-fullname').value;
count3 = c.count("var f=document.getElementById('reg-fullname').value;")
if count3 > 0:
    c = c.replace("var f=document.getElementById('reg-fullname').value;", "")
    print(f"3. var f la tirtiray: {count3} meelood")
else:
    print("3. var f LAMA HELIN")

# Tallaabo 4: Tirtir fulIname f (haddii uu jiro - spaces)
count4 = c.count("fulIname:f")
if count4 > 0:
    c = c.replace("fulIname:f", "")
    print(f"4. fulIname:f (spaces): {count4} meelood")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe14")
