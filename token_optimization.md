# Token Optimization — E-Cantine

## Objectif
Réduire les tokens consommés à chaque session en chargeant uniquement le contexte utile.

## Règles
1. Charger `primer.md` en début de session — résumé 1 page du projet
2. Charger `claude.md` uniquement si besoin d'historique complet
3. Référencer les fichiers par nom, pas par contenu complet
4. Format : bullet points, pas de prose
5. Supprimer les détails redondants après chaque session

## État court — format à utiliser
```
task   : [TACHE_EN_COURS]
status : [pending | in_progress | done | blocked]
next   : [PROCHAINE_ACTION]
error  : [DERNIERE_ERREUR_CONNUE]
commit : [DERNIER_COMMIT]
```

## État actuel
```
task   : Fix TypeError Plotly Cloud sur donut chart
status : done
next   : Vérifier sur Streamlit Cloud que le deploy passe
error  : **PLOTLY avec xaxis/yaxis sur go.Pie — corrigé via PLOTLY_PIE
commit : 66b3615
```

## Fichiers à charger par cas d'usage

| Besoin | Fichiers à lire |
|--------|----------------|
| Reprendre le dev | primer.md + claude.md |
| Corriger un bug Plotly | claude.md (section Problèmes) |
| Ajouter une feature | primer.md + app.py (structure) |
| Modifier le modèle | predict.py (DEFAULT_PARAMS) |
| Vérifier le déploiement | obsidian.md (Checklist) |
