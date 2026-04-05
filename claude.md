# Claude Memory Helper — E-Cantine

## Informations générales
- **Projet** : E-Cantine — Dashboard IA Business Plan
- **Repo** : https://github.com/magi22/ecantine-dashboard
- **Branche** : main
- **Stack** : Python 3.11 · Streamlit · Plotly · Pandas · Scipy · NumPy
- **Date mise à jour** : 2026-04-04
- **Contexte** : BP académique ISM Dakar — startup livraison repas. Données terrain : 100 clients, 23 livreurs, 8 restaurants. Modèle calibré sur Chowdeck Nigeria × Facteur Dakar 0.238.

---

## État actuel — commit 1fd2f7c

### Fichiers principaux
- `app.py` — Dashboard Streamlit (~1 950 lignes)
- `predict.py` — Modèle prédictif (~420 lignes)
- `clients.csv` — 100 répondants (réseau fondateur)
- `restaurants.csv` — 8 établissements réels Dakar
- `livreurs.csv` — 23 entretiens terrain
- `benchmarks.csv` — concurrents avec colonne `marche_dakar` (TRUE/FALSE/BENCHMARK_ONLY)
- `assets/logo_blue.svg` — Logo complet (icône + texte "ecantine") couleur #040c88
- `assets/logo_icon.svg` — Icône seule (ne jamais afficher avec logo_blue en même temps)
- `.streamlit/config.toml` — base=light

### Indicateurs financiers actuels (scénario central)
- **VAN** : ~380,8 M FCFA
- **TRI** : ~99,6%
- **IP** : ~8,7
- **Délai récupération** : ~28 mois (budget 49,5M FCFA)
- **Budget lancement** : **49 500 000 FCFA** (30 motos × 550K + app + marketing + infra)

### Structure des 9 onglets
| # | Onglet | Contenu |
|---|--------|---------|
| 1 | Vue d'ensemble | MAU 3 scénarios, CA annuel, tableau récap, KPIs, interprétation dynamique |
| 2 | Revenus & Coûts | Rev vs coûts, donut 6 flux, trésorerie cumulée, décomposition 5 ans |
| 3 | Données Terrain | Clients/livreurs/restaurants (hardcodé 100/23/8), benchmarks actifs Dakar uniquement |
| 4 | Scénarios | Comparaison 3 scénarios, décomposition 6 flux An 1 |
| 5 | Monte Carlo | Distribution CA/VAN, P10/P50/P90, verdict automatique, tornado |
| 6 | Charges & Trésorerie | Aires empilées coûts, marge nette, trésorerie cumulée, **tableau 7 postes complets** |
| 7 | Opérationnel | Commandes/livreurs/restaurants simulés, **flotte motos**, **critères sélection livreurs** |
| 8 | Glossaire & Guide | Définitions VAN/TRI/MAU/Monte Carlo/P10-P90/Tornado/Facteur Dakar |
| 9 | À propos du Modèle | Architecture, méthodologie, hypothèses, limites, guide sidebar |

### Sidebar — paramètres interactifs
**Modèle Économique** : Panier moyen, Commandes/MAU/mois, Frais livraison, Marge livraison
**Formules Restaurants** : % Starter (3 mois gratuits) / Pro / Premium
**Croissance MAU** : Plateau (L), Vitesse (k)
**Simulation Opérationnelle** : Cmd/livreur/jour, Jours actifs/mois, Restaurants cible An1, MAU par restaurant
**Monte Carlo** : Nombre de simulations + bouton Lancer

---

## Bugs résolus (historique complet)

