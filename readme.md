# README – Projet Python ANSSI / CVE / Alertes
 
---
 
## 1. Description générale
 
Ce projet Python automatise la veille de vulnérabilités publiées par le **CERT-FR (ANSSI)**.
Il inclut :
 
- Récupération des flux RSS **Avis** et **Alertes** ;
- Extraction automatique des identifiants **CVE** contenus dans les bulletins ;
- Enrichissement des CVE via :
  - l’**API MITRE CVE** (description, CVSS, CWE, produits affectés) ;
  - l’**API EPSS** (probabilité d’exploitation) ;
- Construction d’un **fichier CSV** complet pour l’analyse ;
- Visualisations (CVSS, EPSS, vendors, produits, timeline) ;
- Génération d’alertes selon des règles de risque ;
- Envoi optionnel d’un **email d’alerte** via SMTP.
 
Ce pipeline est conçu pour fournir une veille sécurité automatisée utilisable dans un contexte académique ou SOC.
 
---
 
## 2. Pré-requis
 
### 2.1. Système et Python
 
- **Python 3.10 ou supérieur**
- Accès Internet vers :
  - les flux RSS ANSSI ;
  - l’API MITRE : [https://cveawg.mitre.org](https://cveawg.mitre.org) ;
  - l’API EPSS : [https://api.first.org](https://api.first.org) ;
- Optionnel : compte email (Gmail ou autre SMTP)
 
### 2.2. Dépendances Python
 
Modules utilisés :
 
feedparser
requests
pandas
matplotlib
seaborn
plotly
tqdm
 
### 2.3. Environnement virtuel
 
python -m venv venv
 
# Windows
venv\Scripts\activate
 
# Linux / macOS
source venv/bin/activate
 
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
 
#### 3. Organisation du projet
 
Projet/
├── code/
│   ├── src_rss.py
│   ├── src_anssi_json.py
│   ├── src_cve_enrichment.py
│   ├── src_dataframe.py
│   ├── src_visualization.py
│   ├── utils_http.py
│   ├── build_csv.py
│   ├── main_build_csv.py
│   ├── alerts.py
│   ├── alerts_and_mail.py
│
├── output/
│   ├── data.csv
│   ├── alertes.csv
│
└── cache/
    ├── cve_mitre/
    ├── cve_epss/
 
code/ : scripts sources du pipeline
output/ : fichiers générés
cache/ : réponses API MITRE/EPSS mises en cache
 
### 4. Utilisation avec Visual Studio Code
 
# 4.1. Ouvrir le projet
 
Lancer VS Code
Menu File → Open Folder…
Sélectionner le dossier du projet
 
# 4.2. Sélectionner l’interpréteur Python
 
Installer l’extension Python de Microsoft
Ctrl + Shift + P → Python: Select Interpreter
Choisir l’environnement virtuel venv ou Python 3.x global
 
# 4.3. Terminal intégré
 
cd code
python main_build_csv.py
 
# 4.4. Debug (optionnel)
 
VS Code permet :
d’ajouter des breakpoints ;
d’exécuter les scripts pas à pas ;
de visualiser les variables internes.
 
### 5. Étapes pour lancer l’application
# 5.1. Récupération et enrichissement des données
 
cd code
python main_build_csv.py
 
Le script :
télécharge les flux RSS ;
récupère les données JSON ;
extrait les CVE ;
enrichit via MITRE + EPSS ;
génère output/data.csv.
 
# 5.2. Visualisation des données
 
python src_visualization.py
Graphiques générés :
distribution CVSS ;
distribution EPSS ;
scatterplot CVSS vs EPSS ;
top vendors / produits ;
timeline des vulnérabilités.
 
# 5.3. Génération d’alertes
python alerts.py
 
### 6. Configuration SMTP
 
# 6.1. Gmail
 
Pour envoyer des emails :
Activer la double authentification.
Créer un mot de passe d’application.
Configurer dans le script :
 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "votre_email@gmail.com"
SENDER_PASSWORD = "mot_de_passe_application"
 
# 6.2. Bonne pratique de sécurité
Ne jamais committer un mot de passe dans Git.
Utiliser des variables d’environnement ou un fichier .env non versionné.