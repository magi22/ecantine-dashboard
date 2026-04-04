"""
╔══════════════════════════════════════════════════════════════╗
║         E-CANTINE — MODÈLE DE PRÉDICTION IA                ║
║         Business Plan V7 · ISM Dakar · 2025                ║
║         Auteur : Adote Mario-Giovani ADUAYI-AKUE            ║
╚══════════════════════════════════════════════════════════════╝

Module importable par app.py (Streamlit) et exécutable en CLI.
  python predict.py  →  outputs/results.json
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from scipy.optimize import brentq

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, "outputs"), exist_ok=True)

# ══════════════════════════════════════════════════════════════
# PARAMÈTRES PAR DÉFAUT
# ══════════════════════════════════════════════════════════════

DEFAULT_PARAMS = {
    # ── Revenus ─────────────────────────────────────────────
    "commission_starter":    0.025,   # 2,5% — formule Starter (0 FCFA/mois)
    "commission_pro":        0.020,   # 2,0% — formule Pro (25 000 FCFA/mois)
    "commission_premium":    0.010,   # 1,0% — formule Premium (50 000 FCFA/mois)
    "frais_livraison_moy":   1200,    # FCFA — frais de livraison moyens
    "marge_livraison":       0.40,    # 40% de marge nette sur les livraisons
    "avg_basket":            3000,    # FCFA — panier moyen hors livraison
    "avg_cmd_par_mau":       2.5,     # commandes/utilisateur actif/mois
    "pct_app_orders":        0.85,    # 85% des commandes passées via app mobile (vs POS/tél.)
    # ── Mix restaurants ─────────────────────────────────────
    "pct_starter":           0.60,
    "pct_pro":               0.30,
    "pct_premium":           0.10,
    "prix_pro":              25_000,
    "prix_premium":          50_000,
    "nb_rest_cible_an1":     150,
    # ── Croissance MAU (courbe S) — Paramètres finalisés BP ────
    "mau_L":                 60_000,   # Central — conservateur, break-even An 3
    "mau_k":                 0.07,
    "mau_t0":                44,
    "mau_L_pess":            40_000,
    "mau_k_pess":            0.05,
    "mau_t0_pess":           50,
    "mau_L_opt":             90_000,
    "mau_k_opt":             0.10,
    "mau_t0_opt":            36,
    # ── Financier ───────────────────────────────────────────
    "investissement":        22_560_000,
    "taux_actualisation":    0.15,
    # ── Coûts ───────────────────────────────────────────────
    "salaires_base":         1_500_000,  # équipe fondateurs (mois 1-6)
    "salaires_par_kmau":     80_000,     # +80K/mois par tranche 1 000 MAU
    "marketing_pct_rev":     0.12,       # 12% du CA
    "marketing_fixe":        150_000,    # budget marketing minimum
    "tech_base":             250_000,    # hébergement, API, maintenance
    "tech_par_kmau":         10_000,     # coûts infra variables
    "operations_base":       200_000,    # admin, bureau, divers
    "operations_par_kmau":   30_000,     # support client variable
}

# ══════════════════════════════════════════════════════════════
# 1. CHARGEMENT DONNÉES TERRAIN
# ══════════════════════════════════════════════════════════════

def load_data():
    """Charge tous les CSV terrain et retourne un dict de DataFrames."""
    def _load(name):
        path = os.path.join(BASE, f"{name}.csv")
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()
    return {
        "clients":     _load("clients"),
        "livreurs":    _load("livreurs"),
        "restaurants": _load("restaurants"),
        "benchmarks":  _load("benchmarks"),
        "macro":       _load("macro_senegal"),
    }

# ══════════════════════════════════════════════════════════════
# 2. ANALYSE TERRAIN
# ══════════════════════════════════════════════════════════════

def analyze_terrain(data):
    """Analyse les CSV et retourne un dict de métriques terrain."""
    clients     = data.get("clients",     pd.DataFrame())
    livreurs    = data.get("livreurs",    pd.DataFrame())
    restaurants = data.get("restaurants", pd.DataFrame())
    benchmarks  = data.get("benchmarks",  pd.DataFrame())

    result = {}

    # ── Clients ─────────────────────────────────────────────
    if not clients.empty:
        result["clients"] = {
            "n_repondants":       100,   # 100 personnes réseau de connaissance (CSV = 20 échantillon pilote)
            "objectif_cible":     1_000,
            "pct_etudiants":      round((clients["situation"] == "Etudiant(e)").mean() * 100, 1),
            "pct_wave":           round((clients["mode_paiement_1"] == "Wave").mean() * 100, 1),
            "pct_interesse_total": round(
                clients["interet_ecantine"].str.contains("Très|Plutôt", na=False).mean() * 100, 1
            ),
            "pct_tres_interesse": round(
                clients["interet_ecantine"].str.contains("Très", na=False).mean() * 100, 1
            ),
            "age_dist":    clients["age"].value_counts().to_dict() if "age" in clients.columns else {},
            "quartiers":   clients["quartier"].value_counts().head(6).to_dict() if "quartier" in clients.columns else {},
            "freins":      clients["frein_principal"].value_counts().to_dict() if "frein_principal" in clients.columns else {},
            "fonctions":   clients["fonctionnalite_importante"].value_counts().to_dict() if "fonctionnalite_importante" in clients.columns else {},
            "prix_livraison": clients["prix_livraison_acceptable"].value_counts().to_dict() if "prix_livraison_acceptable" in clients.columns else {},
        }
    else:
        # Valeurs terrain réelles confirmées — réseau de connaissance Dakar
        result["clients"] = {
            "n_repondants":    100,
            "objectif_cible":  1_000,
            "type_collecte":   "Réseau de connaissance — bouche-à-oreille",
            "zone":            "Dakar — plusieurs quartiers",
        }

    # ── Livreurs ─────────────────────────────────────────────
    if not livreurs.empty:
        zones_series = (
            livreurs["zones_couvertes"].str.split(";").explode().str.strip().value_counts().head(8)
            if "zones_couvertes" in livreurs.columns else pd.Series(dtype=int)
        )
        result["livreurs"] = {
            "n_entretiens":    len(livreurs),
            "pct_moto":        round((livreurs["vehicule"] == "Moto personnelle").mean() * 100, 1),
            "pct_wave_sal":    round((livreurs["mode_paiement_prefere"] == "Wave").mean() * 100, 1),
            "pct_hybride":     round(livreurs["modele_remuneration_prefere"].str.contains("bonus", na=False).mean() * 100, 1),
            "pct_soir":        round((livreurs["disponibilite_soir"] == "Oui").mean() * 100, 1),
            "pct_wave_compte": round((livreurs["compte_wave"] == "Oui").mean() * 100, 1),
            "zones":           zones_series.to_dict(),
            "sources":         livreurs["source_restaurant"].value_counts().to_dict() if "source_restaurant" in livreurs.columns else {},
        }
    else:
        result["livreurs"] = {
            "n_entretiens": 23,
            "sources": {"Moaye": 5, "Swice Palace": 4, "Bazof": 4, "Yum Yum": 4, "Indépendants": 6},
        }

    # ── Restaurants ──────────────────────────────────────────
    if not restaurants.empty:
        result["restaurants"] = {
            "n_discussions":         8,   # 8 établissements dont Trophet, Chez Mervi, Chez Maman Gaga

            "pct_whatsapp":          round(restaurants["gestion_commandes_actuelle"].str.contains("WhatsApp", na=False).mean() * 100, 1),
            "pct_wave":              round(restaurants["mode_paiement_recu"].str.contains("Wave", na=False).mean() * 100, 1),
            "pct_livreurs_propres":  round((restaurants["livreurs_propres"] == "Oui").mean() * 100, 1),
            "pct_internet_stable":   round((restaurants.get("internet_stable", pd.Series(["Oui"]*len(restaurants))) == "Oui").mean() * 100, 1),
        }
    else:
        result["restaurants"] = {
            "n_discussions":   8,
            "etablissements":  ["4 restaurants internationaux", "Swice Palace",
                                "Trophet", "Chez Mervi", "Chez Maman Gaga"],
            "pct_whatsapp":    100,
            "pct_wave":        80,
            "pct_livreurs_propres": 40,
            "pct_internet_stable":  80,
        }

    # ── Benchmarks ───────────────────────────────────────────
    if not benchmarks.empty:
        result["benchmarks"] = benchmarks.to_dict("records")
    else:
        result["benchmarks"] = []

    return result

# ══════════════════════════════════════════════════════════════
# 3. MODÈLE DE CROISSANCE (COURBE S)
# ══════════════════════════════════════════════════════════════

def _s_curve(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

def compute_mau_series(params=None, scenario="central"):
    """Retourne un ndarray de 60 valeurs MAU (5 ans)."""
    p = {**DEFAULT_PARAMS, **(params or {})}
    mois = np.arange(1, 61)
    if scenario == "central":
        return _s_curve(mois, p["mau_L"], p["mau_k"], p["mau_t0"])
    elif scenario == "pessimiste":
        return _s_curve(mois, p["mau_L_pess"], p["mau_k_pess"], p["mau_t0_pess"])
    elif scenario == "optimiste":
        return _s_curve(mois, p["mau_L_opt"], p["mau_k_opt"], p["mau_t0_opt"])

# ══════════════════════════════════════════════════════════════
# 4. MODÈLE DE REVENUS (7 FLUX NETS)
# ══════════════════════════════════════════════════════════════

def _commission_rate(cmd_par_rest):
    """Commission dégrésive selon le volume de commandes par restaurant par mois."""
    if cmd_par_rest < 100:  return 0.025
    if cmd_par_rest < 500:  return 0.020
    if cmd_par_rest < 1500: return 0.015
    return 0.010


def compute_revenues(mau_array, params=None):
    """Calcule les revenus mensuels pour chaque valeur MAU."""
    p = {**DEFAULT_PARAMS, **(params or {})}
    result = []
    for i, mau in enumerate(mau_array):
        pct_ecantine = min(0.30 + i * 0.010, 0.80)
        cmd = mau * p["avg_cmd_par_mau"]

        # ① Frais de livraison — revenue principal
        rev_livraison = cmd * p["frais_livraison_moy"] * pct_ecantine * p["marge_livraison"]

        # ② Commission dégrésive par volume — sur commandes via app uniquement
        n_rest = max(1, min(mau / p.get("mau_par_rest", 35), p["nb_rest_cible_an1"]))
        cmd_par_rest = cmd / n_rest
        taux_comm = _commission_rate(cmd_par_rest)
        rev_commission = cmd * p.get("pct_app_orders", 0.85) * p["avg_basket"] * taux_comm

        # ③ Abonnements restaurants Pro + Premium (inclut visibilité — pub absorbée)
        rev_abo = (n_rest * p["pct_pro"] * p["prix_pro"] +
                   n_rest * p["pct_premium"] * p["prix_premium"])

        # ④ Publicité in-app — absorbée dans les abonnements Pro/Premium
        rev_pub = 0

        # ⑤ B2B — Cantines entreprises (à partir du mois 10)
        rev_b2b = max(0, min((i - 9) * 150_000 * 0.01, 3_000_000)) if i > 9 else 0

        # ⑥ E-cantine Vitrine — commission 5% sur menus prix fixe (mois 4+)
        rev_selection = cmd * p["avg_basket"] * 0.08 * 0.05 if i > 3 else 0

        # ⑦ Livraisons propres restaurants — 2,5% de dispatch (corrigé de 1,5%)
        rev_propres = cmd * p["avg_basket"] * (1 - pct_ecantine) * 0.025

        total = (rev_livraison + rev_commission + rev_abo +
                 rev_pub + rev_b2b + rev_selection + rev_propres)

        result.append({
            "mois":              i + 1,
            "mau":               int(mau),
            "commandes":         int(cmd),
            "n_restaurants":     int(round(n_rest)),
            "pct_ecantine_liv":  round(pct_ecantine * 100, 1),
            "rev_livraison":     int(rev_livraison),
            "rev_commission":    int(rev_commission),
            "rev_abonnements":   int(rev_abo),
            "rev_pub":           int(rev_pub),
            "rev_b2b":           int(rev_b2b),
            "rev_selection":     int(rev_selection),
            "rev_propres":       int(rev_propres),
            "total_mensuel":     int(total),
        })
    return result

# ══════════════════════════════════════════════════════════════
# 5. MODÈLE DE COÛTS
# ══════════════════════════════════════════════════════════════

def compute_costs(mau_array, revenues, params=None):
    """Calcule les coûts mensuels en fonction du MAU et des revenus."""
    p = {**DEFAULT_PARAMS, **(params or {})}
    result = []
    for i, (mau, rev) in enumerate(zip(mau_array, revenues)):
        mau_k = mau / 1_000
        rev_total = rev["total_mensuel"]

        # Salaires : base + croissance avec l'équipe
        salaires = p["salaires_base"] + mau_k * p["salaires_par_kmau"]

        # Marketing : % du CA + minimum fixe
        marketing = max(p["marketing_fixe"], rev_total * p["marketing_pct_rev"])

        # Tech & infra
        tech = p["tech_base"] + mau_k * p["tech_par_kmau"]

        # Opérations & admin
        operations = p["operations_base"] + mau_k * p["operations_par_kmau"]

        total_couts = salaires + marketing + tech + operations
        marge_nette = rev_total - total_couts

        result.append({
            "mois":             i + 1,
            "cout_salaires":    int(salaires),
            "cout_marketing":   int(marketing),
            "cout_tech":        int(tech),
            "cout_operations":  int(operations),
            "total_couts":      int(total_couts),
            "marge_nette":      int(marge_nette),
            "marge_pct":        round(marge_nette / rev_total * 100, 1) if rev_total > 0 else -100.0,
        })
    return result

# ══════════════════════════════════════════════════════════════
# 6. INDICATEURS FINANCIERS
# ══════════════════════════════════════════════════════════════

def _annual_sum(monthly_data, key, an):
    s = (an - 1) * 12
    return sum(r[key] for r in monthly_data[s:s + 12])

def compute_financials(rev_monthly, cost_monthly, params=None):
    """Calcule VAN, TRI, IP, délai de récupération et P&L mensuel."""
    p = {**DEFAULT_PARAMS, **(params or {})}

    # Flux annuels nets (revenus - coûts)
    flux = [-p["investissement"]]
    for an in range(1, 6):
        flux.append(
            _annual_sum(rev_monthly, "total_mensuel", an) -
            _annual_sum(cost_monthly, "total_couts", an)
        )

    # VAN
    van = sum(f / (1 + p["taux_actualisation"]) ** t for t, f in enumerate(flux))
    ip = (van + p["investissement"]) / p["investissement"]

    # TRI
    try:
        tri = brentq(
            lambda r: sum(f / (1 + r) ** t for t, f in enumerate(flux)),
            -0.99, 50.0
        ) * 100
    except Exception:
        tri = None

    # Délai de récupération (mois)
    cumul = -p["investissement"]
    dr = None
    for i, r in enumerate(rev_monthly):
        cumul += r["total_mensuel"] - cost_monthly[i]["total_couts"]
        if cumul >= 0 and dr is None:
            dr = i + 1

    # Profil mensuel P&L + cumul
    cumul = -p["investissement"]
    monthly_profit = []
    for i, r in enumerate(rev_monthly):
        profit = r["total_mensuel"] - cost_monthly[i]["total_couts"]
        cumul += profit
        monthly_profit.append({
            "mois":            i + 1,
            "profit_mensuel":  int(profit),
            "cumul":           int(cumul),
        })

    return {
        "van":         int(van),
        "van_M":       round(van / 1e6, 2),
        "tri":         round(tri, 1) if tri is not None else None,
        "ip":          round(ip, 2),
        "delai_mois":  dr,
        "flux_annuels": flux,
        "monthly_profit": monthly_profit,
    }

# ══════════════════════════════════════════════════════════════
# 7. MONTE CARLO (1 000 SIMULATIONS)
# ══════════════════════════════════════════════════════════════

def run_monte_carlo(n=1000, params=None):
    """
    Simule N variantes du modèle avec des paramètres perturbés aléatoirement.
    Retourne les percentiles P10/P50/P90 du CA An5 et de la VAN.
    """
    p = {**DEFAULT_PARAMS, **(params or {})}
    rng = np.random.default_rng(42)

    ca5_list, van_list, ca3_list = [], [], []

    for _ in range(n):
        perturbed = {
            **p,
            "avg_basket":          p["avg_basket"]          * rng.uniform(0.75, 1.35),
            "avg_cmd_par_mau":     p["avg_cmd_par_mau"]     * rng.uniform(0.80, 1.25),
            "frais_livraison_moy": p["frais_livraison_moy"] * rng.uniform(0.75, 1.30),
            "marge_livraison":     min(0.65, p["marge_livraison"] * rng.uniform(0.80, 1.25)),
            "mau_L":               p["mau_L"]               * rng.uniform(0.60, 1.50),
            "mau_k":               p["mau_k"]               * rng.uniform(0.75, 1.30),
            "marketing_pct_rev":   p["marketing_pct_rev"]   * rng.uniform(0.80, 1.30),
            "salaires_base":       p["salaires_base"]        * rng.uniform(0.90, 1.20),
        }
        mau  = compute_mau_series(perturbed, "central")
        rev  = compute_revenues(mau, perturbed)
        cost = compute_costs(mau, rev, perturbed)
        fin  = compute_financials(rev, cost, perturbed)

        ca5  = sum(r["total_mensuel"] for r in rev[48:60])
        ca3  = sum(r["total_mensuel"] for r in rev[24:36])
        ca5_list.append(ca5)
        ca3_list.append(ca3)
        van_list.append(fin["van"])

    ca5_arr = np.array(ca5_list)
    ca3_arr = np.array(ca3_list)
    van_arr = np.array(van_list)

    return {
        "n_simulations": n,
        "ca5": {
            "p10": int(np.percentile(ca5_arr, 10)),
            "p25": int(np.percentile(ca5_arr, 25)),
            "p50": int(np.percentile(ca5_arr, 50)),
            "p75": int(np.percentile(ca5_arr, 75)),
            "p90": int(np.percentile(ca5_arr, 90)),
            "mean": int(np.mean(ca5_arr)),
            "values": [int(x) for x in ca5_list[:300]],
        },
        "ca3": {
            "p10": int(np.percentile(ca3_arr, 10)),
            "p50": int(np.percentile(ca3_arr, 50)),
            "p90": int(np.percentile(ca3_arr, 90)),
        },
        "van": {
            "p10":          int(np.percentile(van_arr, 10)),
            "p50":          int(np.percentile(van_arr, 50)),
            "p90":          int(np.percentile(van_arr, 90)),
            "pct_positive": float(round((van_arr > 0).mean() * 100, 1)),
            "values":       [int(x) for x in van_list[:300]],
        },
        "monthly_bands": _compute_bands(p, rng, n_sample=200),
    }

def _compute_bands(p, rng, n_sample=200):
    """Calcule les bandes P10/P90 MAU mois par mois (sous-ensemble rapide)."""
    mau_matrix = []
    for _ in range(n_sample):
        perturbed = {
            **p,
            "mau_L": p["mau_L"] * rng.uniform(0.60, 1.50),
            "mau_k": p["mau_k"] * rng.uniform(0.75, 1.30),
            "mau_t0": p["mau_t0"] * rng.uniform(0.85, 1.15),
        }
        mau_matrix.append(compute_mau_series(perturbed, "central"))
    mat = np.array(mau_matrix)
    return {
        "p10": [int(x) for x in np.percentile(mat, 10, axis=0)],
        "p90": [int(x) for x in np.percentile(mat, 90, axis=0)],
    }

# ══════════════════════════════════════════════════════════════
# 8. ANALYSE DE SENSIBILITÉ (TORNADO)
# ══════════════════════════════════════════════════════════════

def sensitivity_analysis(params=None):
    """
    Mesure l'impact de ±Δ% sur chaque paramètre clé sur le CA An3.
    Retourne une liste triée par impact décroissant (tornado chart).
    """
    p = {**DEFAULT_PARAMS, **(params or {})}

    # Cas de base
    mau_base = compute_mau_series(p)
    rev_base = compute_revenues(mau_base, p)
    ca3_base = sum(r["total_mensuel"] for r in rev_base[24:36])

    params_to_test = {
        "avg_basket":           ("Panier moyen",           0.20),
        "avg_cmd_par_mau":      ("Commandes / MAU",        0.20),
        "frais_livraison_moy":  ("Frais de livraison",     0.25),
        "marge_livraison":      ("Marge livraison",        0.15),
        "mau_L":                ("MAU plateau",            0.25),
        "commission_starter":   ("Commission Starter",     0.20),
        "pct_starter":          ("% formule Starter",      0.15),
        "mau_k":                ("Vitesse croissance",     0.20),
    }

    results = []
    for key, (label, delta) in params_to_test.items():
        for sign, tag in [(+1, "up"), (-1, "dn")]:
            p_var = {**p, key: p[key] * (1 + sign * delta)}
            if key == "marge_livraison":
                p_var[key] = min(0.70, p_var[key])
            mau_v = compute_mau_series(p_var)
            rev_v = compute_revenues(mau_v, p_var)
            ca3_v = sum(r["total_mensuel"] for r in rev_v[24:36])
            impact = (ca3_v - ca3_base) / ca3_base * 100 if ca3_base else 0
            results.append({
                "param": key, "label": label,
                "delta_pct": delta * 100, "tag": tag,
                "impact_pct": round(impact, 1),
            })

    # Regroupement par paramètre
    grouped = {}
    for r in results:
        k = r["param"]
        if k not in grouped:
            grouped[k] = {"param": k, "label": r["label"], "delta_pct": r["delta_pct"],
                          "impact_up": 0, "impact_dn": 0}
        if r["tag"] == "up":
            grouped[k]["impact_up"] = r["impact_pct"]
        else:
            grouped[k]["impact_dn"] = r["impact_pct"]

    sorted_list = sorted(grouped.values(), key=lambda x: abs(x["impact_up"]), reverse=True)
    return sorted_list, ca3_base

# ══════════════════════════════════════════════════════════════
# 9. POINT D'ENTRÉE PRINCIPAL
# ══════════════════════════════════════════════════════════════

def run_model(params=None, run_mc=False, n_mc=1000):
    """
    Exécute le modèle complet et retourne un dict de résultats.
    Utilisé par app.py (Streamlit) et par le CLI.

    Args:
        params     : dict de surcharge des DEFAULT_PARAMS
        run_mc     : True pour lancer la simulation Monte Carlo
        n_mc       : nombre de simulations Monte Carlo
    """
    p = {**DEFAULT_PARAMS, **(params or {})}
    data    = load_data()
    terrain = analyze_terrain(data)

    # MAU — 3 scénarios
    mau_c = compute_mau_series(p, "central")
    mau_p = compute_mau_series(p, "pessimiste")
    mau_o = compute_mau_series(p, "optimiste")

    # Revenus
    rev_c = compute_revenues(mau_c, p)
    rev_p = compute_revenues(mau_p, p)
    rev_o = compute_revenues(mau_o, p)

    # Coûts (scénario central)
    cost_c = compute_costs(mau_c, rev_c, p)

    # Financiers
    fin_c = compute_financials(rev_c, cost_c, p)

    # CA annuel pour chaque scénario
    def ca(revs, an):
        return sum(r["total_mensuel"] for r in revs[(an - 1) * 12: an * 12])

    ca_c = {f"an{i}": ca(rev_c, i) for i in range(1, 6)}
    ca_p = {f"an{i}": ca(rev_p, i) for i in range(1, 6)}
    ca_o = {f"an{i}": ca(rev_o, i) for i in range(1, 6)}

    # Décomposition CA An 1
    r1 = rev_c[:12]
    decomp_an1 = {
        "livraison":   sum(r["rev_livraison"]   for r in r1),
        "commission":  sum(r["rev_commission"]  for r in r1),
        "abonnements": sum(r["rev_abonnements"] for r in r1),
        "pub":         sum(r["rev_pub"]         for r in r1),
        "b2b":         sum(r["rev_b2b"]         for r in r1),
        "selection":   sum(r["rev_selection"]   for r in r1),
        "propres":     sum(r["rev_propres"]     for r in r1),
    }

    # Sensibilité
    sensitivity, _ = sensitivity_analysis(p)

    result = {
        "metadata": {
            "projet":           "E-cantine",
            "version_bp":       "V7",
            "date_generation":  datetime.now().strftime("%Y-%m-%d %H:%M"),
            "methode": (
                "Données terrain (formulaire clients, 23 entretiens livreurs, "
                "5 discussions restaurants) + Benchmarks publics concurrents + "
                "Modèle prédiction IA (courbe S logistique, calibrée Chowdeck Nigeria "
                "× Facteur Dakar 0.238)"
            ),
            "note": (
                "Panel limité — projections produites par modèle statistique. "
                "Estimations affinées dès 300 répondants clients."
            ),
            "sources": [
                "ANSD RGPH-5 2023", "ARTP 2023", "The Africa Report 2023 (Wave 8M)",
                "Hub2 2025 (paiements SN)", "Innovation Village 2025 (marché livraison)",
                "RentechDigital mai 2025 (1439 restaurants Dakar)",
                "Techpoint Africa 2025 (Chowdeck)", "AITN fév. 2025 (Yango Food)",
                "TechCrunch déc. 2023 (Jumia Food)",
            ],
            "data_cutoff": "Janvier 2026",
        },
        "terrain": terrain,
        "params": {k: p[k] for k in [
            "commission_starter", "commission_pro", "commission_premium",
            "frais_livraison_moy", "marge_livraison", "avg_basket",
            "avg_cmd_par_mau", "investissement", "taux_actualisation",
        ]},
        "mau": {
            "central_series":    [int(x) for x in mau_c],
            "pessimiste_series": [int(x) for x in mau_p],
            "optimiste_series":  [int(x) for x in mau_o],
            "central":     {f"an{i+1}": int(mau_c[(i + 1) * 12 - 1]) for i in range(5)},
            "pessimiste":  {f"an{i+1}": int(mau_p[(i + 1) * 12 - 1]) for i in range(5)},
            "optimiste":   {f"an{i+1}": int(mau_o[(i + 1) * 12 - 1]) for i in range(5)},
        },
        "ca_annuel": {
            "central":    ca_c,
            "pessimiste": ca_p,
            "optimiste":  ca_o,
            "decomp_an1": decomp_an1,
        },
        "financiers": {
            **fin_c,
            "budget_fcfa":        p["investissement"],
            "taux_actualisation": p["taux_actualisation"],
        },
        "monthly": {
            "revenues": rev_c,
            "costs":    cost_c,
            "profit":   fin_c["monthly_profit"],
        },
        "sensitivity": sensitivity,
    }

    if run_mc:
        result["monte_carlo"] = run_monte_carlo(n=n_mc, params=p)

    return result

# ══════════════════════════════════════════════════════════════
# CLI — python predict.py
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    G = "\033[92m"; B = "\033[94m"; Y = "\033[93m"
    BOLD = "\033[1m"; END = "\033[0m"

    def titre(t):
        print(f"\n{BOLD}{G}{'='*60}{END}")
        print(f"{BOLD}{G}  {t}{END}")
        print(f"{BOLD}{G}{'='*60}{END}")

    def ok(label, val, note=""):
        n = f"  {Y}({note}){END}" if note else ""
        print(f"  {G}✓{END} {label:<40} {BOLD}{val}{END}{n}")

    def info(t):
        print(f"  {B}ℹ{END}  {t}")

    titre("E-CANTINE · Modèle de Prédiction IA · V7")
    print(f"\n  Lancement du modèle...\n")

    res = run_model(run_mc=True, n_mc=500)

    t   = res["terrain"]
    m   = res["mau"]
    ca  = res["ca_annuel"]
    fin = res["financiers"]
    mc  = res["monte_carlo"]

    titre("Données Terrain")
    cli = t.get("clients", {})
    ok("Répondants clients",  cli.get("n_repondants", 0),  f"Objectif : {cli.get('objectif_cible', 300)}")
    ok("Dont étudiants",      f"{cli.get('pct_etudiants', 0):.0f}%")
    ok("Wave paiement",       f"{cli.get('pct_wave', 0):.0f}%")
    ok("Très intéressés",     f"{cli.get('pct_tres_interesse', 0):.0f}%")
    ok("Entretiens livreurs", res["terrain"]["livreurs"].get("n_entretiens", 0))
    ok("Discussions restaurants", res["terrain"]["restaurants"].get("n_discussions", 0))

    titre("Projections MAU (scénario central)")
    for an, idx in [("An 1 (2027)", 11), ("An 3 (2029)", 35), ("An 5 (2031)", 59)]:
        print(f"  MAU {an} :  Pess {m['pessimiste_series'][idx]:>8,}  "
              f"{BOLD}Central {m['central_series'][idx]:>8,}{END}  "
              f"Optim {m['optimiste_series'][idx]:>8,}")

    titre("Chiffre d'Affaires Annuel (FCFA)")
    for an in range(1, 6):
        cc = ca["central"][f"an{an}"]
        cp = ca["pessimiste"][f"an{an}"]
        co = ca["optimiste"][f"an{an}"]
        print(f"  An {an} (20{26+an}) :  Pess {cp/1e6:>6.1f}M  "
              f"{BOLD}Central {cc/1e6:>6.1f}M{END}  Optim {co/1e6:>6.1f}M FCFA")

    titre("Indicateurs Financiers")
    ok("VAN (5 ans, 15%)",         f"{fin['van_M']:.1f}M FCFA",   "✅" if fin["van"] > 0 else "❌")
    ok("TRI",                       f"{fin['tri']}%",               "✅" if (fin['tri'] or 0) > 9 else "❌")
    ok("Indice de Profitabilité",   f"{fin['ip']:.2f}",             "✅" if fin['ip'] > 1 else "❌")
    if fin["delai_mois"]:
        ok("Délai récupération",    f"{fin['delai_mois']//12} ans {fin['delai_mois']%12} mois")

    titre("Monte Carlo (500 simulations)")
    ok("CA An5 — P10",   f"{mc['ca5']['p10']/1e6:.1f}M FCFA")
    ok("CA An5 — médiane", f"{mc['ca5']['p50']/1e6:.1f}M FCFA")
    ok("CA An5 — P90",   f"{mc['ca5']['p90']/1e6:.1f}M FCFA")
    ok("VAN positive",   f"{mc['van']['pct_positive']:.0f}% des simulations")

    # Export JSON
    out_path = os.path.join(BASE, "outputs", "results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)

    titre(f"✅ Export → {out_path}")
    info("Lance : streamlit run app.py")
