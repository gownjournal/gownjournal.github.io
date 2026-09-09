import re, glob, sys
bad = ["delve","elevate","leverage","serves as","a testament","dream dress","big day","special day","stunning","breathtaking","it's important to note","in conclusion","ultimately","look no further","timeless elegance","whether you're"]
issues = 0
for f in sorted(glob.glob("src/posts/*.md") + glob.glob("src/*.md") + glob.glob("src/*.njk") + glob.glob("src/_includes/*.njk")):
    t = open(f, encoding="utf-8").read()
    for i, line in enumerate(t.splitlines(), 1):
        if "—" in line or "–" in line:
            print(f"{f}:{i}: long dash"); issues += 1
        low = line.lower()
        for b in bad:
            if re.search(r"\b" + re.escape(b) + r"\b", low):
                print(f"{f}:{i}: '{b}'"); issues += 1
        if re.search(r"[£$€]\s?\d|\d\s?(USD|EUR|GBP|ILS|₪)", line):
            print(f"{f}:{i}: price?"); issues += 1
print("issues:", issues)
