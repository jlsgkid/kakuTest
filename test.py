from urllib.request import urlopen
import ssl
import urllib

url1 = "https://www.av01.tv/"

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36)'
}
req=urllib.request.Request(url=url1, headers=headers1)
# resp = urlopen(url)
resp2 = urlopen(req).read().decode("utf-8")
print(resp2)
with open("bdtxt.html", mode="w", encoding="utf-8") as f:
    f.write(resp2)
"""
print(resp.read().decode("utf-8"))

with open("bdtxt.html", mode="w", encoding="utf-8") as f:
    f.write(resp.read().decode("utf-8"))
"""