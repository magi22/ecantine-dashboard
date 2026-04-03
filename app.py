"""
E-CANTINE · TABLEAU DE BORD IA · BUSINESS PLAN V7
Design : Blanc & Bleu Brand — Clean, Fluide, Moderne
"""

import base64, os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from predict import (
    run_model, run_monte_carlo,
    DEFAULT_PARAMS,
)

# ── Logos ────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

def _svg_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

LOGO_BLUE_B64 = _svg_b64(os.path.join(BASE, "assets", "logo_blue.svg"))
LOGO_ICON_B64 = _svg_b64(os.path.join(BASE, "assets", "logo_icon.svg"))

def logo_img(b64, width="140px", extra=""):
    if b64:
        return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{width};{extra}" />'
    return ""

# ── Page ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Cantine · Business Plan IA",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# PALETTE — THÈME BLANC PROPRE
# ══════════════════════════════════════════════════════════════
BRAND      = "#040c88"
BRAND_MED  = "#1a2fff"
BRAND_LT   = "#4d6aff"
CYAN       = "#00b4d8"
TEAL       = "#0096c7"
WHITE      = "#ffffff"
GREY_BG    = "#f5f7ff"   # fond page légèrement bleuté
CARD_BG    = "#ffffff"
BORDER     = "#dde3ff"
TEXT       = "#1a1f3c"
TEXT_DIM   = "#6b7280"
ORANGE     = "#f97316"
GREEN      = "#10b981"
PURPLE     = "#7c3aed"
GOLD       = "#f59e0b"
PINK       = "#ec4899"
TEAL2      = "#14b8a6"

REV_COLORS = [BRAND_MED, CYAN, PURPLE, GOLD, ORANGE, TEAL2, PINK]
REV_LABELS = ["① Livraison","② Commission","③ Abonnements","④ Pub","⑤ B2B","⑥ Sélection","⑦ Propres"]
REV_KEYS   = ["rev_livraison","rev_commission","rev_abonnements","rev_pub","rev_b2b","rev_selection","rev_propres"]
YEARS      = ["An 1","An 2","An 3","An 4","An 5"]
MONTHS     = list(range(1, 61))

# Template Plotly — fond blanc, sans font weight
PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(245,247,255,0.5)",
    font=dict(color=TEXT, family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=42, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11,
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1),
    xaxis=dict(gridcolor="#e8ecff", zerolinecolor="#e8ecff",
               tickfont=dict(color=TEXT_DIM, size=11)),
    yaxis=dict(gridcolor="#e8ecff", zerolinecolor="#e8ecff",
               tickfont=dict(color=TEXT_DIM, size=11)),
)

# ══════════════════════════════════════════════════════════════
# CSS — THÈME BLANC FLUIDE
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, .stApp, [data-testid="stAppViewContainer"],
.main, .block-container {{
  background-color: {GREY_BG} !important;
  font-family: 'Inter', sans-serif !important;
  color: {TEXT} !important;
}}
.block-container {{
  padding-top: 1.5rem !important;
  max-width: 1400px !important;
}}

/* ── Header barre ── */
[data-testid="stHeader"] {{
  background: rgba(255,255,255,0.95) !important;
  border-bottom: 1px solid {BORDER} !important;
  backdrop-filter: blur(12px);
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background: {WHITE} !important;
  border-right: 1px solid {BORDER} !important;
  box-shadow: 2px 0 20px rgba(4,12,136,0.06);
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] .stSlider label {{
  color: {BRAND} !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}}

/* ── Sliders ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
  background: {BRAND_MED} !important;
  border: 2px solid {WHITE} !important;
  box-shadow: 0 0 0 3px {BRAND_LT} !important;
}}

/* ── Métriques ── */
[data-testid="metric-container"] {{
  background: {WHITE} !important;
  border: 1px solid {BORDER} !important;
  border-top: 3px solid {BRAND_MED} !important;
  border-radius: 14px !important;
  padding: 18px 16px 14px !important;
  box-shadow: 0 2px 12px rgba(4,12,136,0.08) !important;
  transition: transform 0.2s, box-shadow 0.2s;
}}
[data-testid="metric-container"]:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(4,12,136,0.14) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
  color: {BRAND} !important;
  font-size: 1.6rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.5px !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
  color: {TEXT_DIM} !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
  font-weight: 600 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
  color: {GREEN} !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
}}

