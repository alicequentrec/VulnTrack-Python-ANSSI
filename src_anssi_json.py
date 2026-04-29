import requests
import re
import time

CVE_REGEX = r"CVE-\d{4}-\d{4,7}"

def fetch_anssi_json(bulletin_url: str, delay: float = 2.0) -> dict:
    """
    Télécharge le JSON d'un bulletin ANSSI
    """
    json_url = bulletin_url.rstrip("/") + "/json/"
    response = requests.get(json_url, timeout=10)
    response.raise_for_status()

    time.sleep(delay)  # Respect ANSSI
    return response.json()


def extract_cves(data: dict) -> list[str]:
    """
    Extraction robuste des CVE depuis le JSON
    """
    cves = set()

    # Méthode officielle
    for cve in data.get("cves", []):
        if "name" in cve:
            cves.add(cve["name"])

    # Fallback regex (sécurité)
    found = re.findall(CVE_REGEX, str(data))
    cves.update(found)

    return sorted(cves)
