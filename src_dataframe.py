import pandas as pd
from src_cve_enrichment import enrich_cve_mitre, enrich_cve_epss

def rows_from_bulletin(bulletin: dict, cves: list[str]) -> list[dict]:
    """
    Construit les lignes "à plat" :
    1 bulletin ANSSI -> N CVE -> N lignes.
    """
    rows = []
    for cve_id in cves:
        mitre = enrich_cve_mitre(cve_id)
        epss = enrich_cve_epss(cve_id)

        # affected peut contenir plusieurs produits -> on garde 1 ligne par cve (simple),
        # et on met vendor/product/versions concaténés. (on pourra normaliser plus tard)
        vendors = []
        products = []
        versions = []
        for vendor, product, vers in mitre.get("affected", []):
            if vendor: vendors.append(vendor)
            if product: products.append(product)
            if vers: versions.extend(vers)

        rows.append({
            "title_anssi": bulletin["title"],
            "type_bulletin": bulletin["type"],
            "date_publication": bulletin["published"],
            "cve": cve_id,
            "cvss": mitre.get("cvss"),
            "severity": mitre.get("severity"),
            "cwe": mitre.get("cwe"),
            "cwe_desc": mitre.get("cwe_desc"),
            "epss": epss,
            "link_anssi": bulletin["link"],
            "description": mitre.get("description"),
            "vendors": ", ".join(sorted(set(vendors))) if vendors else None,
            "products": ", ".join(sorted(set(products))) if products else None,
            "versions_affected": ", ".join(sorted(set(versions))) if versions else None,
        })

    return rows

def build_dataframe(all_rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(all_rows)
    df["cvss"] = pd.to_numeric(df["cvss"], errors="coerce")
    df["epss"] = pd.to_numeric(df["epss"], errors="coerce")
    return df
