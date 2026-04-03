# Claude Memory Helper — E-Cantine

## Informations générales
- **Projet** : E-Cantine — Dashboard IA Business Plan V7
- **Repo** : https://github.com/magi22/ecantine-dashboard
- **Branche** : main
- **Stack** : Python 3.11 · Streamlit · Plotly · Pandas · Scipy · NumPy
- **Date** : 2026-04-03
- **Contexte** : BP académique ISM Dakar — startup livraison repas. Données terrain limitées (20 clients, 23 livreurs, 5 restaurants) compensées par modèle statistique calibré sur Chowdeck Nigeria × Facteur Dakar 0.238.

---

## Ce que l'utilisateur a fait
- Fourni predict.py V1 (script CLI monolithique)
- Fourni 5 CSV terrain : clients, livreurs, restaurants, benchmarks, macro_senegal
- Fourni logos SVG : logo_icon.svg, logo_blue.svg (brand #040c88)
- Déployé sur Streamlit Cloud via repo GitHub magi22/ecantine-dashboard
- Demandé : thème blanc/clair, logo bleu, animations

## Ce que l'assistant a fait
- Refactorisé predict.py en module importable avec fonctions séparées
- Ajouté modèle de coûts, Monte Carlo (500-2000 simulations), analyse de sensibilité tornado
- Créé app.py dashboard Streamlit 5 onglets
- Créé assets/ avec logos SVG, .streamlit/config.toml
- Initialisé git, créé repo GitHub, poussé 4 commits
- Corrigé 2 bugs Streamlit Cloud TypeError Plotly :
  - `font=dict(..., weight=600)` → non supporté Cloud → supprimé
  - `**PLOTLY` avec xaxis/yaxis sur go.Pie → créé PLOTLY_PIE sans axes
  - `annotations=[]` dans update_layout sur Pie → remplacé par fig.add_annotation()

---

## Problèmes rencontrés

| Erreur | Cause | Fix |
|--------|-------|-----|
| UnicodeEncodeError CLI Windows | Terminal cp1252 | `sys.stdout = io.TextIOWrapper(encoding="utf-8")` |
| TypeError Plotly Cloud L617 | `font=dict(weight=600)` sur titre chart | Supprimé weight partout |
| TypeError Plotly Cloud L621/L870 | `**PLOTLY` (avec xaxis/yaxis) appliqué à go.Pie | Créé `PLOTLY_PIE` sans xaxis/yaxis |
| TypeError "multiple values for legend" | `legend=` dans PLOTLY global ET passé en kwarg → doublon Python | Supprimé `legend` de PLOTLY, créé `LEG_H`/`LEG_V` séparés, chaque chart l'ajoute explicitement |
| `font_size=11` dans legend | Raccourci non supporté Streamlit Cloud | Remplacé partout par `font=dict(size=11)` |

## ⚠️ Règle critique à ne jamais oublier
- **Jamais** `font=dict(..., weight=N)` dans les layouts Plotly → non supporté Streamlit Cloud
- **Jamais** `**PLOTLY` (avec axes) sur un `go.Pie` ou `go.Sunburst` → utiliser `PLOTLY_PIE`
- **Jamais** `annotations=[...]` avec HTML `<span style=...>` dans Plotly → HTML inline non supporté dans annotations

---

## Décisions et état actuel
- Thème : blanc (#f5f7ff fond) + brand bleu #040c88 + cyan #00b4d8
- Logo : logo_blue.svg (#4d6aff) dans sidebar et footer
- Template Plotly : `PLOTLY` (avec axes) pour Bar/Scatter/Histogram, `PLOTLY_PIE` pour Pie/Donut
- Monte Carlo : lazy (lancé via bouton sidebar, mis en cache session_state)
- Commit actuel : 66b3615

## Points checkés avec succès
- [x] predict.py tourne en CLI : python predict.py → outputs/results.json OK
- [x] Monte Carlo 500 simulations → VAN positive 100%
- [x] Git initialisé + remote origin configuré
- [x] Push sur GitHub réussi
- [x] config.toml base=light configuré

## Prochaines étapes recommandées
1. Vérifier le déploiement Streamlit Cloud (share.streamlit.io) — le bug Pie est corrigé commit 66b3615
2. Augmenter le panel clients (objectif 300 répondants) pour affiner les projections
3. Ajouter onglet "Export PDF" pour impression BP jury
4. Envisager README.md pour documenter l'utilisation

## Règles de fonctionnement pour Claude
1. Toujours planifier avant de coder : poser un plan clair avant de lancer le développement.
2. Déléguer aux sous-agents dès qu'il y a une tâche complexe.
3. Auto-amélioration : logger chaque erreur (voir tableau ci-dessus), ne jamais répéter la même.
4. Testing : exécuter `python predict.py` après chaque modification de predict.py.
5. Fixer les bugs automatiquement si détecté — corriger avant de passer à la suite.