/* ── Onglets ── */
.stTabs [data-baseweb="tab-list"] {{
  background: {WHITE};
  border: 1px solid {BORDER};
  border-radius: 12px;
  padding: 4px 6px;
  gap: 2px;
  box-shadow: 0 2px 8px rgba(4,12,136,0.05);
}}
.stTabs [data-baseweb="tab"] {{
  color: {TEXT_DIM} !important;
  border-radius: 9px !important;
  padding: 8px 20px !important;
  font-size: 0.84rem !important;
  font-weight: 500 !important;
  transition: all 0.18s;
}}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
  background: {GREY_BG} !important;
  color: {BRAND} !important;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
  background: {BRAND} !important;
  color: {WHITE} !important;
  border-bottom: none !important;
  box-shadow: 0 2px 12px rgba(4,12,136,0.25) !important;
  font-weight: 600 !important;
}}
[data-testid="stTabsContent"],
[data-baseweb="tab-panel"] {{
  background: transparent !important;
}}

/* ── Boutons ── */
.stButton > button {{
  background: {BRAND} !important;
  border: none !important;
  color: {WHITE} !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: 0.84rem !important;
  padding: 10px 22px !important;
  box-shadow: 0 4px 14px rgba(4,12,136,0.3) !important;
  transition: all 0.2s !important;
  letter-spacing: 0.3px !important;
}}
.stButton > button:hover {{
  background: {BRAND_MED} !important;
  box-shadow: 0 6px 22px rgba(26,47,255,0.4) !important;
  transform: translateY(-2px) !important;
}}
.stButton > button:active {{
  transform: translateY(0) !important;
}}

/* ── Tableaux ── */
[data-testid="stDataFrame"] {{
  border: 1px solid {BORDER} !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 12px rgba(4,12,136,0.07) !important;
  background: {WHITE} !important;
}}
[data-testid="stDataFrame"] thead tr th {{
  background: {GREY_BG} !important;
  color: {BRAND} !important;
  font-size: 0.73rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.7px !important;
  font-weight: 700 !important;
}}
[data-testid="stDataFrame"] tbody tr:hover td {{
  background: #eef1ff !important;
}}

/* ── Divider ── */
.ec-divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, {BORDER}, {BRAND_LT}, {BORDER}, transparent);
  margin: 18px 0;
  opacity: 0.8;
}}

/* ── Cartes ── */
.ec-card {{
  background: {WHITE};
  border: 1px solid {BORDER};
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 2px 16px rgba(4,12,136,0.07);
  margin-bottom: 14px;
  transition: box-shadow 0.2s;
}}
.ec-card:hover {{
  box-shadow: 0 6px 28px rgba(4,12,136,0.13);
}}
.ec-card-accent {{
  background: linear-gradient(135deg, #f0f3ff 0%, {WHITE} 100%);
  border: 1px solid {BRAND_LT};
  border-left: 4px solid {BRAND_MED};
  border-radius: 14px;
  padding: 18px 22px;
  box-shadow: 0 2px 16px rgba(4,12,136,0.08);
  margin-bottom: 14px;
}}

/* ── Badges ── */
.badge-ok {{
  background: #eff6ff;
  color: {BRAND_MED};
  border: 1px solid #bfdbfe;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.76rem;
  font-weight: 700;
  display: inline-block;
  letter-spacing: 0.2px;
}}
.badge-success {{
  background: #f0fdf4;
  color: #065f46;
  border: 1px solid #a7f3d0;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.76rem;
  font-weight: 700;
  display: inline-block;
}}

/* ── Header principal ── */
.ec-header-bar {{
  background: {WHITE};
  border: 1px solid {BORDER};
  border-radius: 18px;
  padding: 22px 28px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 24px;
  box-shadow: 0 4px 24px rgba(4,12,136,0.09);
  border-left: 5px solid {BRAND_MED};
}}

/* ── Label section ── */
.ec-label {{
  color: {BRAND};
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin: 14px 0 8px;
  display: flex;
  align-items: center;
  gap: 7px;
}}
.ec-label::before {{
  content: '';
  display: inline-block;
  width: 3px; height: 14px;
  background: {BRAND_MED};
  border-radius: 2px;
}}

/* ── Stat chip ── */
.stat-chip {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: {GREY_BG};
  border: 1px solid {BORDER};
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.82rem;
  font-weight: 600;
  color: {BRAND};
  margin: 3px;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {GREY_BG}; }}
::-webkit-scrollbar-thumb {{ background: {BRAND_LT}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {BRAND_MED}; }}

