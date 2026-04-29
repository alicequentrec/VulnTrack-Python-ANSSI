import requests

urls = [
    "https://www.cert.ssi.gouv.fr/alerte/feed",
    "https://www.cert.ssi.gouv.fr/alerte/feed/",
    "https://cert.ssi.gouv.fr/alerte/feed",
    "https://cert.ssi.gouv.fr/alerte/feed/",
]

for u in urls:
    r = requests.get(u, allow_redirects=True, timeout=15)
    print("\nURL:", u)
    print("Final:", r.url)
    print("Status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))
    print("First chars:", r.text[:60].replace("\n"," "))