| Erreur | Cause | Fix | Commit |
|--------|-------|-----|--------|
| UnicodeEncodeError CLI Windows | Terminal cp1252 | `sys.stdout = io.TextIOWrapper(encoding="utf-8")` | — |
| TypeError Plotly Cloud L617 | `font=dict(weight=600)` | Supprimé weight partout | 66b3615 |
| TypeError Plotly Cloud L621/L870 | `**PLOTLY` avec axes sur go.Pie | Remplacé par `_layout(pie=True)` | 66b3615 |
| TypeError "multiple values for legend" | `legend=` doublon Python | Créé `_LEG_H`/`_LEG_V` | b855bd9 |
| `font_size=11` dans legend | Non supporté Streamlit Cloud | Remplacé par `font=dict(size=11)` | b855bd9 |
| TypeError f-string `{{}}.get()` | `{{}}` = chaîne, pas dict | Remplacé par `{}` (dict vide réel) | e2445b9 |
| KeyError `n_restaurants` | Clé absente dans cache ancien | `.get("n_restaurants", fallback calculé)` | e737181 |
| Logo doublé dans header | `LOGO_ICON_B64` + `LOGO_BLUE_B64` côte à côte | Garder uniquement `LOGO_BLUE_B64` | e737181 |
| Glovo affiché dans concurrents Dakar | Pas de filtre marche_dakar | `df_b[df_b["marche_dakar"].astype(str)=="TRUE"]` | 1fd2f7c |
| Terrain affichait 20 clients / 5 restaurants | Streamlit Cloud lit CSV → valeurs anciennes | Hardcoder `n_rep=100, n_liv=23, n_rest=8` dans app.py | 1fd2f7c |
| CLI 500 simulations au lieu de 1000 | `run_model(n_mc=500)` dans main | Changé en `n_mc=1000` | 1fd2f7c |
| Tab6 charges — écart total vs détail (~15M An1) | Colonnes flotte/formation/qualité absentes du tableau | Ajout de `cout_flotte`, `cout_formation`, `cout_qualite` dans rows_ch | a4f5954 |

---

## Règles critiques à ne jamais oublier

1. **Jamais** `font=dict(..., weight=N)` dans les layouts Plotly → non supporté Streamlit Cloud
2. **Jamais** `**PLOTLY` (avec axes) sur `go.Pie` ou `go.Sunburst` → utiliser `_layout(pie=True)`
3. **Jamais** `{{}}` dans un f-string si tu veux un dict vide → utiliser `{}`
4. **Logo** : `logo_blue.svg` contient icône + texte. Ne JAMAIS afficher `logo_icon.svg` à côté dans le header
5. **Jamais** `annotations=[]` avec HTML `<span style=...>` dans Plotly → utiliser `fig.add_annotation()`
6. **Aucun numéro de version** (V7, V8, V9...) dans les titres, header, sidebar, footer, fichiers
7. **Valeurs terrain** : toujours hardcoder 100/23/8 dans app.py — jamais lire depuis CSV
8. **benchmarks.csv** : filtrer par `marche_dakar=="TRUE"` — Glovo/Jumia/Chowdeck ne sont PAS dans le marché Dakar
9. **BCEAO 1%** : frais réglementaires reversés à Wave/OM/Mix by Yass — PAS un revenu E-cantine
10. **README.md** : mettre à jour à chaque modification significative de predict.py ou app.py

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

### 6 flux de revenus (REV_LABELS / REV_KEYS / REV_COLORS)
```python
REV_LABELS = ["Livraison", "Commission", "Abonnements", "Vitrine", "Livr. propres", "B2B"]
REV_KEYS   = ["rev_livraison", "rev_commission", "rev_abonnements", "rev_vitrine", "rev_propres", "rev_b2b"]
# Pub absorbée dans abonnements — rev_pub = 0
```

