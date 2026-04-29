
from pathlib import Path
from utils_http import get_json_cached


def _extract_cvss_any(metrics: list) -> tuple[float | None, str | None]:
    """
    Cherche un score CVSS dans différentes variantes possibles (cvssV3_1, cvssV3_0, ...).
    Retourne (baseScore, baseSeverity).
    """
    if not metrics or not isinstance(metrics, list):
        return None, None

    for m in metrics:
        if not isinstance(m, dict):
            continue
        
        for k, v in m.items():
            if isinstance(k, str) and k.lower().startswith("cvss") and isinstance(v, dict):
                score = v.get("baseScore")
                sev = v.get("baseSeverity")
                return score, sev

    return None, None


def enrich_cve_mitre(
    cve_id: str,
    cache_dir: str = "cache/cve_mitre",
    delay: float = 1.0
) -> dict:
    url = f"https://cveawg.mitre.org/api/cve/{cve_id}"
    cache_path = Path(cache_dir) / f"{cve_id}.json"
    data = get_json_cached(url, cache_path, delay=delay)

    
    if data is None:
        return {
            "description": None,
            "cvss": None,
            "severity": None,
            "cwe": None,
            "cwe_desc": None,
            "affected": [],
            "mitre_url": url,
        }

    cna = data.get("containers", {}).get("cna", {})

    # Description
    description = None
    try:
        descs = cna.get("descriptions", [])
        if isinstance(descs, list) and descs:
            description = descs[0].get("value")
    except Exception:
        description = None

    # CVSS
    cvss, severity = _extract_cvss_any(cna.get("metrics", []))

    # CWE
    cwe = None
    cwe_desc = None
    try:
        pt = cna.get("problemTypes", [])
        if isinstance(pt, list) and pt:
            d0 = pt[0].get("descriptions", [{}])[0]
            cwe = d0.get("cweId")
            cwe_desc = d0.get("description")
    except Exception:
        pass

    # Produits affectés
    vendors_products = []
    try:
        affected = cna.get("affected", [])
        if isinstance(affected, list):
            for prod in affected:
                if not isinstance(prod, dict):
                    continue
                vendor = prod.get("vendor")
                product = prod.get("product")
                versions = []

                for v in prod.get("versions", []):
                    if isinstance(v, dict) and v.get("status") == "affected":
                        vv = v.get("version")
                        if vv:
                            versions.append(vv)

                vendors_products.append((vendor, product, versions))
    except Exception:
        pass

    return {
        "description": description,
        "cvss": cvss,
        "severity": severity,
        "cwe": cwe,
        "cwe_desc": cwe_desc,
        "affected": vendors_products,  # liste de tuples
        "mitre_url": url,
    }


def enrich_cve_epss(
    cve_id: str,
    cache_dir: str = "cache/cve_epss",
    delay: float = 1.0
) -> float | None:
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    cache_path = Path(cache_dir) / f"{cve_id}.json"
    data = get_json_cached(url, cache_path, delay=delay)

    
    if data is None:
        return None

    arr = data.get("data", [])
    if isinstance(arr, list) and arr:
        try:
            return float(arr[0].get("epss"))
        except Exception:
            return None

    return None


if __name__ == "__main__":
    # Petit test
    test = "CVE-2025-55125"  # peut être 404
    print(enrich_cve_mitre(test))
    print(enrich_cve_epss(test))
