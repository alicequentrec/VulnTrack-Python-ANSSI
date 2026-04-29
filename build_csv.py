from pathlib import Path
import pandas as pd
from tqdm import tqdm

from src_rss import fetch_rss
from src_anssi_json import fetch_anssi_json, extract_cves
from src_cve_enrichment import enrich_cve_mitre, enrich_cve_epss
from email.mime.text import MIMEText
import smtplib

def send_email(to_email, subject, body):
    from_email = "john.doe.securite.esilv@gmail.com"
    password = "qgdbcbrnlrpfaldv"
    
    try:
        msg = MIMEText(body)
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        
        print(f"Email envoyé à {to_email}") 
    except Exception as e:
        print(f"Erreur: {str(e)}") 

OUT_PATH = "output/data.csv"

def build_csv(
    n_bulletins=80,
    max_cves_per_bulletin=200
):
    # 1) Récupération et tri des bulletins
    bulletins = fetch_rss("avis") + fetch_rss("alerte")
    bulletins.sort(key=lambda x: x["published"], reverse=True)
    bulletins = bulletins[:n_bulletins]

    rows = []

    print(f"Bulletins traités : {len(bulletins)}")

    # 2) Traitement bulletin par bulletin
    for b in tqdm(bulletins, desc="Bulletins"):
        try:
            data = fetch_anssi_json(b["link"])
            cves = extract_cves(data)[:max_cves_per_bulletin]
        except Exception as e:
            print("Erreur bulletin:", b["link"], e)
            continue

        # 3) Enrichissement CVE par CVE
        for cve_id in cves:
            try:
                mitre = enrich_cve_mitre(cve_id)
                epss = enrich_cve_epss(cve_id)
            except Exception as e:
                print("Erreur CVE:", cve_id, e)
                continue

            rows.append({
                "title_anssi": b["title"],
                "type_bulletin": b["type"],
                "date_publication": b["published"],
                "cve": cve_id,
                "cvss": mitre.get("cvss"),
                "severity": mitre.get("severity"),
                "cwe": mitre.get("cwe"),
                "epss": epss,
                "link_anssi": b["link"],
                "description": mitre.get("description"),
                "vendor": mitre.get("vendors"),
                "product": mitre.get("affected"),
                "versions_affected": mitre.get("versions_affected"),
                "mitre_url": mitre.get("mitre_url"),
            })

    # 4) DataFrame final
    df = pd.DataFrame(rows)
    df["cvss"] = pd.to_numeric(df["cvss"], errors="coerce")
    df["epss"] = pd.to_numeric(df["epss"], errors="coerce")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")

    print("\nCSV FINAL GÉNÉRÉ")
    print("Fichier :", OUT_PATH)
    print("Lignes :", len(df))
    print(df.head(5))


    critical_cves = df[(df["cvss"] >= 7) & (df["epss"] >= 0.7)] #gardes seulement les CVE qui sont à la fois graves ET en danger d'être exploitées
    
    if not critical_cves.empty:
        print(f"{len(critical_cves)} CVE(s) critique(s)\n")
        
        # Construire UN SEUL email avec tous les CVE
        subject = f"ALERTE: {len(critical_cves)} vulnérabilités critiques détectées"
        body = "Vulnérabilités critiques détectées:\n\n"
        
        for idx, row in critical_cves.iterrows():
            # Extraire les produits de la liste de tuples
            affected = row['product']
            if isinstance(affected, list) and len(affected) > 0:
                product = ", ".join([f"{v} {p}" for v, p, _ in affected if v and p])
            else:
                product = "Produit inconnu"
            
            description = row['description'] if pd.notna(row['description']) else "Description non disponible"
            body += f"CVE: {row['cve']}\nProduit: {product}\nScore CVSS: {row['cvss']}/10\nDescription: {description}\n\n"
        # Envoyer UN SEUL email
        send_email("jane.smith.esilv.2026@gmail.com", subject, body)
        print(f"Email envoyé avec {len(critical_cves)} CVE(s)")
    else:
        print("Aucun CVE critique")

if __name__ == "__main__":
    build_csv(
        n_bulletins=80,
        max_cves_per_bulletin=200
    )


