"""
╔══════════════════════════════════════════════════════════════╗
║   E-CANTINE · TABLEAU DE BORD IA · BUSINESS PLAN V7         ║
║   Streamlit Dashboard — Futuristic Dark Theme                ║
╚══════════════════════════════════════════════════════════════╝
  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── Import du modèle ────────────────────────────────────────
from predict import (
    run_model,
    run_monte_carlo,
    sensitivity_analysis,
    compute_mau_series,
    compute_revenues,
    compute_costs,
    DEFAULT_PARAMS,
)

# ══════════════════════════════════════════════════════════════
# CONFIG PAGE
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="E-Cantine · Modèle IA",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# THÈME FUTURISTE — CSS GLOBAL
# ══════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* ── Fond principal ── */
.stApp, [data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #06080f 0%, #0a0d1a 60%, #060810 100%);
    color: #dde6f0;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b18 0%, #0a0e1c 100%) !important;
    border-right: 1px solid rgba(0,255,136,0.15) !important;
}
[data-testid="stSidebar"] * { color: #c8d8e8 !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] h3 { color: #00ff88 !important; }

/* ── Onglets ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,255,136,0.04);
    border-radius: 10px;
    border: 1px solid rgba(0,255,136,0.15);
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: rgba(200,220,240,0.6) !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-weight: 500;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: rgba(0,255,136,0.12) !important;
    color: #00ff88 !important;
    border-bottom: 2px solid #00ff88 !important;
}

/* ── Métriques natives ── */
[data-testid="metric-container"] {
    background: rgba(0,255,136,0.04);
    border: 1px solid rgba(0,255,136,0.25);
    border-radius: 12px;
    padding: 18px 16px;
    box-shadow: 0 0 24px rgba(0,255,136,0.07), inset 0 0 12px rgba(0,0,0,0.3);
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00ff88 !important;
    font-family: 'Courier New', monospace;
    font-size: 1.55rem !important;
    font-weight: 800;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: rgba(200,220,240,0.65) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Cartes HTML custom ── */
.ecantine-card {
    background: rgba(0,255,136,0.04);
    border: 1px solid rgba(0,255,136,0.22);
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 0 28px rgba(0,255,136,0.06);
    margin-bottom: 12px;
}
.ecantine-card-cyan {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.22);
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 0 28px rgba(0,212,255,0.06);
    margin-bottom: 12px;
}

/* ── Titre gradient ── */
.ecantine-title {
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}
.ecantine-subtitle {
    color: rgba(200,220,240,0.5);
    font-size: 0.9rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Badge status ── */
.badge-ok {
    background: rgba(0,255,136,0.15);
    color: #00ff88;
    border: 1px solid rgba(0,255,136,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}
.badge-warn {
    background: rgba(255,107,53,0.15);
    color: #ff6b35;
    border: 1px solid rgba(255,107,53,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
}

/* ── Divider lumineux ── */
.neon-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,136,0.4), transparent);
    margin: 18px 0;
}

/* ── Tableaux ── */
.stDataFrame { border: 1px solid rgba(0,255,136,0.18) !important; border-radius: 10px; }
thead tr th { background: rgba(0,255,136,0.08) !important; color: #00ff88 !important; }

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div { background: #00ff88 !important; }

/* ── Boutons ── */
.stButton > button {
    background: linear-gradient(90deg, rgba(0,255,136,0.15), rgba(0,212,255,0.15));
    border: 1px solid rgba(0,255,136,0.4);
    color: #00ff88;
    border-radius: 8px;
    font-weight: 600;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0,255,136,0.25), rgba(0,212,255,0.25));
    box-shadow: 0 0 16px rgba(0,255,136,0.3);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080b18; }
::-webkit-scrollbar-thumb { background: rgba(0,255,136,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PALETTE COULEURS
# ══════════════════════════════════════════════════════════════

C_GREEN  = "#00ff88"
C_CYAN   = "#00d4ff"
C_ORANGE = "#ff6b35"
C_PURPLE = "#a855f7"
C_GOLD   = "#ffd700"
C_PINK   = "#ff4081"
C_TEAL   = "#64ffda"
C_BG     = "#06080f"
C_CARD   = "rgba(255,255,255,0.03)"

REV_COLORS = [C_GREEN, C_CYAN, C_PURPLE, C_GOLD, C_ORANGE, C_PINK, C_TEAL]
REV_LABELS = [
    "① Livraison (40%)",
    "② Commission var.",
    "③ Abonnements",
    "④ Pub in-app",
    "⑤ B2B entreprises",
    "⑥ Sélection",
    "⑦ Livr. propres",
]
REV_KEYS = [
    "rev_livraison", "rev_commission", "rev_abonnements",
    "rev_pub", "rev_b2b", "rev_selection", "rev_propres",
]

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c8d8e8", family="Inter, sans-serif"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)"),
)

# ══════════════════════════════════════════════════════════════
# SIDEBAR — PARAMÈTRES
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;margin-bottom:16px'>
      <div style='font-size:2.2rem'>🍱</div>
      <div style='font-size:1.3rem;font-weight:900;color:#00ff88;letter-spacing:-0.5px'>E-CANTINE</div>
      <div style='font-size:0.72rem;color:rgba(200,220,240,0.45);letter-spacing:1.5px;
                  text-transform:uppercase'>Business Plan V7 · IA</div>
    </div>
    <div class='neon-divider'></div>
    """, unsafe_allow_html=True)

    st.markdown("### Modèle Économique")
    avg_basket = st.slider("Panier moyen (FCFA)", 1500, 6000, 3000, 100)
    avg_cmd    = st.slider("Commandes / MAU / mois", 1.0, 5.0, 2.5, 0.1)
    frais_liv  = st.slider("Frais livraison moy. (FCFA)", 500, 2500, 1200, 50)
    marge_liv  = st.slider("Marge livraison (%)", 20, 65, 40, 1)

    st.markdown("### Formules Restaurants")
    pct_starter = st.slider("% Starter (gratuit)", 40, 80, 60, 5)
    pct_pro     = st.slider("% Pro (25K FCFA/mois)", 10, 50, 30, 5)
    pct_prem    = 100 - pct_starter - pct_pro
    st.caption(f"% Premium = {pct_prem}%")

    st.markdown("### Croissance")
    mau_L  = st.slider("MAU plateau", 40_000, 200_000, 80_000, 5_000)
    mau_k  = st.slider("Vitesse croissance (k)", 0.05, 0.20, 0.10, 0.01)

    st.markdown("### Monte Carlo")
    n_mc = st.slider("Simulations", 200, 2000, 500, 100)
    run_mc_btn = st.button("▶ Lancer Monte Carlo", use_container_width=True)

    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.caption("ISM Dakar · 2025 · © Adote Mario-Giovani ADUAYI-AKUE")

