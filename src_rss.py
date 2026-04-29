import feedparser
import requests
from datetime import datetime

ANSSI_RSS = {
    # on tente d'abord cert.ssi.gouv.fr (souvent canonical), puis www.cert...
    "avis": [
        "https://cert.ssi.gouv.fr/avis/feed/",
        "https://www.cert.ssi.gouv.fr/avis/feed/",
    ],
    "alerte": [
        "https://cert.ssi.gouv.fr/alerte/feed/",
        "https://www.cert.ssi.gouv.fr/alerte/feed/",
    ],
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ANSSI-RSS-StudentProject/1.0"

def parse_date_struct(published_parsed):
    try:
        if published_parsed:
            return datetime(*published_parsed[:6])
    except Exception:
        pass
    return None

def _fetch_feed_content(url: str) -> bytes: #Télécharge le contenu d'un flux RSS
    r = requests.get(url, headers={"User-Agent": UA}, timeout=20, allow_redirects=True)
    r.raise_for_status()
    return r.content

def fetch_rss(rss_type: str) -> list[dict]: #Récupère un flux RSS (avis ou alerte) et retourne la liste des bulletins
    if rss_type not in ANSSI_RSS:
        raise ValueError("rss_type doit être 'avis' ou 'alerte'")

    last_err = None
    for url in ANSSI_RSS[rss_type]: ## Essaie chaque URL disponible
        try: 
            content = _fetch_feed_content(url)
            feed = feedparser.parse(content)

            # bozo=0 et entries non vides => OK
            if getattr(feed, "bozo", 0) == 0 and len(feed.entries) > 0:
                entries = []
                for entry in feed.entries: # Extrait les informations importantes de chaque entrée
                    entries.append({
                        "id_anssi": entry.get("id", ""),
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "published": parse_date_struct(entry.get("published_parsed")),
                        "type": rss_type,
                    })
                return entries

            last_err = f"Flux invalide: bozo={getattr(feed,'bozo',None)} entries={len(feed.entries)} url={url}"
        except Exception as e:
            last_err = f"{url} -> {e!r}"

    raise RuntimeError(f"Aucun flux RSS valide trouvé. Dernière erreur: {last_err}")

if __name__ == "__main__":
    for t in ("avis", "alerte"):
        try:
            data = fetch_rss(t)
            print(t, "OK :", len(data), "entrées")
            print("Ex:", data[0]["title"])
        except Exception as e:
            print(t, "ECHEC :", e)
