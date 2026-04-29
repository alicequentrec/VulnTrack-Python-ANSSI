from src_rss import fetch_rss
from src_anssi_json import fetch_anssi_json, extract_cves
from build_csv import build_csv
from src_visualization import *

def main(n=5):
    # Récupère tous les bulletins d'avis et d'alertes
    all_items = fetch_rss("avis") + fetch_rss("alerte")
    # Trie par date (les plus récents d'abord)
    all_items.sort(key=lambda x: x["published"], reverse=True)

    # Affiche le nombre total de bulletins
    print(f"Total bulletins: {len(all_items)}")
    # Récupère les n premiers bulletins
    items = all_items[:n]

    # Parcourt chaque bulletin
    for i, it in enumerate(items, start=1):
        print(f"\n--- Bulletin {i}/{n} ---")
        print("Type :", it["type"])
        print("Date :", it["published"])
        print("Titre:", it["title"])
        print("Lien :", it["link"])

        try:
            # Récupère les données JSON du bulletin
            data = fetch_anssi_json(it["link"])
            # Extrait les CVEs
            cves = extract_cves(data)
            # Affiche le nombre de CVEs et les 8 premières
            print("CVE:", len(cves), "-", cves[:8])
        except Exception as e:
            # Gère les erreurs
            print("Erreur JSON/CVE:", e)

if __name__ == "__main__":
    main(5) 
    print("Affichage des alertes et envoie d'email")
    build_csv()