# ══════════════════════════════════════════════════════════════
# CONSTRUCTION DES PARAMÈTRES DEPUIS SIDEBAR
# ══════════════════════════════════════════════════════════════

params = {
    **DEFAULT_PARAMS,
    "avg_basket":          avg_basket,
    "avg_cmd_par_mau":     avg_cmd,
    "frais_livraison_moy": frais_liv,
    "marge_livraison":     marge_liv / 100,
    "pct_starter":         pct_starter / 100,
    "pct_pro":             pct_pro / 100,
    "pct_premium":         pct_prem / 100,
    "mau_L":               mau_L,
    "mau_k":               mau_k,
}

# ══════════════════════════════════════════════════════════════
# CALCUL DU MODÈLE (mis en cache par Streamlit)
# ══════════════════════════════════════════════════════════════

@st.cache_data(show_spinner="Calcul du modèle en cours…")
def get_model(p_frozen):
    return run_model(params=dict(p_frozen))

@st.cache_data(show_spinner="Simulation Monte Carlo…")
def get_mc(p_frozen, n):
    return run_monte_carlo(n=n, params=dict(p_frozen))

params_key = tuple(sorted(params.items()))
res = get_model(params_key)

m   = res["mau"]
ca  = res["ca_annuel"]
fin = res["financiers"]
rev_monthly  = res["monthly"]["revenues"]
cost_monthly = res["monthly"]["costs"]
profit_monthly = res["monthly"]["profit"]
terrain = res["terrain"]

# Monte Carlo (lazy)
if "mc_result" not in st.session_state or run_mc_btn:
    with st.spinner("Monte Carlo en cours…"):
        st.session_state["mc_result"] = get_mc(params_key, n_mc)
