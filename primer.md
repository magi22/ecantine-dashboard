# Primer E-Cantine — Guide de contexte projet

> Ce fichier est conçu pour être partagé avec n'importe quelle IA (Gemini, ChatGPT, etc.)
> afin de déléguer des tâches simples sans perdre le contexte du projet.

---

## Contexte en 5 lignes

Projet **E-Cantine** : startup de livraison de repas à Dakar, Sénégal.
Dashboard IA Business Plan académique pour ISM Dakar.
Stack : Python 3.11 · Streamlit · Plotly · Pandas · Scipy · NumPy.
Déployé gratuitement sur **Streamlit Cloud** (GitHub : magi22/ecantine-dashboard).
Thème blanc (#f5f7ff) + brand bleu **#040c88**.

---

## Fichiers principaux

```
ecantine_vscode/
├── predict.py          # modèle IA (courbe S + Monte Carlo)
├── app.py              # dashboard Streamlit (9 onglets)
├── requirements.txt    # pandas, numpy, scipy, streamlit, plotly
├── .streamlit/
│   └── config.toml     # base=light
├── assets/
│   ├── logo_blue.svg   # logo brand couleur #040c88 (icône + texte)
│   └── logo_icon.svg   # icône seule (ne pas afficher avec logo_blue)
├── outputs/
│   └── results.json    # généré automatiquement par predict.py
├── clients.csv         # 100 répondants réseau de connaissance fondateur
├── restaurants.csv     # 8 établissements Dakar (4 internationaux + 4 sénégalais)
├── livreurs.csv        # 23 entretiens terrain
└── benchmarks.csv      # concurrents avec colonne marche_dakar (TRUE/FALSE/BENCHMARK_ONLY)
```

---

## Données terrain (vraies valeurs — NE PAS MODIFIER)

- **100 clients** — réseau de connaissance fondateur, commandant régulièrement à Dakar
- **23 livreurs** — entretiens semi-directifs (Moaye, Swice Palace, Bazof, Yum Yum, Indépendants)
- **8 restaurants** — Restaurant International 1-4, Swice Palace, Trophet, Chez Mervi, Chez Maman Gaga
- **Objectif** : 1 000 répondants via formulaire in-app avant fin An 1 (décembre 2027)

---

## Modèle économique — 6 flux de revenus

1. ① Frais livraison (marge 40%)
2. ② Commission dégrésive par volume : <100 cmd→2.5% | 100-500→2.0% | 500-1500→1.5% | >1500→1.0%
3. ③ Abonnements restaurants (Starter **3 mois gratuits sans engagement** → commission 2.5% dès mois 4 / Pro 25K / Premium 50K FCFA/mois) — pub incluse
4. ④ Vitrine E-cantine (mise en avant restaurants)
5. ⑤ Livraisons propres (2.5% dispatch)
6. ⑥ B2B entreprises

**Frais BCEAO 1%** = réglementaires, reversés à Wave/Orange Money/Mix by Yass — PAS un revenu E-cantine.

---

## Paramètres clés du modèle prédictif

- MAU plateau (L) = 60 000 (central)
- Vitesse de croissance (k) = 0.07
- Point d'inflexion (t0) = 44 mois
- Calibration : Chowdeck Nigeria × Facteur Dakar **0.238**
- Simulation Monte Carlo : 1 000 itérations
- Cercle vertueux : taux_conversion_client_to_rest = 8% (mois 6+)
- Rétention J30 = 45% · Churn mensuel = 12% · NPS cible = 60
- Budget lancement : **49 500 000 FCFA** (30 motos × 550K + app + marketing + infra)
- Flotte motos : An1=30 · An2=80 · An3+=100 (33 000 FCFA/moto/mois opérationnel)
- Indicateurs centraux : VAN ~380,8M FCFA · TRI ~99,6% · Délai récupération ~28 mois

---

## Concurrents — Marché Dakar (actifs)

| Plateforme | Statut |
|---|---|
| Dakar Food Delivery | Actif |
| Ayda App | Actif (niche petit-déjeuner) |
| Yango Food | Actif (fév. 2025 — commission 0% temporaire) |
| Yassir | Actif ($150M levés — multi-services) |
| Bring Me SN | Actif (100+ restaurants, 4.5★) |
| KonectFood | Actif (multi-villes) |
| Togalma | Actif (B2B pro) |
| Wajeez | Actif (ex FoodBeeper) |

**Hors marché Dakar :**
- Jumia Food : fermé décembre 2023
- Glovo : jamais officiellement lancé au Sénégal (fort en Côte d'Ivoire et Maroc)
- Chowdeck : Nigeria uniquement — calibration benchmark seulement

---

## Règles absolues (NE PAS VIOLER)

1. `font=dict(weight=N)` → interdit dans Plotly (crash Streamlit Cloud)
2. `**PLOTLY` sur `go.Pie` → interdit (utiliser `_layout(pie=True)`)
3. `{{}}` dans f-string pour dict vide → ne PAS faire (retourne string `"{}"`)
4. Valeurs terrain dans l'affichage → hardcoder 100/23/8 (jamais depuis CSV)
5. Logo header → `logo_blue.svg` seul (jamais + `logo_icon.svg` en même temps)
6. Couleur brand → **#040c88** (jamais #4d6aff)
7. Après modification → `python predict.py` AVANT git commit

---

## Tâches déléguables à Gemini / ChatGPT

✅ **OK à déléguer :**
- Générer des données CSV synthétiques réalistes (nouvelles lignes clients, livreurs)
- Rédiger/améliorer des textes de description en français pour les onglets
- Traduire des termes techniques en français simple (glossaire)
- Vérifier la cohérence des données concurrents (noms, dates, sources)
- Rédiger des sections du Business Plan en français académique
- Créer des visualisations statiques (tableaux, graphiques dans des outils externes)

❌ **Garder dans Claude Code :**
- Modifications de app.py ou predict.py
- Commits et push git
- Débogage Python/Plotly
- Logique financière et modèle prédictif
- Architecture du dashboard

---

## Variables globales importantes (app.py)

```python
BRAND    = "#040c88"   # bleu brand officiel
BRAND_MED= "#1a2fff"
BRAND_LT = "#4d6aff"
CYAN     = "#00b4d8"
GREEN    = "#10b981"
ORANGE   = "#f97316"
GOLD     = "#f59e0b"
PURPLE   = "#7c3aed"
TEXT     = "#1a1f3c"
TEXT_DIM = "#6b7280"
GREY_BG  = "#f5f7ff"
```

---

## Preuve de concept V0 (chiffres réels)

- 34 commandes totales, 25 livrées
- 1er livreur : Tito Gbedjeha
- 1er restaurant : TCHOP MASTER (4 commandes)
- Plats : Choukouya de Porc, ALLOCO, Attiéké
- Stack : PHP/Laravel admin + React.js client + iOS/Android

---

## Liens

- Dashboard : https://ecantine-dash.streamlit.app/
- GitHub : https://github.com/magi22/ecantine-dashboard
- Formulaire terrain : https://forms.gle/FMQqysZSYWC7Phhp9