/* ── Caption ── */
[data-testid="stCaptionContainer"] {{
  color: {TEXT_DIM} !important;
  font-size: 0.76rem !important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 8px 8px;text-align:center">
      {logo_img(LOGO_BLUE_B64, width="150px")}
    </div>
    <div style="text-align:center;margin-bottom:14px">
      <span style="font-size:0.68rem;color:{TEXT_DIM};letter-spacing:1.5px;
                   text-transform:uppercase;font-weight:600">Business Plan V7 · IA</span>
    </div>
    <div class="ec-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p class='ec-label'>Modèle Économique</p>", unsafe_allow_html=True)
    avg_basket  = st.slider("Panier moyen (FCFA)",       1500, 6000,   3000, 100)
    avg_cmd     = st.slider("Commandes / MAU / mois",    1.0,  5.0,    2.5,  0.1)
    frais_liv   = st.slider("Frais livraison moy (FCFA)",500,  2500,   1200, 50)
    marge_liv   = st.slider("Marge livraison (%)",       20,   65,     40,   1)

    st.markdown(f"<p class='ec-label'>Formules Restaurants</p>", unsafe_allow_html=True)
    pct_starter = st.slider("% Starter (gratuit)",       40,   80,     60,   5)
    pct_pro     = st.slider("% Pro (25K FCFA/mois)",     10,   50,     30,   5)
    pct_prem    = max(0, 100 - pct_starter - pct_pro)
    st.caption(f"% Premium (50K FCFA/mois) = {pct_prem}%")

    st.markdown(f"<p class='ec-label'>Croissance MAU</p>", unsafe_allow_html=True)
    mau_L = st.slider("MAU plateau",         40_000, 200_000, 80_000, 5_000)
    mau_k = st.slider("Vitesse croissance k", 0.05,   0.20,    0.10,   0.01)

    st.markdown(f"<p class='ec-label'>Monte Carlo</p>", unsafe_allow_html=True)
    n_mc       = st.slider("Simulations", 200, 2000, 500, 100)
    run_mc_btn = st.button("▶  Lancer Monte Carlo", use_container_width=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='text-align:center;font-size:0.7rem;color:{TEXT_DIM};line-height:1.8'>
      ISM Dakar · 2025<br>
      <b style='color:{BRAND}'>Adote Mario-Giovani ADUAYI-AKUE</b>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CALCUL MODÈLE
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

@st.cache_data(show_spinner="Calcul en cours…")
def get_model(pk):
    return run_model(params=dict(pk))

@st.cache_data(show_spinner="Monte Carlo…")
def get_mc(pk, n):
    return run_monte_carlo(n=n, params=dict(pk))

pk    = tuple(sorted(params.items()))
res   = get_model(pk)
m     = res["mau"]
ca    = res["ca_annuel"]
fin   = res["financiers"]
rev_m = res["monthly"]["revenues"]
cst_m = res["monthly"]["costs"]
pft_m = res["monthly"]["profit"]
terr  = res["terrain"]

if "mc" not in st.session_state or run_mc_btn:
    st.session_state["mc"] = get_mc(pk, n_mc)
mc = st.session_state.get("mc")

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
dr      = fin["delai_mois"]
tri_val = fin["tri"] or 0

st.markdown(f"""
<div class="ec-header-bar">
  <div style="flex-shrink:0">
    {logo_img(LOGO_BLUE_B64, width="160px")}
  </div>
  <div style="flex:1;padding-left:4px">
    <div style="font-size:0.68rem;color:{TEXT_DIM};letter-spacing:1.5px;
                text-transform:uppercase;font-weight:600;margin-bottom:3px">
      Tableau de Bord · Modèle IA · Dakar 2027–2031
    </div>
    <div style="font-size:1.4rem;font-weight:800;color:{BRAND};letter-spacing:-0.5px">
      Business Plan V7 — Prédictions Financières
    </div>
    <div style="margin-top:10px;display:flex;gap:7px;flex-wrap:wrap">
      <span class="badge-ok">VAN {fin['van_M']:.1f}M FCFA</span>
      <span class="badge-ok">TRI {tri_val:.0f}%</span>
      <span class="badge-ok">IP {fin['ip']:.1f}x</span>
      <span class="badge-success">Break-even M{dr}</span>
    </div>
  </div>
  <div style="text-align:right;padding-left:16px;border-left:1px solid {BORDER}">
    <div style="font-size:0.68rem;color:{TEXT_DIM};text-transform:uppercase;
                letter-spacing:1px;margin-bottom:2px">CA An 5 Central</div>
    <div style="font-size:2.2rem;font-weight:900;color:{BRAND_MED};letter-spacing:-1.5px;
                line-height:1">{ca['central']['an5']/1e6:.0f}M</div>
    <div style="font-size:0.75rem;color:{TEXT_DIM};font-weight:600">FCFA</div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("MAU An 1",  f"{m['central']['an1']:,}")
c2.metric("MAU An 3",  f"{m['central']['an3']:,}", delta="objectif")
c3.metric("CA An 1",   f"{ca['central']['an1']/1e6:.1f}M FCFA")
c4.metric("CA An 3",   f"{ca['central']['an3']/1e6:.1f}M FCFA",
          delta=f"+{(ca['central']['an3']/ca['central']['an1']-1)*100:.0f}%")
c5.metric("VAN 15%",   f"{fin['van_M']:.1f}M FCFA", delta="positif")

st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ONGLETS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Vue d'ensemble",
    "💰  Revenus & Coûts",
    "🌍  Données Terrain",
    "🔀  Scénarios",
    "🎲  Monte Carlo",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure()
        if mc and "monthly_bands" in mc:
            b = mc["monthly_bands"]
            fig.add_trace(go.Scatter(
                x=MONTHS + MONTHS[::-1],
                y=b["p90"] + b["p10"][::-1],
                fill="toself",
                fillcolor="rgba(26,47,255,0.07)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Intervalle MC", showlegend=True, hoverinfo="skip",
            ))
        for series, name, color, width, dash in [
            (m["optimiste_series"],  "Optimiste",  CYAN,      1.8, "dot"),
            (m["central_series"],    "Central",    BRAND_MED, 2.8, "solid"),
            (m["pessimiste_series"], "Pessimiste", ORANGE,    1.8, "dash"),
        ]:
            fig.add_trace(go.Scatter(
                x=MONTHS, y=series, name=name, mode="lines",
                line=dict(color=color, width=width, dash=dash),
            ))
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color="rgba(4,12,136,0.15)", line_width=1)
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Croissance MAU — 5 ans", font=dict(color=BRAND, size=14)),
            yaxis_title="Utilisateurs actifs", height=330,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig = go.Figure()
        for scenario, name, color, opacity in [
            ("optimiste",  "Optimiste",  CYAN,      0.7),
            ("central",    "Central",    BRAND_MED, 1.0),
            ("pessimiste", "Pessimiste", ORANGE,    0.7),
        ]:
            vals = [ca[scenario][f"an{a}"] / 1e6 for a in range(1, 6)]
            fig.add_trace(go.Bar(
                x=YEARS, y=vals, name=name,
                marker=dict(color=color, opacity=opacity,
                            line=dict(color=WHITE, width=1)),
            ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="CA Annuel — 3 scénarios (M FCFA)", font=dict(color=BRAND, size=14)),
            barmode="group", yaxis_title="Millions FCFA", height=330,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau récap
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Performance par année — Scénario Central</p>",
                unsafe_allow_html=True)
    rows = []
    for an in range(1, 6):
        rev_an  = sum(r["total_mensuel"] for r in rev_m[(an-1)*12:an*12])
        cout_an = sum(c["total_couts"]   for c in cst_m[(an-1)*12:an*12])
        mg = rev_an - cout_an
        rows.append({
            "Année":           f"An {an} · {2026+an}",
            "MAU fin d'année": f"{m['central'][f'an{an}']:,}",
            "CA (M FCFA)":     f"{rev_an/1e6:.2f}",
            "Coûts (M FCFA)":  f"{cout_an/1e6:.2f}",
            "Marge (M FCFA)":  f"{mg/1e6:.2f}",
            "Marge nette":     f"{mg/rev_an*100:.0f}%" if rev_an else "—",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    fi1, fi2, fi3, fi4 = st.columns(4)
    fi1.metric("VAN (5 ans, 15%)",     f"{fin['van_M']:.1f}M FCFA", delta="Positif")
    fi2.metric("TRI",                   f"{tri_val:.1f}%",            delta="> 9% bancaire")
    fi3.metric("Indice Profitabilité",  f"{fin['ip']:.2f}x",          delta="> 1")
    fi4.metric("Budget de lancement",  f"{fin['budget_fcfa']/1e6:.2f}M FCFA")

# ══════════════════════════════════════════════════════════════
# TAB 2 — REVENUS & COÛTS
# ══════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS, y=[c["total_couts"]/1e6 for c in cst_m],
            name="Coûts", mode="lines",
            line=dict(color=ORANGE, width=2),
            fill="tozeroy", fillcolor="rgba(249,115,22,0.07)",
        ))
        fig.add_trace(go.Scatter(
            x=MONTHS, y=[r["total_mensuel"]/1e6 for r in rev_m],
            name="Revenus", mode="lines",
            line=dict(color=BRAND_MED, width=2.8),
            fill="tozeroy", fillcolor="rgba(26,47,255,0.08)",
        ))
        if dr:
            fig.add_vline(x=dr, line_dash="dash", line_color=GREEN, line_width=2,
                          annotation_text=f"  Break-even M{dr}",
                          annotation_font=dict(color=GREEN, size=12))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Revenus vs Coûts mensuels (M FCFA)", font=dict(color=BRAND, size=14)),
            height=310, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        d    = ca["decomp_an1"]
        keys = ["livraison","commission","abonnements","pub","b2b","selection","propres"]
        vals = [d[k] for k in keys]
        total_donut = sum(vals)
        fig = go.Figure(go.Pie(
            labels=REV_LABELS, values=vals, hole=0.60,
            marker=dict(colors=REV_COLORS, line=dict(color=WHITE, width=2)),
            textinfo="percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} FCFA<br>%{percent}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="7 flux revenus — An 1", font=dict(color=BRAND, size=14)),
            showlegend=True, height=310,
            legend=dict(font_size=10, orientation="v", x=1.02, y=0.5,
                        bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=115, t=42, b=0),
            annotations=[dict(
                text=f"<b>{total_donut/1e6:.1f}M</b><br>FCFA",
                x=0.44, y=0.5, showarrow=False,
                font=dict(size=16, color=BRAND),
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cash flow cumulatif
    fig = go.Figure()
    cumul_vals = [p["cumul"]/1e6 for p in pft_m]
    fig.add_trace(go.Scatter(
        x=MONTHS, y=cumul_vals, mode="lines", name="Cumul P&L",
        line=dict(color=BRAND_MED, width=2.5),
        fill="tozeroy", fillcolor="rgba(26,47,255,0.07)",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color=TEXT_DIM, line_width=1)
    if dr:
        fig.add_vline(x=dr, line_dash="dash", line_color=GREEN, line_width=2,
                      annotation_text=f"  Break-even M{dr}",
                      annotation_font=dict(color=GREEN, size=12))
    fig.update_layout(
        **PLOTLY,
        title=dict(text="Cash Flow Cumulatif depuis investissement (M FCFA)",
                   font=dict(color=BRAND, size=14)),
        height=260, yaxis_title="M FCFA",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        c1d = cst_m[:12]
        ck  = ["cout_salaires","cout_marketing","cout_tech","cout_operations"]
        cl  = ["Salaires","Marketing","Tech/Infra","Opérations"]
        cc  = [BRAND_MED, CYAN, TEAL2, GOLD]
        fig = go.Figure()
        for k, lbl, col in zip(ck, cl, cc):
            fig.add_trace(go.Bar(
                x=list(range(1,13)), y=[c[k]/1e3 for c in c1d],
                name=lbl, marker=dict(color=col, line=dict(width=0)),
            ))
        fig.update_layout(
            **PLOTLY, barmode="stack",
            title=dict(text="Coûts An 1 (K FCFA)", font=dict(color=BRAND, size=13)),
            height=290,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        fig = go.Figure()
        for k, lbl, col in zip(REV_KEYS, REV_LABELS, REV_COLORS):
            annual = [sum(r[k] for r in rev_m[(an-1)*12:an*12])/1e6 for an in range(1,6)]
            fig.add_trace(go.Bar(x=YEARS, y=annual, name=lbl,
                                 marker=dict(color=col, line=dict(width=0))))
        fig.update_layout(
            **PLOTLY, barmode="stack",
            title=dict(text="Décomposition CA 5 ans (M FCFA)", font=dict(color=BRAND, size=13)),
            height=290,
        )
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — DONNÉES TERRAIN
# ══════════════════════════════════════════════════════════════
with tab3:
    cli  = terr.get("clients",     {})
    liv  = terr.get("livreurs",    {})
    rest = terr.get("restaurants", {})
    bench= terr.get("benchmarks",  [])
    n_rep = cli.get("n_repondants", 0)
    n_obj = cli.get("objectif_cible", 300)
    pct_prog = min(n_rep / n_obj * 100, 100)

    st.markdown(f"""
    <div class="ec-card-accent">
      <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap">
        <div style="flex:1;min-width:200px">
          <div style="font-size:0.7rem;color:{TEXT_DIM};text-transform:uppercase;
                      letter-spacing:1px;font-weight:600">Collecte de données primaires</div>
          <div style="font-size:1.1rem;font-weight:700;color:{BRAND};margin-top:4px">
            {n_rep} clients · {liv.get('n_entretiens',0)} livreurs · {rest.get('n_discussions',0)} restaurants
          </div>
          <div style="font-size:0.82rem;color:{TEXT_DIM};margin-top:3px">
            Extrapolé via benchmarks Chowdeck Nigeria × Facteur Dakar <b style="color:{BRAND_MED}">0.238</b>
          </div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          <div style="font-size:0.7rem;color:{TEXT_DIM};margin-bottom:4px">Objectif clients</div>
          <div style="font-size:1.5rem;font-weight:800;color:{BRAND}">{n_rep}
            <span style="font-size:0.9rem;color:{TEXT_DIM}">/ {n_obj}</span>
          </div>
          <div style="background:#e0e7ff;border-radius:4px;height:6px;width:130px;margin-top:6px">
            <div style="background:{BRAND_MED};border-radius:4px;height:6px;
                        width:{pct_prog:.0f}%"></div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("<p class='ec-label'>Clients — indicateurs clés</p>",
                    unsafe_allow_html=True)
        fig = go.Figure()
        labels_c = ["Très intéressés","Intérêt total","Wave paiement","Étudiants"]
        vals_c   = [cli.get("pct_tres_interesse",75), cli.get("pct_interesse_total",100),
                    cli.get("pct_wave",100),           cli.get("pct_etudiants",70)]
        colors_c = [BRAND_MED, CYAN, PURPLE, TEAL2]
        fig.add_trace(go.Bar(
            x=vals_c, y=labels_c, orientation="h",
            marker=dict(color=colors_c, line=dict(width=0)),
            text=[f"{v:.0f}%" for v in vals_c],
            textposition="outside",
            textfont=dict(color=TEXT, size=12),
        ))
        fig.update_layout(
            **PLOTLY,
            xaxis_range=[0, 125], height=220, showlegend=False,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        if cli.get("freins"):
            fr = dict(list(cli["freins"].items())[:5])
            fig = go.Figure(go.Bar(
                x=list(fr.values()), y=list(fr.keys()), orientation="h",
                marker=dict(color=ORANGE, opacity=0.85, line=dict(width=0)),
                text=list(fr.values()), textposition="outside",
                textfont=dict(color=TEXT),
            ))
            fig.update_layout(
                **PLOTLY,
                title=dict(text="Freins principaux", font=dict(color=BRAND, size=13)),
                height=max(180, len(fr)*48), showlegend=False,
                margin=dict(l=10, r=50, t=42, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_t2:
        st.markdown("<p class='ec-label'>Livreurs — terrain</p>",
                    unsafe_allow_html=True)
        llabels = ["Moto personnelle","Wave salaire","Modèle hybride","Soir","Compte Wave"]
        lvals   = [liv.get("pct_moto",96), liv.get("pct_wave_sal",87),
                   liv.get("pct_hybride",70), liv.get("pct_soir",100), liv.get("pct_wave_compte",87)]
        lcolors = [TEAL2, BRAND_MED, CYAN, GOLD, PURPLE]
        fig = go.Figure(go.Bar(
            x=lvals, y=llabels, orientation="h",
            marker=dict(color=lcolors, line=dict(width=0)),
            text=[f"{v:.0f}%" for v in lvals], textposition="outside",
            textfont=dict(color=TEXT, size=12),
        ))
        fig.update_layout(
            **PLOTLY,
            xaxis_range=[0, 125], height=220, showlegend=False,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<p class='ec-label'>Restaurants — terrain</p>",
                    unsafe_allow_html=True)
        rlabels = ["Via WhatsApp","Acceptent Wave","Livreurs propres","Internet stable"]
        rvals   = [rest.get("pct_whatsapp",100), rest.get("pct_wave",80),
                   rest.get("pct_livreurs_propres",40), rest.get("pct_internet_stable",80)]
        fig = go.Figure(go.Bar(
            x=rvals, y=rlabels, orientation="h",
            marker=dict(color=[BRAND_MED, PURPLE, ORANGE, GOLD], line=dict(width=0)),
            text=[f"{v:.0f}%" for v in rvals], textposition="outside",
            textfont=dict(color=TEXT, size=12),
        ))
        fig.update_layout(
            **PLOTLY,
            xaxis_range=[0, 125], height=200, showlegend=False,
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    if bench:
        st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
        st.markdown("<p class='ec-label'>Concurrents — Marché Dakar</p>",
                    unsafe_allow_html=True)
        df_b = pd.DataFrame(bench)
        cols = [c for c in ["plateforme","statut","commission_pct",
                             "frais_livraison_moy_fcfa","point_fort","point_faible"]
                if c in df_b.columns]
        if cols:
            st.dataframe(df_b[cols], use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — SCÉNARIOS
# ══════════════════════════════════════════════════════════════
with tab4:
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        fig = go.Figure()
        for sc, nm, col, dsh in [
            ("optimiste","Optimiste",CYAN,"dot"),
            ("central","Central",BRAND_MED,"solid"),
            ("pessimiste","Pessimiste",ORANGE,"dash"),
        ]:
            fig.add_trace(go.Scatter(
                x=MONTHS, y=[v/1000 for v in m[f"{sc}_series"]],
                name=nm, mode="lines",
                line=dict(color=col, width=2.5 if sc=="central" else 1.8, dash=dsh),
            ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="MAU — 3 scénarios (milliers)", font=dict(color=BRAND, size=14)),
            height=330, yaxis_title="MAU (000s)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_s2:
        fig = go.Figure()
        for sc, nm, col in [("optimiste","Optimiste",CYAN),
                             ("central","Central",BRAND_MED),
                             ("pessimiste","Pessimiste",ORANGE)]:
            fig.add_trace(go.Scatter(
                x=YEARS,
                y=[ca[sc][f"an{a}"]/1e6 for a in range(1,6)],
                name=nm, mode="lines+markers",
                line=dict(color=col, width=2.5 if sc=="central" else 1.8),
                marker=dict(size=7),
            ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="CA annuel — 3 scénarios (M FCFA)", font=dict(color=BRAND, size=14)),
            height=330, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    rows_s = []
    for an in range(1, 6):
        rows_s.append({
            "Année":          f"An {an} · {2026+an}",
            "MAU Pess.":      f"{m['pessimiste'][f'an{an}']:,}",
            "MAU Central":    f"{m['central'][f'an{an}']:,}",
            "MAU Optim.":     f"{m['optimiste'][f'an{an}']:,}",
            "CA Pess. (M)":   f"{ca['pessimiste'][f'an{an}']/1e6:.2f}",
            "CA Central (M)": f"{ca['central'][f'an{an}']/1e6:.2f}",
            "CA Optim. (M)":  f"{ca['optimiste'][f'an{an}']/1e6:.2f}",
        })
    st.dataframe(pd.DataFrame(rows_s), use_container_width=True, hide_index=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Décomposition CA An 1 — 7 flux nets E-cantine</p>",
                unsafe_allow_html=True)
    total_an1 = sum(ca["decomp_an1"].values())
    lmap = {"livraison":"① Frais livraison (40%)",
            "commission":"② Commission 1–2,5%",
            "abonnements":"③ Abonnements",
            "pub":"④ Publicité in-app",
            "b2b":"⑤ B2B entreprises",
            "selection":"⑥ Sélection (5%)",
            "propres":"⑦ Livr. propres (1,5%)"}
    drows = []
    for k, lbl in lmap.items():
        v = ca["decomp_an1"][k]
        drows.append({"Flux": lbl,
                      "FCFA": f"{v:,.0f}",
                      "M FCFA": f"{v/1e6:.3f}",
                      "Part": f"{v/total_an1*100:.0f}%"})
    st.dataframe(pd.DataFrame(drows), use_container_width=True, hide_index=True)
    st.markdown(f"""
    <div style="text-align:right;padding:10px 14px;background:#eff6ff;
                border-radius:10px;margin-top:6px;border:1px solid #bfdbfe">
      <span style="color:{TEXT_DIM};font-size:0.82rem">TOTAL NET An 1 : </span>
      <span style="color:{BRAND};font-size:1.2rem;font-weight:800">{total_an1/1e6:.2f}M FCFA</span>
      <span style="color:{TEXT_DIM};font-size:0.74rem;margin-left:8px">
        (Frais Wave 1% exclus — revenu Wave, pas E-cantine)
      </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — MONTE CARLO & SENSIBILITÉ
# ══════════════════════════════════════════════════════════════
with tab5:
    if mc:
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=[v/1e6 for v in mc["ca5"]["values"]],
                nbinsx=35, name="CA An5",
                marker=dict(color=BRAND_MED, opacity=0.75,
                            line=dict(color=WHITE, width=0.5)),
            ))
            for perc, val, col in [
                ("P10", mc["ca5"]["p10"]/1e6, ORANGE),
                ("P50", mc["ca5"]["p50"]/1e6, BRAND),
                ("P90", mc["ca5"]["p90"]/1e6, GREEN),
            ]:
                fig.add_vline(x=val, line_dash="dash", line_color=col, line_width=2,
                              annotation_text=f"  {perc}: {val:.0f}M",
                              annotation_font=dict(color=col, size=11))
            fig.update_layout(
                **PLOTLY,
                title=dict(text=f"Distribution CA An5 — {mc['n_simulations']} simulations",
                           font=dict(color=BRAND, size=14)),
                height=310, xaxis_title="CA An5 (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_m2:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=[v/1e6 for v in mc["van"]["values"]],
                nbinsx=35, name="VAN",
                marker=dict(color=CYAN, opacity=0.75,
                            line=dict(color=WHITE, width=0.5)),
            ))
            fig.add_vline(x=0, line_dash="dot", line_color=ORANGE, line_width=2,
                          annotation_text="  Seuil 0",
                          annotation_font=dict(color=ORANGE, size=11))
            fig.update_layout(
                **PLOTLY,
                title=dict(text=f"Distribution VAN — {mc['van']['pct_positive']:.0f}% positives",
                           font=dict(color=BRAND, size=14)),
                height=310, xaxis_title="VAN (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("CA An5 · P10", f"{mc['ca5']['p10']/1e6:.0f}M FCFA")
        mc2.metric("CA An5 · P50", f"{mc['ca5']['p50']/1e6:.0f}M FCFA")
        mc3.metric("CA An5 · P90", f"{mc['ca5']['p90']/1e6:.0f}M FCFA")
        mc4.metric("VAN positive",  f"{mc['van']['pct_positive']:.0f}%",
                   delta="robuste" if mc["van"]["pct_positive"] > 80 else "")
        mc5.metric("Simulations",   f"{mc['n_simulations']:,}")

    else:
        st.markdown(f"""
        <div class="ec-card" style="text-align:center;padding:40px 20px">
          <div style="font-size:2.5rem;margin-bottom:10px">🎲</div>
          <div style="font-size:1rem;font-weight:700;color:{BRAND}">
            Monte Carlo non lancé</div>
          <div style="color:{TEXT_DIM};font-size:0.85rem;margin-top:6px">
            Clique sur <b>▶ Lancer Monte Carlo</b> dans la sidebar
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Tornado
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Analyse de Sensibilité — Impact sur CA An 3</p>",
                unsafe_allow_html=True)
    sens = res.get("sensitivity", [])
    if sens:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[s["label"] for s in sens],
            x=[s["impact_up"] for s in sens],
            orientation="h", name="+Δ",
            marker=dict(color=GREEN, opacity=0.85, line=dict(width=0)),
            text=[f"+{s['impact_up']:.1f}%" for s in sens],
            textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        fig.add_trace(go.Bar(
            y=[s["label"] for s in sens],
            x=[s["impact_dn"] for s in sens],
            orientation="h", name="-Δ",
            marker=dict(color=ORANGE, opacity=0.85, line=dict(width=0)),
            text=[f"{s['impact_dn']:.1f}%" for s in sens],
            textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        fig.add_vline(x=0, line_color=TEXT_DIM, line_width=1)
        fig.update_layout(
            **PLOTLY,
            barmode="overlay",
            title=dict(text="Tornado — Impact ±Δ% sur CA An3",
                       font=dict(color=BRAND, size=14)),
            xaxis_title="Impact (%)", height=400,
            legend=dict(orientation="h", y=1.12),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Paramètre en tête = levier le plus fort sur le CA An3.")

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ec-card">
      <div style="display:flex;gap:14px;align-items:flex-start">
        <div style="font-size:1.6rem">🔬</div>
        <div>
          <div style="font-size:0.75rem;font-weight:700;color:{BRAND};
                      text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px">
            Note Méthodologique</div>
          <div style="font-size:0.83rem;color:{TEXT_DIM};line-height:1.7">
            Modèle de prédiction statistique <b style="color:{TEXT}">courbe S logistique</b>
            calibré sur <b style="color:{TEXT}">Chowdeck Nigeria (Lagos)</b>
            × Facteur Dakar <b style="color:{BRAND_MED}">0.238</b>
            (population × pouvoir d'achat × pénétration mobile).<br>
            Le Monte Carlo simule <b style="color:{TEXT}">{mc['n_simulations'] if mc else n_mc} variantes</b>
            avec perturbation aléatoire ±20–30% des paramètres clés → intervalles P10–P90.<br>
            <span style="color:{ORANGE}">Panel terrain limité</span> —
            projections affinées à <b style="color:{TEXT}">300 répondants clients</b>.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            flex-wrap:wrap;gap:10px;padding:6px 4px">
  <div>{logo_img(LOGO_BLUE_B64, width="100px", extra="opacity:0.7;")}</div>
  <div style="color:{TEXT_DIM};font-size:0.73rem;text-align:center">
    Business Plan V7 · ISM Dakar · 2025 ·
    <b style="color:{BRAND}">Adote Mario-Giovani ADUAYI-AKUE</b>
  </div>
  <div style="font-size:0.7rem;color:{TEXT_DIM}">Modèle IA · Courbe S × Benchmarks Africains</div>
</div>
""", unsafe_allow_html=True)
