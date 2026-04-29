import requests
print(requests.get("https://www.cert.ssi.gouv.fr/alerte/feed", timeout=10).status_code)
print(requests.get("https://www.cert.ssi.gouv.fr/alerte/feed", timeout=10).text[:200])
