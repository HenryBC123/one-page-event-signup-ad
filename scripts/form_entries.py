"""從 Google 表單的公開填寫網址，列出每一題的 entry ID 與選項文字。

用法：python3 form_entries.py <表單 viewform 網址>
報名網頁 landing.html 送出時要用這些 entry.xxx，選項文字也要一字不差。
"""
import json
import re
import sys
import urllib.request

url = sys.argv[1]
html = urllib.request.urlopen(url).read().decode("utf-8")
data = json.loads(re.search(r"FB_PUBLIC_LOAD_DATA_ = (.*?);</script>", html, re.S).group(1))

print("FORM_URL =", re.sub(r"/viewform.*$", "/formResponse", url))
for item in data[1][1]:
    if len(item) > 4 and item[4]:
        q = item[4][0]
        choices = [c[0] for c in (q[1] or [])] if len(q) > 1 else []
        print(f"entry.{q[0]}\t{item[1]}" + (f"\t選項：{choices}" if choices else ""))
