# Obsidian Notes — E-Cantine Dashboard

## Variables clés
- **repo** : https://github.com/magi22/ecantine-dashboard
- **branche** : main
- **dernier commit** : 66b3615 — fix TypeError Plotly Cloud PLOTLY_PIE
- **app principale** : app.py
- **modèle** : predict.py
- **déploiement** : Streamlit Cloud (share.streamlit.io)
- **auteur** : Adote Mario-Giovani ADUAYI-AKUE · ISM Dakar · 2025

## Variables modèle économique (DEFAULT_PARAMS)
- Commission Starter : 2,5% · Pro : 2,0% · Premium : 1,0%
- Frais livraison moy : 1 200 FCFA · Marge : 40%
- Panier moyen : 3 000 FCFA · 2,5 cmd/MAU/mois
- Investissement : 22,56M FCFA · Taux actualisation : 15%
- MAU plateau central : 80 000 · k=0.10 · t0=36

## Checklist déploiement
- [x] predict.py importable sans erreur
- [x] app.py sans font=dict(weight=N)
- [x] PLOTLY_PIE utilisé pour go.Pie
- [x] requirements.txt à jour
- [x] .streamlit/config.toml base=light
- [x] assets/logo_blue.svg présent
- [x] git remote origin configuré
- [x] push main réussi
- [ ] Vérifier 0 erreur sur Streamlit Cloud (commit 66b3615)
- [ ] Atteindre 300 répondants clients

## Règles compression tokens
- Résumés bullet points — pas de prose longue
- Référencer claude.md pour le contexte complet
- Ne répéter que les décisions et erreurs critiques

## Résumé rapide (pour requêtes futures)
E-Cantine = dashboard Streamlit BP IA, thème blanc brand #040c88.
Bug récurrent : TypeError Plotly Cloud → toujours utiliser PLOTLY_PIE pour Pie charts.
Repo : magi22/ecantine-dashboard · branch main · deploy auto Streamlit Cloud.
