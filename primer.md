# Primer de workflow — E-Cantine

## Contexte en 3 lignes
Projet E-Cantine : dashboard IA Business Plan V7, ISM Dakar 2025.
Stack : Python · Streamlit · Plotly · GitHub (magi22/ecantine-dashboard).
Déployé gratuitement sur Streamlit Cloud. Thème blanc + brand bleu #040c88.

## Règles de démarrage de session
- Toujours vérifier : `git status`, `git remote -v` avant tout push
- Fichier principal : `predict.py` (modèle) + `app.py` (dashboard)
- Tester avec `python predict.py` avant de toucher app.py
- Ne jamais utiliser `font=dict(weight=N)` dans Plotly → crash Streamlit Cloud
- Ne jamais appliquer `**PLOTLY` à un `go.Pie` → utiliser `PLOTLY_PIE`

## Erreurs à ne jamais reproduire
- `font=dict(..., weight=600)` dans update_layout Plotly → non supporté Cloud
- `xaxis`/`yaxis` dans le layout d'un Pie chart → TypeError Cloud
- `<span style=...>` dans les annotations Plotly → HTML inline non rendu
- Commit sans tester `python predict.py` d'abord

## Format de résultat
- Titres + bullet points concis
- Contexte + actions + décisions
- Corrections urgentes en tête

## Fichiers clés
```
ecantine_vscode/
├── predict.py          # modèle IA (importable + CLI)
├── app.py              # dashboard Streamlit
├── requirements.txt    # pandas, numpy, scipy, streamlit, plotly
├── .streamlit/
│   └── config.toml     # theme light, brand colors
├── assets/
│   ├── logo_blue.svg   # logo brand #4d6aff (fond clair)
│   └── logo_icon.svg   # icône seule
├── outputs/
│   └── results.json    # généré par predict.py
└── *.csv               # données terrain
```
