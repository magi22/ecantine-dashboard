# E-Cantine — Modèle de Prédiction IA
## Business Plan · ISM Dakar · 2026
**Auteur :** Adote Mario-Giovani ADUAYI-AKUE · contact@ecantine.sn

---

## LANCER LE MODÈLE

```bash
pip install pandas numpy scipy streamlit plotly
python predict.py              # génère outputs/results.json
streamlit run app.py           # lance le dashboard interactif
```

---

## STRUCTURE DES FICHIERS

```
ecantine_vscode/
├── predict.py          # Modèle IA — courbe S + Monte Carlo + export JSON
├── app.py              # Dashboard Streamlit — 9 onglets interactifs
├── primer.md           # Contexte projet pour délégation à autres IA
├── methodologie.py     # Note méthodologique officielle BP
├── requirements.txt    # pandas numpy scipy streamlit plotly
│
├── clients.csv         # 100 répondants réseau de connaissance fondateur
├── livreurs.csv        # 23 entretiens terrain (Moaye, Swice Palace, Bazof, Yum Yum, Indép.)
├── restaurants.csv     # 8 établissements (4 internationaux + Swice Palace, Trophet, Chez Mervi, Chez Maman Gaga)
├── benchmarks.csv      # Concurrents Dakar — colonne marche_dakar (TRUE/FALSE/BENCHMARK_ONLY)
├── macro_senegal.csv   # ANSD · ARTP · Wave · PIB
│
├── assets/
│   ├── logo_blue.svg   # Logo complet brand #040c88 (icône + texte)
│   └── logo_icon.svg   # Icône seule (ne pas afficher en même temps que logo_blue)
│
└── outputs/
    └── results.json    # Généré automatiquement par python predict.py
```

---

## CE QUE FAIT LE MODÈLE — VUE D'ENSEMBLE

Le modèle tourne en **3 étapes** :

