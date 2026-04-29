import json
import time
from pathlib import Path
import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ANSSI-RSS-StudentProject/1.0"


def get_json_cached(url: str, cache_path: Path, delay: float = 1.0) -> dict | None:
    """
    GET JSON + cache disque.
    Retourne None si 404 (ressource absente), et met un cache d'erreur
    pour éviter de requêter encore.
    """
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    r = requests.get(url, headers={"User-Agent": UA}, timeout=20, allow_redirects=True)

    if r.status_code == 404:
        cache_path.write_text(
            json.dumps({"_error": 404, "_url": url}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        time.sleep(delay)
        return None

    r.raise_for_status()

    data = r.json()
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(delay)
    return data

