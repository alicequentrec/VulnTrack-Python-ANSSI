from pathlib import Path
from src_rss import fetch_rss
from src_anssi_json import fetch_anssi_json, extract_cves
from src_dataframe import rows_from_bulletin, build_dataframe

def main(n_bulletins=5, max_cves_per_bulletin=15):
    bulletins = fetch_rss("avis") + fetch_rss("alerte")
    bulletins.sort(key=lambda x: x["published"], reverse=True)
    bulletins = bulletins[:n_bulletins]

    all_rows = []

    for b in bulletins:
        data = fetch_anssi_json(b["link"])
        cves = extract_cves(data)[:max_cves_per_bulletin]  # limite test
        all_rows.extend(rows_from_bulletin(b, cves))

    df = build_dataframe(all_rows)

    Path("output").mkdir(exist_ok=True)
    df.to_csv("output/data.csv", index=False, encoding="utf-8")
    print("CSV généré: output/data.csv")
    print(df.head(10))

if __name__ == "__main__":
    main()
