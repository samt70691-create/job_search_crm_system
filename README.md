# Job Search CRM Final

## Démarrage rapide

### 1) Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2) Lancer l'initialisation complète
```bash
python -m src.pipelines.run_full_setup
```

### 3) Lancer l'application
```bash
streamlit run app.py
```

## Ce que le système inclut
- Dashboard prêt à l'emploi
- Offres avec scoring personnalisé
- Candidatures avec relances
- Contacts
- Masters / formations
- Export Excel
- Rapport texte synthétique
- Profil candidat préchargé
- Données de démonstration prêtes

## Fichiers utiles
- `data/app.db`
- `data/exports/job_offers.xlsx`
- `data/exports/system_report.txt`

## Déploiement
L'application peut être déployée sur Streamlit Community Cloud via GitHub. Ajouter les secrets/API dans la configuration Streamlit si besoin.