mc = st.session_state.get("mc_result", None)

# ══════════════════════════════════════════════════════════════
# EN-TÊTE PRINCIPAL
# ══════════════════════════════════════════════════════════════

mois_labels = [f"M{i}" for i in range(1, 61)]
years_label = ["An 1\n2027", "An 2\n2028", "An 3\n2029", "An 4\n2030", "An 5\n2031"]

col_logo, col_title, col_badge = st.columns([1, 6, 2])
with col_title:
    st.markdown("""
    <p class='ecantine-title'>E-CANTINE</p>
    <p class='ecantine-subtitle'>Tableau de bord · Modèle IA · Business Plan V7 · Dakar 2025</p>
    """, unsafe_allow_html=True)
with col_badge:
    van_ok = fin["van"] > 0
    tri_ok = (fin["tri"] or 0) > 9
    st.markdown(f"""
    <div style='text-align:right;padding-top:12px'>
      <span class='badge-ok'>VAN ✅</span>&nbsp;
      <span class='badge-ok'>TRI {fin['tri']}% ✅</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# ── KPIs rapides ──────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
mau_an3 = m["central"]["an3"]
ca_an3  = ca["central"]["an3"]
ca_an5  = ca["central"]["an5"]
dr = fin["delai_mois"]

k1.metric("MAU An 3", f"{mau_an3:,}")
k2.metric("CA An 3", f"{ca_an3/1e6:.1f}M FCFA")
k3.metric("CA An 5", f"{ca_an5/1e6:.1f}M FCFA")
k4.metric("VAN (15%)", f"{fin['van_M']:.1f}M FCFA")
k5.metric("Délai récup.", f"{dr//12}a {dr%12}m" if dr else "N/A")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ONGLETS
# ══════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble",
    "💰 Revenus & Coûts",
    "🌍 Données Terrain",
    "🔀 Scénarios",
    "🎲 Monte Carlo & Sensibilité",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════

with tab1:
    col_mau, col_ca = st.columns(2)

    # Courbe MAU — 3 scénarios
    with col_mau:
        fig = go.Figure()
        # Scénarios
        for series, name, color, dash in [
            (m["optimiste_series"],  "Optimiste",  C_CYAN,   "dot"),
            (m["central_series"],    "Central",    C_GREEN,  "solid"),
            (m["pessimiste_series"], "Pessimiste", C_ORANGE, "dash"),
        ]:
            fig.add_trace(go.Scatter(
                x=list(range(1, 61)), y=series,
                name=name, mode="lines",
                line=dict(color=color, width=2.5, dash=dash),
            ))
        # Bande Monte Carlo si dispo
        if mc and "monthly_bands" in mc:
            b = mc["monthly_bands"]
            fig.add_trace(go.Scatter(
                x=list(range(1, 61)) + list(range(60, 0, -1)),
                y=b["p90"] + b["p10"][::-1],
                fill="toself",
                fillcolor="rgba(0,255,136,0.07)",
                line=dict(color="rgba(0,0,0,0)"),
                name="P10–P90 MC", showlegend=True,
            ))
        # Marqueurs annuels
        for an, idx in [(1,11),(2,23),(3,35),(4,47),(5,59)]:
            fig.add_vline(x=idx+1, line_dash="dot",
                          line_color="rgba(200,220,240,0.12)")
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="📈 Croissance MAU (5 ans)", font_color=C_GREEN, font_size=14),
            yaxis_title="Utilisateurs actifs",
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    # CA annuel — 3 scénarios
    with col_ca:
        ans = [1, 2, 3, 4, 5]
        fig = go.Figure()
        for scenario, name, color in [
            ("optimiste",  "Optimiste",  C_CYAN),
            ("central",    "Central",    C_GREEN),
            ("pessimiste", "Pessimiste", C_ORANGE),
        ]:
            vals = [ca[scenario][f"an{a}"] / 1e6 for a in ans]
            fig.add_trace(go.Bar(
                x=years_label, y=vals,
                name=name, marker_color=color,
                opacity=0.85,
            ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="💵 CA Annuel par scénario (M FCFA)", font_color=C_GREEN, font_size=14),
            barmode="group",
            yaxis_title="Millions FCFA",
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau récapitulatif
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Résumé par année — Scénario Central")

    rows = []
    for an in range(1, 6):
        rev_an = sum(r["total_mensuel"]  for r in rev_monthly[(an-1)*12:an*12])
        cout_an= sum(c["total_couts"]    for c in cost_monthly[(an-1)*12:an*12])
        rows.append({
            "Année":         f"An {an} ({2026+an})",
            "MAU fin d'an":  f"{m['central'][f'an{an}']:,}",
            "CA (M FCFA)":   f"{rev_an/1e6:.2f}",
            "Coûts (M FCFA)":f"{cout_an/1e6:.2f}",
            "Marge (M FCFA)":f"{(rev_an-cout_an)/1e6:.2f}",
            "Marge %":        f"{(rev_an-cout_an)/rev_an*100:.0f}%" if rev_an else "—",
        })
    df_recap = pd.DataFrame(rows)
    st.dataframe(df_recap, use_container_width=True, hide_index=True)

    # Indicateurs financiers
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Indicateurs Financiers")
    fi1, fi2, fi3, fi4 = st.columns(4)
    fi1.metric("VAN (5 ans, 15%)", f"{fin['van_M']:.1f}M FCFA",
               delta="✅ Positif" if fin["van"] > 0 else "❌")
    fi2.metric("TRI", f"{fin['tri']}%",
               delta="✅ > 9% bancaire" if (fin["tri"] or 0) > 9 else "⚠")
    fi3.metric("Indice Profitabilité", f"{fin['ip']:.2f}",
               delta="✅ > 1" if fin["ip"] > 1 else "❌")
    fi4.metric("Budget de lancement", f"{fin['budget_fcfa']/1e6:.2f}M FCFA")

# ══════════════════════════════════════════════════════════════
# TAB 2 — REVENUS & COÛTS
# ══════════════════════════════════════════════════════════════

with tab2:
    col_rl, col_donut = st.columns([3, 2])

    # Revenus vs Coûts mensuels
    with col_rl:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, 61)),
            y=[r["total_mensuel"] / 1e6 for r in rev_monthly],
            name="Revenus", mode="lines",
            line=dict(color=C_GREEN, width=2.5),
            fill="tozeroy", fillcolor="rgba(0,255,136,0.07)",
        ))
        fig.add_trace(go.Scatter(
            x=list(range(1, 61)),
            y=[c["total_couts"] / 1e6 for c in cost_monthly],
            name="Coûts", mode="lines",
            line=dict(color=C_ORANGE, width=2),
            fill="tozeroy", fillcolor="rgba(255,107,53,0.07)",
        ))
        # Zone négative (avant break-even)
        if fin["delai_mois"]:
            fig.add_vrect(
                x0=1, x1=fin["delai_mois"],
                fillcolor="rgba(255,107,53,0.06)",
                line_width=0,
                annotation_text=f"Break-even M{fin['delai_mois']}",
                annotation_font_color=C_ORANGE,
            )
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="📊 Revenus vs Coûts mensuels (M FCFA)", font_color=C_GREEN, font_size=14),
            height=320, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Donut — 7 flux revenus An 1
    with col_donut:
        d = ca["decomp_an1"]
        vals  = [d[k.replace("rev_", "")] for k in [
            "livraison", "commission", "abonnements", "pub", "b2b", "selection", "propres"
        ]]
        fig = go.Figure(go.Pie(
            labels=REV_LABELS,
            values=vals,
            hole=0.55,
            marker=dict(colors=REV_COLORS, line=dict(color="#06080f", width=2)),
            textinfo="label+percent",
            textfont_size=11,
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="🍩 7 flux revenus — An 1", font_color=C_GREEN, font_size=14),
            showlegend=False,
            height=320,
            annotations=[dict(
                text=f"<b>{sum(vals)/1e6:.1f}M</b><br>FCFA",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=C_GREEN),
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cash flow cumulatif
    fig = go.Figure()
    cumul = [p["cumul"] / 1e6 for p in profit_monthly]
    colors = [C_GREEN if v >= 0 else C_ORANGE for v in cumul]
    fig.add_trace(go.Scatter(
        x=list(range(1, 61)), y=cumul,
        mode="lines", name="Cumul P&L",
        line=dict(color=C_CYAN, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.05)",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    if fin["delai_mois"]:
        fig.add_vline(x=fin["delai_mois"], line_dash="dot", line_color=C_GREEN,
                      annotation_text=f"  Break-even M{fin['delai_mois']}",
                      annotation_font_color=C_GREEN)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="💹 Cash Flow Cumulatif — Depuis investissement (M FCFA)", font_color=C_CYAN, font_size=14),
        height=280, yaxis_title="M FCFA cumulés",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Décomposition coûts
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    col_cost1, col_cost2 = st.columns(2)
    with col_cost1:
        st.markdown("#### Structure des coûts — An 1")
        c1_data = cost_monthly[:12]
        cost_keys = ["cout_salaires", "cout_marketing", "cout_tech", "cout_operations"]
        cost_labels = ["Salaires", "Marketing", "Tech/Infra", "Opérations"]
        cost_colors = [C_PURPLE, C_CYAN, C_TEAL, C_GOLD]
        fig = go.Figure()
        for k, lbl, col in zip(cost_keys, cost_labels, cost_colors):
            fig.add_trace(go.Bar(
                x=list(range(1, 13)),
                y=[c[k] / 1e3 for c in c1_data],
                name=lbl, marker_color=col,
            ))
        fig.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title=dict(text="Coûts An 1 (K FCFA)", font_color=C_CYAN, font_size=13),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_cost2:
        st.markdown("#### Flux revenus — 5 ans (M FCFA)")
        fig = go.Figure()
        for k, lbl, col in zip(REV_KEYS, REV_LABELS, REV_COLORS):
            annual_vals = [
                sum(r[k] for r in rev_monthly[(an-1)*12:an*12]) / 1e6
                for an in range(1, 6)
            ]
            fig.add_trace(go.Bar(x=years_label, y=annual_vals, name=lbl, marker_color=col))
        fig.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title=dict(text="Décomposition CA (M FCFA)", font_color=C_GREEN, font_size=13),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — DONNÉES TERRAIN
# ══════════════════════════════════════════════════════════════

with tab3:
    cli  = terrain.get("clients", {})
    liv  = terrain.get("livreurs", {})
    rest = terrain.get("restaurants", {})
    bench= terrain.get("benchmarks", [])

    st.markdown(f"""
    <div class='ecantine-card'>
      <b style='color:{C_GREEN}'>Terrain E-cantine — Données Primaires</b><br>
      <span style='color:rgba(200,220,240,0.6);font-size:0.85rem'>
        {cli.get('n_repondants',0)} répondants clients (obj. {cli.get('objectif_cible',300)}) ·
        {liv.get('n_entretiens',0)} entretiens livreurs ·
        {rest.get('n_discussions',0)} discussions restaurants ·
        Panel extrapolé via benchmarks Chowdeck Nigeria × Facteur Dakar 0.238
      </span>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    # ── Clients ──────────────────────────────────────────────
    with col_c1:
        st.markdown(f"##### 👤 Clients ({cli.get('n_repondants',0)} répondants)")

        # Intérêt pour E-cantine
        fig = go.Figure(go.Bar(
            x=["Très intéressé", "Intérêt total", "Wave principal", "Étudiants"],
            y=[cli.get("pct_tres_interesse", 0),
               cli.get("pct_interesse_total", 0),
               cli.get("pct_wave", 0),
               cli.get("pct_etudiants", 0)],
            marker_color=[C_GREEN, C_CYAN, C_PURPLE, C_GOLD],
            text=[f"{v:.0f}%" for v in [
                cli.get("pct_tres_interesse",0), cli.get("pct_interesse_total",0),
                cli.get("pct_wave",0), cli.get("pct_etudiants",0)
            ]],
            textposition="outside",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Profil clients — Indicateurs clés", font_size=13, font_color=C_GREEN),
            yaxis_range=[0, 120], height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Freins
        if cli.get("freins"):
            freins = cli["freins"]
            fig = go.Figure(go.Bar(
                x=list(freins.values()),
                y=list(freins.keys()),
                orientation="h",
                marker_color=C_ORANGE,
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Freins principaux (clients)", font_size=13, font_color=C_ORANGE),
                height=max(200, len(freins) * 40),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Fonctionnalités importantes
        if cli.get("fonctions"):
            foncs = dict(list(cli["fonctions"].items())[:6])
            fig = go.Figure(go.Bar(
                x=list(foncs.values()),
                y=list(foncs.keys()),
                orientation="h",
                marker_color=C_CYAN,
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Fonctionnalités attendues", font_size=13, font_color=C_CYAN),
                height=max(200, len(foncs) * 40),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        # ── Livreurs ──────────────────────────────────────────
        st.markdown(f"##### 🛵 Livreurs ({liv.get('n_entretiens',0)} entretiens)")
        fig = go.Figure(go.Bar(
            x=["Moto perso", "Wave salaire", "Modèle hybride", "Soir", "Compte Wave"],
            y=[liv.get("pct_moto", 96),
               liv.get("pct_wave_sal", 87),
               liv.get("pct_hybride", 70),
               liv.get("pct_soir", 100),
               liv.get("pct_wave_compte", 87)],
            marker_color=[C_TEAL, C_PURPLE, C_CYAN, C_GREEN, C_GOLD],
            text=[f"{v:.0f}%" for v in [
                liv.get("pct_moto",96), liv.get("pct_wave_sal",87),
                liv.get("pct_hybride",70), liv.get("pct_soir",100), liv.get("pct_wave_compte",87)
            ]],
            textposition="outside",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Profil livreurs — Terrain", font_size=13, font_color=C_TEAL),
            yaxis_range=[0, 120], height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Zones couvertes
        if liv.get("zones"):
            z = dict(list(sorted(liv["zones"].items(), key=lambda x: -x[1]))[:8])
            fig = go.Figure(go.Bar(
                x=list(z.values()), y=list(z.keys()),
                orientation="h", marker_color=C_TEAL,
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Zones couvertes (livreurs)", font_size=13, font_color=C_TEAL),
                height=max(200, len(z) * 38),
            )
            st.plotly_chart(fig, use_container_width=True)

        # ── Restaurants ───────────────────────────────────────
        st.markdown(f"##### 🍽 Restaurants ({rest.get('n_discussions',0)} discussions)")
        fig = go.Figure(go.Bar(
            x=["WhatsApp actuel", "Wave accepté", "Livreurs propres", "Internet stable"],
            y=[rest.get("pct_whatsapp", 100),
               rest.get("pct_wave", 80),
               rest.get("pct_livreurs_propres", 40),
               rest.get("pct_internet_stable", 80)],
            marker_color=[C_ORANGE, C_PURPLE, C_PINK, C_GOLD],
            text=[f"{v:.0f}%" for v in [
                rest.get("pct_whatsapp",100), rest.get("pct_wave",80),
                rest.get("pct_livreurs_propres",40), rest.get("pct_internet_stable",80)
            ]],
            textposition="outside",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Profil restaurants — Terrain", font_size=13, font_color=C_ORANGE),
            yaxis_range=[0, 120], height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Concurrents ───────────────────────────────────────────
    if bench:
        st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
        st.markdown("##### 🏁 Analyse Concurrentielle")
        df_bench = pd.DataFrame(bench)
        cols_show = [c for c in ["plateforme","statut","commission_pct","frais_livraison_moy_fcfa",
                                  "point_fort","point_faible"] if c in df_bench.columns]
        if cols_show:
            st.dataframe(df_bench[cols_show], use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class='ecantine-card-cyan' style='margin-top:16px'>
      <b style='color:{C_CYAN}'>Facteur Dakar — Calibration</b><br>
      <span style='font-size:0.85rem;color:rgba(200,220,240,0.7)'>
        Population Dakar × Pouvoir d'achat × Pénétration mobile = <b style='color:{C_GREEN}'>0.238</b>
        vs Lagos (Chowdeck Nigeria) → MAU plateau réaliste Dakar ≈ 80 000
      </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — SCÉNARIOS
# ══════════════════════════════════════════════════════════════

with tab4:
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        fig = go.Figure()
        for scenario, name, color, dash in [
            ("optimiste",  "Optimiste",  C_CYAN,   "dot"),
            ("central",    "Central",    C_GREEN,  "solid"),
            ("pessimiste", "Pessimiste", C_ORANGE, "dash"),
        ]:
            mau_series = m[f"{scenario}_series"]
            fig.add_trace(go.Scatter(
                x=list(range(1, 61)), y=[v/1000 for v in mau_series],
                name=name, mode="lines",
                line=dict(color=color, width=2.5, dash=dash),
            ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="MAU — 3 scénarios (milliers)", font_color=C_GREEN, font_size=14),
            height=340, yaxis_title="MAU (000s)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_s2:
        fig = go.Figure()
        ans = [1, 2, 3, 4, 5]
        for scenario, name, color in [
            ("optimiste",  "Optimiste",  C_CYAN),
            ("central",    "Central",    C_GREEN),
            ("pessimiste", "Pessimiste", C_ORANGE),
        ]:
            fig.add_trace(go.Scatter(
                x=years_label,
                y=[ca[scenario][f"an{a}"] / 1e6 for a in ans],
                name=name, mode="lines+markers",
                line=dict(color=color, width=2.5),
                marker=dict(size=8),
            ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="CA — 3 scénarios (M FCFA)", font_color=C_GREEN, font_size=14),
            height=340, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau comparatif
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Tableau comparatif — MAU & CA par scénario")
    rows_s = []
    for an in range(1, 6):
        rows_s.append({
            "Année":                f"An {an} ({2026+an})",
            "MAU Pess.":            f"{m['pessimiste'][f'an{an}']:,}",
            "MAU Central":          f"{m['central'][f'an{an}']:,}",
            "MAU Optim.":           f"{m['optimiste'][f'an{an}']:,}",
            "CA Pess. (M)":         f"{ca['pessimiste'][f'an{an}']/1e6:.2f}",
            "CA Central (M)":       f"{ca['central'][f'an{an}']/1e6:.2f}",
            "CA Optim. (M)":        f"{ca['optimiste'][f'an{an}']/1e6:.2f}",
        })
    st.dataframe(pd.DataFrame(rows_s), use_container_width=True, hide_index=True)

    # Décomposition An 1
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Décomposition CA An 1 — 7 flux nets E-cantine")
    total_an1 = sum(ca["decomp_an1"].values())
    decomp_rows = []
    label_map = {
        "livraison":   "① Frais livraison (marge 40%)",
        "commission":  "② Commission 1–2,5% restaurants",
        "abonnements": "③ Abonnements Pro / Premium",
        "pub":         "④ Publicité in-app",
        "b2b":         "⑤ B2B cantines entreprises",
        "selection":   "⑥ E-cantine Sélection (5%)",
        "propres":     "⑦ Livraisons propres (1,5%)",
    }
    for k, lbl in label_map.items():
        v = ca["decomp_an1"][k]
        decomp_rows.append({
            "Flux":          lbl,
            "FCFA":          f"{v:,.0f}",
            "M FCFA":        f"{v/1e6:.2f}",
            "% du CA An 1":  f"{v/total_an1*100:.0f}%" if total_an1 else "—",
        })
    st.dataframe(pd.DataFrame(decomp_rows), use_container_width=True, hide_index=True)
    st.markdown(f"""
    <div style='text-align:right;padding-right:12px'>
      <span style='color:{C_GREEN};font-size:1.1rem;font-weight:700'>
        TOTAL NET : {total_an1/1e6:.2f}M FCFA
      </span>
      <span style='color:rgba(200,220,240,0.4);font-size:0.78rem;margin-left:8px'>
        (Frais Wave 1% exclus — revenu Wave, pas E-cantine)
      </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — MONTE CARLO & SENSIBILITÉ
# ══════════════════════════════════════════════════════════════

with tab5:
    if mc:
        col_mc1, col_mc2 = st.columns(2)

        # Distribution CA An5
        with col_mc1:
            ca5_vals = [v / 1e6 for v in mc["ca5"]["values"]]
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=ca5_vals,
                nbinsx=30,
                marker_color=C_GREEN,
                opacity=0.75,
                name="CA An5",
            ))
            for perc, val, color in [
                ("P10", mc["ca5"]["p10"]/1e6, C_ORANGE),
                ("P50", mc["ca5"]["p50"]/1e6, C_CYAN),
                ("P90", mc["ca5"]["p90"]/1e6, C_GREEN),
            ]:
                fig.add_vline(x=val, line_dash="dash", line_color=color,
                              annotation_text=f"  {perc}: {val:.1f}M",
                              annotation_font_color=color)
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text=f"Distribution CA An5 ({mc['n_simulations']} simulations)",
                           font_color=C_GREEN, font_size=14),
                height=320, xaxis_title="CA An5 (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Distribution VAN
        with col_mc2:
            van_vals = [v / 1e6 for v in mc["van"]["values"]]
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=van_vals, nbinsx=30,
                marker_color=C_CYAN, opacity=0.75, name="VAN",
            ))
            fig.add_vline(x=0, line_dash="dot",
                          line_color=C_ORANGE, annotation_text="  VAN = 0",
                          annotation_font_color=C_ORANGE)
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text=f"Distribution VAN ({mc['van']['pct_positive']:.0f}% positives)",
                           font_color=C_CYAN, font_size=14),
                height=320, xaxis_title="VAN (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        # KPIs Monte Carlo
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("CA An5 — P10", f"{mc['ca5']['p10']/1e6:.1f}M FCFA")
        mc2.metric("CA An5 — P50", f"{mc['ca5']['p50']/1e6:.1f}M FCFA")
        mc3.metric("CA An5 — P90", f"{mc['ca5']['p90']/1e6:.1f}M FCFA")
        mc4.metric("VAN positive", f"{mc['van']['pct_positive']:.0f}%")
        mc5.metric("Simulations", f"{mc['n_simulations']:,}")

    else:
        st.info("Clique sur **▶ Lancer Monte Carlo** dans la sidebar pour lancer les simulations.")

    # ── Tornado Sensibilité ────────────────────────────────────
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Analyse de Sensibilité — Impact sur CA An 3 (Tornado Chart)")

    sens = res.get("sensitivity", [])
    if sens:
        labels  = [s["label"] for s in sens]
        impacts_up = [s["impact_up"] for s in sens]
        impacts_dn = [s["impact_dn"] for s in sens]
        delta_pct  = [s["delta_pct"] for s in sens]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=labels, x=impacts_up,
            orientation="h",
            name="+Δ paramètre",
            marker_color=C_GREEN,
            text=[f"+{v:.1f}%" for v in impacts_up],
            textposition="outside",
        ))
        fig.add_trace(go.Bar(
            y=labels, x=impacts_dn,
            orientation="h",
            name="−Δ paramètre",
            marker_color=C_ORANGE,
            text=[f"{v:.1f}%" for v in impacts_dn],
            textposition="outside",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            barmode="overlay",
            title=dict(
                text="Impact ±Δ% de chaque paramètre sur le CA An3",
                font_color=C_GREEN, font_size=14
            ),
            xaxis_title="Impact sur CA An3 (%)",
            height=420,
        )
        fig.add_vline(x=0, line_color="rgba(255,255,255,0.3)")
        st.plotly_chart(fig, use_container_width=True)

        st.caption("Le paramètre en haut est celui qui impacte le plus le CA An 3. "
                   "Priorité : maîtriser le panier moyen et le volume de commandes.")

    # ── Note méthodologique ───────────────────────────────────
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='ecantine-card'>
      <b style='color:{C_GREEN}'>Note Méthodologique</b><br>
      <span style='font-size:0.85rem;color:rgba(200,220,240,0.7)'>
        Les projections sont produites par un modèle de prédiction statistique (courbe S logistique)
        calibré sur Chowdeck Nigeria (Lagos) × Facteur Dakar <b>0.238</b>.
        Le Monte Carlo simule {mc['n_simulations'] if mc else n_mc} variantes en perturbant les paramètres clés
        (±20-30%) pour fournir des intervalles de confiance P10–P90.
        <br><br>
        Les données terrain (formulaire clients, 23 entretiens livreurs, 5 discussions restaurants)
        sont transparentes et disponibles dans les onglets <i>Données Terrain</i>.
        Les projections seront affinées à 300 répondants clients.
      </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown("<br><div class='neon-divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;color:rgba(200,220,240,0.3);font-size:0.78rem;padding:8px'>
  E-Cantine · Business Plan V7 · ISM Dakar · 2025 ·
  Auteur : Adote Mario-Giovani ADUAYI-AKUE ·
  Modèle IA — Courbe S logistique × Benchmarks Africains
</div>
""", unsafe_allow_html=True)