### Étape 1 — Croissance MAU (Courbe S logistique)
Simule le nombre d'**Utilisateurs Actifs Mensuels** sur 60 mois (5 ans).
Calibré sur **Chowdeck Nigeria × Facteur Dakar 0.238** (population × pouvoir d'achat × pénétration mobile Dakar vs Lagos).

| Scénario | Plateau (L) | Vitesse (k) | Inflexion (t0) |
|---|---|---|---|
| Pessimiste | 40 000 | 0.05 | Mois 50 |
| **Central** | **60 000** | **0.07** | **Mois 44** |
| Optimiste | 90 000 | 0.10 | Mois 36 |

### Étape 2 — 6 Flux de Revenus Mensuels
Calculés à partir du MAU, mois par mois sur 60 mois.

| # | Flux | Formule |
|---|---|---|
| ① | Frais livraison | `MAU × cmd/MAU × frais_livraison × %E-cantine × marge 40%` |
| ② | Commission dégrésive | `commandes × 85% app × panier × taux_comm` |
| ③ | Abonnements Pro/Premium | `n_restaurants × %Pro × 25K + %Premium × 50K` (pub incluse) |
| ④ | Vitrine E-cantine | `commandes × panier × 8% × 5%` (à partir mois 4) |
| ⑤ | Livraisons propres | `commandes × panier × %hors E-cantine × 2.5%` |
| ⑥ | B2B entreprises | Progressif à partir mois 10 (plafond 3M FCFA/mois) |

**Commission dégrésive par volume** (pas par formule) :
- < 100 cmd/mois → 2,5%
- 100–500 cmd/mois → 2,0%
- 500–1 500 cmd/mois → 1,5%
- ≥ 1 500 cmd/mois → 1,0%

**An 3+ uniquement** : livreurs externes autorisés → commission 10% sur 15% des livraisons.

### Étape 3 — Coûts Mensuels
7 postes de coûts (4 variables + flotte motos + formation + suivi qualité) :

| Poste | Formule |
|---|---|
| Salaires | `1 500 000 + MAU/1000 × 80 000` FCFA/mois |
| Marketing | `max(150 000 ; CA × 12%)` |
| Tech & infra | `250 000 + MAU/1000 × 10 000` |
| Opérations | `200 000 + MAU/1000 × 30 000` |
| **Flotte motos** | `nb_motos × 33 000` FCFA/mois (essence + entretien + réparations) |
| **Formation livreurs** | One-shot : 1 500 000 mois 0 · 2 500 000 mois 12 · 1 000 000 mois 24 |
| **Suivi qualité** | 150 000 FCFA/mois (superviseur + outils) |

**Flotte motos :**
- An 1 : 30 motos → 990 000 FCFA/mois
- An 2 : 80 motos → 2 640 000 FCFA/mois
- An 3+ : 100 motos (plafond) → 3 300 000 FCFA/mois

### Indicateurs Financiers Calculés
- **VAN** : Valeur Actuelle Nette sur 5 ans (taux 15%)
- **TRI** : Taux de Rendement Interne
- **IP** : Indice de Profitabilité = (VAN + investissement) / investissement
- **Seuil de rentabilité** : mois où la trésorerie cumulée repasse en positif

### Monte Carlo (1 000 simulations)
Perturbe aléatoirement ±20–30% les paramètres clés → distributions P10/P50/P90 du CA An5 et de la VAN.

---

## DONNÉES TERRAIN

| Source | Taille | Méthode | Zone |
|---|---|---|---|
| Clients | **100 répondants** | Réseau de connaissance fondateur | Dakar — 10 quartiers |
| Livreurs | **23 entretiens** | Semi-directifs terrain | Dakar |
| Restaurants | **8 discussions** | Directes avec gérants | Dakar |

**Objectif** : 1 000 répondants clients via formulaire in-app avant fin An 1 (IC 95%, marge ±3,1%).

**Restaurants interrogés** : Restaurant International 1-4, Swice Palace, Trophet, Chez Mervi, Chez Maman Gaga.

**Sources livreurs** : Moaye (5), Swice Palace (4), Bazof (4), Yum Yum (4), Indépendants colis (6).

---

## MODÈLE ÉCONOMIQUE — PARAMÈTRES CLÉS

```python
avg_basket                    = 3 000 FCFA  # panier moyen hors livraison
frais_livraison               = 1 200 FCFA  # frais de livraison moyens
marge_livraison               = 40%         # marge nette sur livraisons
avg_cmd_par_mau               = 2.5         # commandes/utilisateur actif/mois
pct_app_orders                = 85%         # commandes via app (pour commission)
taux_conversion_client_to_rest= 8%          # clients actifs → restaurant rejoint (cercle vertueux, mois 6+)
taux_retention_j30            = 45%         # clients qui reviennent après J30
taux_churn_mensuel            = 12%         # taux d'inactifs par mois
nps_cible                     = 60          # Net Promoter Score objectif
cout_suivi_qualite_livreurs   = 150 000 FCFA/mois  # superviseur + outils
```

**Mix restaurants :**
- Starter (gratuit) : 60% des restaurants
- Pro (25 000 FCFA/mois) : 30%
- Premium (50 000 FCFA/mois) : 10%

**Offre Starter :**
- **3 mois gratuits, sans engagement**
- Commission 2,5% activée au 4ème mois uniquement si le restaurant continue
- Aucune obligation après les 3 mois

---

## BUDGET DE LANCEMENT — 49 500 000 FCFA

| Poste | Montant |
|---|---|
| Développement V1 (app) | 9 100 000 FCFA |
| Motos An1 (30 × 550K) | 16 500 000 FCFA |
| Marketing lancement | 9 000 000 FCFA |
| Matériel informatique | 6 500 000 FCFA |
| Bureau / coworking 12 mois | 4 200 000 FCFA |
| Formation livreurs (30 × 50K) | 1 500 000 FCFA |
| Licences IA & outils | 1 440 000 FCFA |
| Hébergement cloud 12 mois | 840 000 FCFA |
| Frais juridiques | 500 000 FCFA |
| Fonds de roulement | 920 000 FCFA |
| **TOTAL** | **49 500 000 FCFA** |

---

## FLOTTE MOTOS & SÉLECTION LIVREURS

**Flotte E-cantine :**
- Prix moto : 525 000 FCFA + 25 000 FCFA porte-bagage = 550 000 FCFA
- Coût opérationnel : 33 000 FCFA/moto/mois (essence ~15L + entretien + réparations)
- Suivi qualité livreurs : 150 000 FCFA/mois (superviseur + outils)
- Formation one-shot : An1 = 1,5M · An2 = 2,5M · An3 = 1M FCFA
- Modèle : **flotte propre prioritaire** — activité parallèle autorisée, E-cantine passe en premier
- **Nourriture uniquement** — pas de colis
- An 1–2 : flotte propre uniquement (pas de livreurs externes)
- An 3+ : livreurs externes autorisés (max 15% des livraisons, commission 10%)

**Critères sélection livreurs :**
- Langues requises : Wolof + Français
- Note minimale active : 4,0/5
- Suspension si note < 3,5/5
- Formation obligatoire : 2 jours, 50 000 FCFA/livreur
- Programme : protocole livraison, app E-cantine, GPS Dakar, incidents, hygiène alimentaire

---

## FRAIS BCEAO — RÉGLEMENTAIRES

Les frais de paiement électronique de **1%** (max 5 000 FCFA) sont réglementaires — imposés par la BCEAO à tous les opérateurs de monnaie électronique (Wave, Orange Money, Mix by Yass). Ils sont affichés au client avant validation et **reversés intégralement à l'opérateur**. **Ce n'est pas un revenu E-cantine.**

---

## CONCURRENTS — MARCHÉ DAKAR

| Plateforme | Statut | Point fort |
|---|---|---|
| Dakar Food Delivery | Actif | Ancienneté |
| Ayda App | Actif | Niche petit-déjeuner |
| Yango Food | Actif (fév. 2025) | Commission 0% temporaire |
| Yassir | Actif ($150M levés) | Multi-services VTC+livraison |
| Bring Me SN | Actif (4.5★) | 100+ restaurants, délai 20min |
| KonectFood | Actif | Multi-villes Sénégal |
| Togalma | Actif | B2B pro dès 7h |
| Wajeez | Actif | Ex FoodBeeper |

**Hors marché Dakar :**
- **Jumia Food** : fermé décembre 2023 (TechCabal)
- **Glovo** : jamais officiellement lancé au Sénégal (fort en Côte d'Ivoire et Maroc)
- **Chowdeck** : Nigeria uniquement — benchmark de calibration seulement

---

## DASHBOARD — 9 ONGLETS

| # | Onglet | Contenu |
|---|---|---|
| 1 | Vue d'ensemble | MAU 3 scénarios, CA annuel, KPIs, interprétation dynamique |
| 2 | Revenus & Coûts | Rev vs coûts, donut 6 flux, trésorerie cumulée, décomposition 5 ans |
| 3 | Données Terrain | Clients/livreurs/restaurants, benchmarks concurrents actifs Dakar |
| 4 | Scénarios | Comparaison 3 scénarios, décomposition 6 flux An 1 |
| 5 | Monte Carlo | Distribution CA/VAN, P10/P50/P90, verdict automatique, tornado |
| 6 | Charges & Trésorerie | Aires empilées coûts, marge nette, plan trésorerie cumulatif |
| 7 | Opérationnel | Commandes/livreurs/restaurants simulés, flotte motos, critères livreurs |
| 8 | Glossaire & Guide | Définitions VAN/TRI/MAU/Monte Carlo/P10-P90/Tornado/Facteur Dakar |
| 9 | À propos du Modèle | Architecture, méthodologie, hypothèses, limites, guide sidebar |

---

## RÈGLES ABSOLUES — NE PAS MODIFIER

1. `font=dict(weight=N)` dans Plotly → **interdit** (crash Streamlit Cloud)
2. `**PLOTLY` sur `go.Pie/Sunburst` → **interdit** (utiliser `_layout(pie=True)`)
3. `{{}}` dans f-string pour dict vide → **interdit** (retourne string `"{}"`)
4. Valeurs terrain dans l'affichage → **hardcoder** 100/23/8 (jamais depuis CSV)
5. Logo header → `logo_blue.svg` seul (jamais + `logo_icon.svg` ensemble)
6. Couleur brand → **#040c88** (jamais #4d6aff)
7. Après toute modification → `python predict.py` AVANT git commit

---

## LIENS

- Dashboard : https://ecantine-dash.streamlit.app/
- GitHub : https://github.com/magi22/ecantine-dashboard
- Formulaire terrain : https://forms.gle/FMQqysZSYWC7Phhp9
- Fondateur : Adote Mario-Giovani ADUAYI-AKUE · Sacré-Cœur 2, Dakar, Sénégal

---

---

*Dernière mise à jour : avril 2026*