### Données disponibles après `run_model()`
```
res["mau"]                          ← MAU central/optimiste/pessimiste + series 60 mois
res["ca_annuel"]                    ← CA an1-an5 × 3 scénarios + decomp_an1
res["financiers"]                   ← van_M, tri, ip, delai_mois, budget_fcfa
res["monthly"]["revenues"][i]       ← mois, mau, commandes, n_restaurants, rev_*, total_mensuel
res["monthly"]["costs"][i]          ← cout_salaires/marketing/tech/operations/cout_flotte/cout_formation/cout_qualite, total_couts, marge_pct
res["monthly"]["profit"][i]         ← profit_mensuel, cumul
res["terrain"]                      ← clients, livreurs, restaurants, benchmarks
res["sensitivity"]                  ← [{label, impact_up, impact_dn}]
res["metadata"]                     ← version_bp, livreurs_modele, cercle_vertueux, etc.
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

## Modèle économique — DEFAULT_PARAMS actuels (predict.py)

### Paramètres de croissance
```python
L = 60_000        # MAU plateau central
k = 0.07          # vitesse croissance
t0 = 44           # point inflexion (mois)
facteur_dakar = 0.238   # Chowdeck Nigeria × Facteur Dakar
```

### Paramètres financiers clés
```python
avg_basket = 3_000              # FCFA panier moyen hors livraison
frais_livraison_moy = 1_200     # FCFA frais livraison moyens
marge_livraison = 0.40          # 40% marge nette E-cantine sur livraison
avg_cmd_par_mau = 2.5           # commandes/utilisateur actif/mois
pct_app_orders = 0.85           # commandes via app (pour commission)
investissement = 49_500_000     # FCFA budget lancement
```

### Commission dégrésive
```python
# < 100 cmd/mois → 2.5% | 100-500 → 2.0% | 500-1500 → 1.5% | ≥1500 → 1.0%
```

### Cercle vertueux (mois 6+)
```python
taux_conversion_client_to_rest = 0.08   # 8% MAU actifs → bonus restaurants
# bonus_rest = min((mau / 500) * 0.08, 20)  — ajouté dès mois 6
```

### Rétention et qualité
```python
taux_retention_j30 = 0.45       # 45% clients reviennent après J30
taux_churn_mensuel = 0.12       # 12% inactifs par mois
nps_cible = 60                  # Net Promoter Score objectif
cout_suivi_qualite_livreurs = 150_000   # FCFA/mois superviseur + outils
```

### Formules restaurants
```python
pct_starter = 0.60   # Starter : 3 mois gratuits, commission 2.5% dès mois 4
pct_pro = 0.30       # Pro : 25 000 FCFA/mois (pub incluse)
pct_premium = 0.10   # Premium : 50 000 FCFA/mois (pub incluse)
starter_mois_gratuits = 3       # 3 mois sans frais, sans engagement
starter_facturation_debut = 4   # commission activée au 4ème mois si continuation
```

### Flotte motos
```python
flotte_motos = {
    "an1": {"nb": 30, "prix_unitaire": 550_000},
    "an2": {"nb": 80, "prix_unitaire": 550_000},
    "an3_plus": {"nb": 100, "prix_unitaire": 550_000},
}
cout_operationnel_moto_mensuel = 33_000  # essence ~15L + entretien + réparations
# An1 : 30 motos × 33k = 990k FCFA/mois
# An2 : 80 motos × 33k = 2 640k FCFA/mois
# An3+ : 100 motos × 33k = 3 300k FCFA/mois
```

### Formation livreurs (one-shot par an)
```python
# mois 0  : 1 500 000 FCFA (30 livreurs × 50 000)
# mois 12 : 2 500 000 FCFA (50 livreurs × 50 000)
# mois 24 : 1 000 000 FCFA (20 livreurs × 50 000)
```

### Livreurs externes An3+
```python
livreurs_externes_an3_plus = True
# rev_externes = cmd × frais_livraison × 0.15 × 0.10 (dès mois 24)
```

### Budget lancement 49 500 000 FCFA
| Poste | Montant |
|-------|---------|
| Développement V1 (app) | 9 100 000 |
| Motos An1 (30 × 550K) | 16 500 000 |
| Marketing lancement | 9 000 000 |
| Matériel informatique | 6 500 000 |
| Bureau / coworking 12 mois | 4 200 000 |
| Formation livreurs (30 × 50K) | 1 500 000 |
| Licences IA & outils | 1 440 000 |
| Hébergement cloud 12 mois | 840 000 |
| Frais juridiques | 500 000 |
| Fonds de roulement | 920 000 |

---

## Données terrain (valeurs à hardcoder — NE PAS lire depuis CSV)

| Source | Valeur | Méthode |
|--------|--------|---------|
| Clients | **100** (`n_rep=100`) | Réseau de connaissance fondateur |
| Livreurs | **23** (`n_liv=23`) | Entretiens semi-directifs terrain |
| Restaurants | **8** (`n_rest=8`) | Discussions directes avec gérants |

**Restaurants réels** : R01-R04 (internationaux), R05 Swice Palace, R06 Trophet, R07 Chez Mervi, R08 Chez Maman Gaga

**Sources livreurs** : Moaye (5), Swice Palace (4), Bazof (4), Yum Yum (4), Indépendants colis (6)

---

## Concurrents — Marché Dakar

### benchmarks.csv — colonne `marche_dakar`
- **TRUE** (actifs Dakar) : DFD, Ayda App, Yango Food, Yassir, Bring Me SN, KonectFood, Togalma, Wajeez → affichés dans table
- **FALSE** (hors marché) : Jumia Food (fermé déc 2023), Glovo (jamais lancé SN) → note en bas de table
- **BENCHMARK_ONLY** : Chowdeck Nigeria → calibration uniquement
- **INDIRECT** : PAPS Logistique → logistique, pas restauration

### Filtre dans app.py tab3
```python
df_actifs = df_b[df_b["marche_dakar"].astype(str) == "TRUE"]
```
Glovo, Jumia, Chowdeck → affichés uniquement dans une note stylisée sous la table principale.

---

## Architecture predict.py — fonctions clés

> **Règle importante** : `total_couts` = 7 postes. Le tableau tab6 doit afficher les 7 postes —
> ne jamais en omettre (flotte/formation/qualité représentent ~15M An1 invisible si manquants).

### `compute_revenues(p, scenarios)`
- Calcule les 6 flux mois par mois sur 60 mois
- Cercle vertueux (mois 6+) : `bonus_rest = min((mau / 500) * 0.08, 20)`
- Livreurs externes (mois 24+) : `rev_externes = cmd × 0.15 × 0.10`
- Commission dégrésive par palier de volume

### `compute_costs(p, mau_series)`
- 4 postes variables + flotte motos + formation (one-shot) + suivi qualité (mensuel)
- `cout_flotte` = nb_motos × 33 000 (33k par moto/mois)
- `cout_formation` : 1.5M mois 0, 2.5M mois 12, 1M mois 24, sinon 0
- `cout_qualite` = 150 000/mois

### `run_monte_carlo(p, n=1000)`
- 1 000 simulations (default et CLI)
- Perturbe ±20-30% les paramètres clés
- Retourne P10/P50/P90 CA An5 et VAN

---

## Décisions de design

- **Thème** : blanc (#f5f7ff fond) + brand bleu #040c88 + cyan #00b4d8
- **Logo** : `logo_blue.svg` seul dans le header (icône + texte intégrés)
- **Légendes empilées** : placées sous le graphique (y=-0.15 à -0.18)
- **Métriques** : font-size 1.15rem + white-space:nowrap
- **Graphiques** : carte blanche avec box-shadow
- **6 flux** (pas 7) : pub absorbée dans abonnements → `rev_pub=0`
- **Termes français** : "Trésorerie Cumulée", "Seuil de Rentabilité", "Utilisateurs Actifs Mensuels", "Tableau de bord"

---

## Preuve de concept V0 (chiffres réels)

- 34 commandes totales, 25 livrées
- 1er livreur : Tito Gbedjeha · 1er restaurant : TCHOP MASTER (4 commandes)
- Plats vendus : Choukouya de Porc, ALLOCO, Attiéké
- Stack : PHP/Laravel admin + React.js client + iOS/Android

---

## Pistes d'amélioration (non implémentées)

1. Corrélations Monte Carlo : si MAU factor < 0.80 → cmd_factor *= 0.90
2. Distribution break-even : histogramme du mois de BE sur N simulations
3. Probabilités : P(CA An5 > 100M), P(VAN > 500M)
4. Scénarios nommés : "Adoption lente", "Concurrence forte", "Viral"
5. Refactoring : extraire `charts.py` (~400 lignes moins dans app.py)
6. Augmenter panel : objectif 1 000 répondants clients (formulaire in-app)

---

## Règles de fonctionnement pour Claude

1. Lire le fichier avant de l'éditer (Read avant Edit/Write)
2. Vérifier syntaxe : `python -c "import ast; ast.parse(open('app.py').read())"`
3. Relancer `python predict.py` après toute modification de predict.py
4. Mettre à jour README.md à chaque modification significative
5. Ne jamais utiliser `font=dict(weight=N)` ni `{{}}` comme dict dans f-string
6. Ne jamais remettre de numéro de version (V7, V8...) dans les titres
7. Hardcoder 100/23/8 — jamais lire les valeurs terrain depuis CSV dans app.py
8. Filtrer benchmarks par `marche_dakar=="TRUE"` — Glovo/Jumia hors table
