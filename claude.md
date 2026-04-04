# Claude Memory Helper — E-Cantine

## Informations générales
- **Projet** : E-Cantine — Dashboard IA Business Plan
- **Repo** : https://github.com/magi22/ecantine-dashboard
- **Branche** : main
- **Stack** : Python 3.11 · Streamlit · Plotly · Pandas · Scipy · NumPy
- **Date mise à jour** : 2026-04-04
- **Contexte** : BP académique ISM Dakar — startup livraison repas. Données terrain limitées (20 clients, 23 livreurs, 5 restaurants) compensées par modèle statistique calibré sur Chowdeck Nigeria × Facteur Dakar 0.238.

---

## État actuel — commit e737181

### Fichiers principaux
- `app.py` — Dashboard Streamlit (~1 850 lignes)
- `predict.py` — Modèle prédictif (~340 lignes)
- `assets/logo_blue.svg` — Logo complet (icône + texte "ecantine", bleu #4d6aff)
- `assets/logo_icon.svg` — Icône seule (cercle "e")
- `.streamlit/config.toml` — base=light

### Structure des 9 onglets
| # | Onglet | Contenu |
|---|--------|---------|
| 1 | 📊 Vue d'ensemble | MAU 3 scénarios, CA annuel, tableau récap, KPIs, **interprétation dynamique** |
| 2 | 💰 Revenus & Coûts | Rev vs coûts, donut 7 flux, cash flow cumulatif, coûts An 1, décomposition 5 ans |
| 3 | 🌍 Données Terrain | Clients/livreurs/restaurants, benchmarks concurrents |
| 4 | 🔀 Scénarios | Comparaison 3 scénarios, tableau détaillé, décomposition 7 flux An 1 |
| 5 | 🎲 Monte Carlo | Distribution CA/VAN, KPIs P10/P50/P90, **interprétation auto verdict**, tornado |
| 6 | 💸 Charges & Trésorerie | Aires empilées coûts, marge nette, plan tréso cumulatif, tableau annuel |
| 7 | 📦 Opérationnel | Simulation commandes/livreurs/restaurants, tableau récap annuel, **interprétation écart terrain** |
| 8 | 📖 Glossaire & Guide | Définitions VAN/TRI/MAU/Monte Carlo/P10-P90/Tornado/Facteur Dakar/7 flux |
| 9 | 🗺️ À propos du Modèle | Architecture, rôle onglets, méthodologie, hypothèses, limites, guide sidebar |

### Sidebar — paramètres interactifs
**Modèle Économique** : Panier moyen, Commandes/MAU/mois, Frais livraison, Marge livraison
**Formules Restaurants** : % Starter / Pro / Premium (Premium = 100 - Starter - Pro)
**Croissance MAU** : Plateau (L), Vitesse (k)
**Simulation Opérationnelle** : Cmd/livreur/jour, Jours actifs/mois, Restaurants cible An1, MAU par restaurant
**Monte Carlo** : Nombre de simulations + bouton Lancer

---

## Bugs résolus (historique complet)

| Erreur | Cause | Fix | Commit |
|--------|-------|-----|--------|
| UnicodeEncodeError CLI Windows | Terminal cp1252 | `sys.stdout = io.TextIOWrapper(encoding="utf-8")` | — |
| TypeError Plotly Cloud L617 | `font=dict(weight=600)` | Supprimé weight partout | 66b3615 |
| TypeError Plotly Cloud L621/L870 | `**PLOTLY` avec axes sur go.Pie | Créé `PLOTLY_PIE` → remplacé par fonction `_layout(pie=True)` | 66b3615 |
| TypeError "multiple values for legend" | `legend=` doublon Python | Supprimé legend de PLOTLY global, créé `_LEG_H`/`_LEG_V` | b855bd9 |
| `font_size=11` dans legend | Non supporté Streamlit Cloud | Remplacé par `font=dict(size=11)` | b855bd9 |
| TypeError f-string `{{}}.get()` | `{{}}` = chaîne, pas dict | Remplacé par `{}` (dict vide réel) | e2445b9 |
| KeyError `n_restaurants` | Clé absente dans cache ancien | `.get("n_restaurants", fallback calculé)` | e737181 |
| Logo doublé dans header | `LOGO_ICON_B64` + `LOGO_BLUE_B64` côte à côte | Garder uniquement `LOGO_BLUE_B64` (contient déjà l'icône) | e737181 |

---

## ⚠️ Règles critiques à ne jamais oublier

1. **Jamais** `font=dict(..., weight=N)` dans les layouts Plotly → non supporté Streamlit Cloud
2. **Jamais** `**PLOTLY` (avec axes) sur `go.Pie` ou `go.Sunburst` → utiliser `_layout(pie=True)`
3. **Jamais** `{{}}` dans un f-string si tu veux un dict vide → utiliser `{}`
4. **Logo** : `logo_blue.svg` contient icône + texte. Ne JAMAIS afficher `logo_icon.svg` à côté de `logo_blue.svg` dans le header → doublon visuel
5. **Jamais** `annotations=[]` avec HTML `<span style=...>` dans Plotly → non supporté, utiliser `fig.add_annotation()`
6. **"V7"** : supprimé partout — ne pas remettre dans les titres, header, sidebar, footer

---

## Architecture technique app.py

### Fonction `_layout()`
Remplace tous les dicts `**PLOTLY` — génère le layout Plotly sans doublons de clés.
```python
_layout(title_text="", title_color=None, height=350,
        y_title="", x_title="", margin=None, legend=None,
        showlegend=None, barmode=None, xaxis_range=None, pie=False, **extra)
```
- `pie=True` → exclut xaxis/yaxis du layout

### Variables globales clés
```python
BRAND="#040c88"  BRAND_MED="#1a2fff"  BRAND_LT="#4d6aff"
CYAN="#00b4d8"   GREEN="#10b981"      ORANGE="#f97316"
GOLD="#f59e0b"   PURPLE="#7c3aed"     TEAL2="#14b8a6"
TEXT="#1a1f3c"   TEXT_DIM="#6b7280"   GREY_BG="#f5f7ff"
```

### Données disponibles après `run_model()`
```
res["mau"]                          ← MAU central/optimiste/pessimiste + series 60 mois
res["ca_annuel"]                    ← CA an1-an5 × 3 scénarios + decomp_an1
res["financiers"]                   ← van_M, tri, ip, delai_mois, budget_fcfa
res["monthly"]["revenues"][i]       ← mois, mau, commandes, n_restaurants, rev_*, total_mensuel
res["monthly"]["costs"][i]          ← cout_salaires/marketing/tech/operations, total_couts, marge_pct
res["monthly"]["profit"][i]         ← profit_mensuel, cumul
res["terrain"]                      ← clients, livreurs, restaurants, benchmarks
res["sensitivity"]                  ← [{label, impact_up, impact_dn}]
```

### OPS dict (simulation opérationnelle)
```python
OPS = {
    "cmd_par_livreur_j": cmd_par_livreur_j,
    "jours_actifs_mois": jours_actifs_mois,
    "mau_par_rest":      mau_par_rest,
    "nb_rest_cible_an1": nb_rest_cible,
}
```

---

## Décisions de design

- **Thème** : blanc (#f5f7ff fond) + brand bleu #040c88 + cyan #00b4d8
- **Logo** : `logo_blue.svg` seul (icône + texte, pas "V7" dans les titres)
- **Légendes empilées** : déplacées **sous** le graphique (y=-0.15 à -0.18) pour éviter l'overlap avec le titre
- **Métriques** : font-size 1.15rem + white-space:nowrap pour éviter troncature
- **Graphiques** : encapsulés dans carte blanche avec box-shadow (profondeur visuelle)
- **Badges header** : vert = VAN/TRI positifs, violet = IP, bleu = Break-even
- **Interprétation dynamique** : liée aux sliders, recalculée à chaque changement

---

## Pistes d'amélioration identifiées (non encore implémentées)

1. **Corrélations Monte Carlo** : si MAU factor < 0.80 → cmd_factor *= 0.90
2. **Distribution break-even** : histogramme du mois de BE sur N simulations
3. **Probabilités** : P(CA An5 > 100M), P(VAN > 500M), etc.
4. **Scénarios nommés** : "Adoption lente", "Concurrence forte", "Viral"
5. **Refactoring** : extraire `charts.py` (réduction ~400 lignes app.py)
6. **Augmenter panel** : objectif 300 répondants clients

---

## Règles de fonctionnement pour Claude

1. Toujours vérifier syntaxe `python -c "import ast; ast.parse(...)"` après modification
2. Toujours relancer `python predict.py` après modification de predict.py
3. Logger chaque bug dans ce fichier avant de passer à la suite
4. Ne jamais utiliser `font=dict(weight=N)` ni `{{}}` comme dict dans f-string
5. `logo_blue.svg` = logo complet — ne pas afficher avec `logo_icon.svg` en même temps
6. Pour les légendes à 7 items (Pie, bar empilé) → placer en bas du graphique
