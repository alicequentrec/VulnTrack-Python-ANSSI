import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output/data.csv")

# Nettoyage
df["cvss"] = pd.to_numeric(df["cvss"], errors="coerce")
df["epss"] = pd.to_numeric(df["epss"], errors="coerce")
df = df.dropna(subset=["cvss", "epss"])

# 1) Histogramme CVSS
plt.figure(figsize=(8,4))
plt.hist(df["cvss"], bins=20)
plt.title("Distribution des scores CVSS")
plt.xlabel("CVSS")
plt.ylabel("Nombre de CVE")
plt.show()

# 2) Histogramme EPSS
plt.figure(figsize=(8,4))
plt.hist(df["epss"], bins=20)
plt.title("Distribution des scores EPSS")
plt.xlabel("EPSS")
plt.ylabel("Nombre de CVE")
plt.show()

# 3) Nuage de points CVSS vs EPSS
plt.figure(figsize=(8,5))
plt.scatter(df["cvss"], df["epss"], alpha=0.5)
plt.title("CVSS vs EPSS")
plt.xlabel("CVSS")
plt.ylabel("EPSS")
plt.show()

# 4) Top 10 vendors les plus impactés
top_vendors = df["vendor"].fillna("Unknown").value_counts().head(10)
plt.figure(figsize=(9,4))
plt.bar(top_vendors.index, top_vendors.values)
plt.title("Top 10 éditeurs les plus impactés")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Nombre de CVE")
plt.show()

# 5) Top 10 produits les plus impactés
top_products = df["product"].fillna("Unknown").value_counts().head(10)
plt.figure(figsize=(9,4))
plt.bar(top_products.index, top_products.values)
plt.title("Top 10 produits les plus impactés")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Nombre de CVE")
plt.show()

# 6) Evolution temporelle (CVE / jour)
df["date_publication"] = pd.to_datetime(df["date_publication"], errors="coerce")
by_day = df.dropna(subset=["date_publication"]).groupby(df["date_publication"].dt.date)["cve"].count()

plt.figure(figsize=(10,4))
plt.plot(by_day.index, by_day.values)
plt.title("Nombre de CVE par jour (selon bulletins ANSSI)")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Nombre de CVE")
plt.show()
