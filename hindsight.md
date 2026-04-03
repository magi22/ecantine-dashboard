# Hindsight — E-Cantine

## Bilan des actions réalisées
- predict.py refactorisé : monolithique → module importable avec 8 fonctions
- Modèle enrichi : +coûts (salaires/marketing/tech/ops) +Monte Carlo +sensibilité tornado
- app.py créé from scratch : 5 onglets, Plotly dark puis light, sidebar interactive
- Logos SVG intégrés via base64 (sidebar + header + footer)
- 4 bugs corrigés sans régression (UnicodeError, 2× TypeError Plotly, fond blanc)
- GitHub repo créé et 5 commits poussés
- config.toml : thème clair configuré

## Leçons apprises

### Plotly + Streamlit Cloud
- `font=dict(weight=N)` non supporté → toujours utiliser `font=dict(size=N, color=C)` seulement
- `go.Pie` rejette `xaxis`/`yaxis` → créer un template séparé `PLOTLY_PIE`
- `annotations=[]` dans update_layout sur Pie → préférer `fig.add_annotation()`
- Ne pas mettre de HTML complexe (`<span style=...>`) dans les textes d'annotations Plotly

### Git / déploiement
- Le remote se configure avec `git remote add origin URL` puis `git push -u origin main`
- Streamlit Cloud redéploie automatiquement à chaque push sur main
- `gh auth login` nécessaire avant `gh repo create`

### Architecture
- Séparer template Plotly avec axes (Bar/Scatter) et sans axes (Pie/Donut)
- `@st.cache_data` sur les fonctions lourdes (modèle + Monte Carlo)
- Monte Carlo lazy via `st.session_state` pour ne pas bloquer le chargement

## Pipes à mettre en place
- [ ] Test automatique `python predict.py` dans CI GitHub Actions
- [ ] Export PDF du BP depuis le dashboard
- [ ] Webhook pour notifier quand 300 répondants atteints
- [ ] README.md public pour le repo

## Mesures de succès
- [x] Dashboard déployé sur Streamlit Cloud sans erreur
- [x] Modèle tourne en < 5s (CLI)
- [x] Monte Carlo 500 sims → VAN positive 100%
- [x] Thème blanc propre, logo bleu visible
- [ ] 0 TypeError sur Streamlit Cloud (commit 66b3615 — à vérifier)
