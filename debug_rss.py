import feedparser

url = "https://www.cert.ssi.gouv.fr/alerte/feed"
feed = feedparser.parse(url)

print("bozo:", feed.bozo)  # 1 = erreur de parsing
print("bozo_exception:", repr(getattr(feed, "bozo_exception", None)))
print("status:", getattr(feed, "status", None))
print("href:", getattr(feed, "href", None))
print("entries:", len(feed.entries))
print("first_entry_keys:", list(feed.entries[0].keys()) if feed.entries else None)
