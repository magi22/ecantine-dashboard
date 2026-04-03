"""
╔══════════════════════════════════════════════════════════════╗
║   E-CANTINE · TABLEAU DE BORD IA · BUSINESS PLAN V7         ║
║   Design : Brand #040c88 — Futuriste & Clean                ║
╚══════════════════════════════════════════════════════════════╝
"""

import base64, os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from predict import (
    run_model, run_monte_carlo, sensitivity_analysis,
    compute_mau_series, compute_revenues, compute_costs,
    DEFAULT_PARAMS,
)

# ══════════════════════════════════════════════════════════════
# HELPERS — LOGOS SVG
# ══════════════════════════════════════════════════════════════

BASE = os.path.dirname(os.path.abspath(__file__))

def _svg_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

LOGO_ICON_B64  = _svg_b64(os.path.join(BASE, "assets", "logo_icon.svg"))
LOGO_WHITE_B64 = _svg_b64(os.path.join(BASE, "assets", "logo_blue.svg"))

def logo_img(b64, width="100%", extra=""):
    if b64:
        return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{width};{extra}" />'
    return ""

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="E-Cantine · Business Plan IA",
    page_icon="data:image/svg+xml;base64," + LOGO_ICON_B64 if LOGO_ICON_B64 else "🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# PALETTE BRAND
# ══════════════════════════════════════════════════════════════

BRAND      = "#040c88"   # Bleu E-cantine
BRAND_MED  = "#1a2fff"   # Bleu vif
BRAND_LT   = "#4d6aff"   # Bleu clair
CYAN       = "#00c8ff"   # Cyan accent
CYAN_DK    = "#0099cc"   # Cyan foncé
WHITE      = "#ffffff"
TEXT       = "#e8eeff"   # Texte principal
TEXT_DIM   = "#8899cc"   # Texte secondaire
BG_DEEP    = "#03061a"   # Fond très sombre
BG_CARD    = "#070e30"   # Fond carte
BG_CARD2   = "#0a1240"   # Fond carte accent
BORDER     = "rgba(4,12,136,0.5)"
BORDER_LT  = "rgba(77,106,255,0.35)"
ORANGE     = "#ff6b35"
GOLD       = "#ffd060"
TEAL       = "#00e5cc"
PURPLE     = "#7c6aff"

# Couleurs des 7 flux
REV_COLORS = [BRAND_MED, CYAN, PURPLE, GOLD, ORANGE, TEAL, "#ff80ab"]
REV_LABELS = ["① Livraison","② Commission","③ Abonnements","④ Pub","⑤ B2B","⑥ Sélection","⑦ Propres"]
REV_KEYS   = ["rev_livraison","rev_commission","rev_abonnements","rev_pub","rev_b2b","rev_selection","rev_propres"]

# Template Plotly brand
PLOTLY = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(7,14,48,0.4)",
    font=dict(color=TEXT, family="Inter, 'Segoe UI', sans-serif", size=12),
    margin=dict(l=8, r=8, t=40, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11, orientation="h",
                yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="rgba(77,106,255,0.1)", zerolinecolor="rgba(77,106,255,0.2)",
               tickfont_color=TEXT_DIM),
    yaxis=dict(gridcolor="rgba(77,106,255,0.1)", zerolinecolor="rgba(77,106,255,0.2)",
               tickfont_color=TEXT_DIM),
)

# ══════════════════════════════════════════════════════════════
# CSS GLOBAL — BRAND DESIGN
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   ANIMATIONS KEYFRAMES
══════════════════════════════════════════ */
@keyframes fadeInUp {{
  from {{ opacity:0; transform:translateY(18px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes fadeInLeft {{
  from {{ opacity:0; transform:translateX(-16px); }}
  to   {{ opacity:1; transform:translateX(0); }}
}}
@keyframes pulseGlow {{
  0%,100% {{ box-shadow: 0 0 12px rgba(0,200,255,0.2), 0 4px 24px rgba(4,12,136,0.3); }}
  50%      {{ box-shadow: 0 0 28px rgba(0,200,255,0.45), 0 6px 32px rgba(26,47,255,0.4); }}
}}
@keyframes borderScan {{
  0%   {{ background-position: 0% 50%; }}
  100% {{ background-position: 200% 50%; }}
}}
@keyframes shimmer {{
  0%   {{ background-position: -400px 0; }}
  100% {{ background-position: 400px 0; }}
}}
@keyframes rotateDot {{
  from {{ transform: rotate(0deg) translateX(22px) rotate(0deg); }}
  to   {{ transform: rotate(360deg) translateX(22px) rotate(-360deg); }}
}}
@keyframes countUp {{
  from {{ opacity:0; transform:scale(0.85); }}
  to   {{ opacity:1; transform:scale(1); }}
}}
@keyframes gradientShift {{
  0%   {{ background-position: 0% 50%; }}
  50%  {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}
@keyframes neonPulse {{
  0%,100% {{ opacity:0.5; }}
  50%      {{ opacity:1; }}
}}

/* ══════════════════════════════════════════
   BASE
══════════════════════════════════════════ */
.stApp, [data-testid="stAppViewContainer"] {{
  background:
    radial-gradient(ellipse at 15% 0%,   rgba(4,12,136,0.22) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 100%, rgba(0,200,255,0.09) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%,  rgba(26,47,255,0.04) 0%, transparent 70%),
    linear-gradient(180deg, {BG_DEEP} 0%, #030718 100%);
  font-family: 'Inter', 'Space Grotesk', sans-serif;
  color: {TEXT};
  animation: fadeInUp 0.5s ease both;
}}

[data-testid="stHeader"] {{
  background: rgba(3,6,26,0.97) !important;
  border-bottom: 1px solid rgba(26,47,255,0.3) !important;
  backdrop-filter: blur(16px) saturate(180%);
}}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #020514 0%, #040c26 100%) !important;
  border-right: 1px solid rgba(4,12,136,0.6) !important;
  animation: fadeInLeft 0.4s ease both;
}}
[data-testid="stSidebar"]::after {{
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 1px; height: 100%;
  background: linear-gradient(180deg, transparent, {CYAN}, transparent);
  opacity: 0.2;
  animation: neonPulse 3s ease-in-out infinite;
}}
[data-testid="stSidebar"] .stSlider label {{
  color: {CYAN} !important;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.4px;
  text-transform: uppercase;
}}
[data-testid="stSidebar"] p  {{ color: {TEXT_DIM} !important; font-size: 0.82rem; }}

/* ─── Sliders ─── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
  background: radial-gradient(circle, {CYAN}, {BRAND_MED}) !important;
  border: 2px solid {CYAN} !important;
  width: 18px !important; height: 18px !important;
  box-shadow: 0 0 12px rgba(0,200,255,0.7), 0 0 4px rgba(0,200,255,0.4);
  transition: box-shadow 0.2s, transform 0.2s;
}}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]:hover {{
  box-shadow: 0 0 20px rgba(0,200,255,0.9) !important;
  transform: scale(1.15) !important;
}}
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {{
  background: linear-gradient(90deg, {BRAND}, {BRAND_MED}) !important;
  border-radius: 4px;
}}

/* ══════════════════════════════════════════
   MÉTRIQUES — CARTES KPI
══════════════════════════════════════════ */
[data-testid="metric-container"] {{
  background: linear-gradient(145deg, rgba(10,20,70,0.85) 0%, rgba(4,8,32,0.95) 100%);
  border: 1px solid rgba(77,106,255,0.3);
  border-top: 2px solid {BRAND_MED};
  border-radius: 16px;
  padding: 20px 18px 16px;
  backdrop-filter: blur(12px) saturate(150%);
  animation: pulseGlow 4s ease-in-out infinite, fadeInUp 0.5s ease both;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s ease;
}}
[data-testid="metric-container"]::before {{
  content: '';
  position: absolute;
  top: 0; left: -60%;
  width: 40%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,200,255,0.06), transparent);
  animation: shimmer 3.5s ease-in-out infinite;
}}
[data-testid="metric-container"]:hover {{
  transform: translateY(-4px) scale(1.01);
  border-top-color: {CYAN} !important;
  box-shadow: 0 12px 40px rgba(4,12,136,0.5), 0 0 20px rgba(0,200,255,0.15);
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
  color: {WHITE} !important;
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: 1.65rem !important;
  font-weight: 700;
  letter-spacing: -0.8px;
  animation: countUp 0.6s cubic-bezier(.34,1.56,.64,1) both;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
  color: rgba(160,180,220,0.75) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  font-weight: 600;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
  color: {CYAN} !important;
  font-size: 0.78rem !important;
  font-weight: 600;
}}

/* ══════════════════════════════════════════
   ONGLETS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
  background: rgba(4,12,136,0.1);
  border: 1px solid rgba(26,47,255,0.25);
  border-radius: 14px;
  padding: 5px 7px;
  gap: 3px;
  backdrop-filter: blur(8px);
}}
.stTabs [data-baseweb="tab"] {{
  color: rgba(160,180,220,0.55) !important;
  border-radius: 10px !important;
  padding: 9px 22px !important;
  font-size: 0.84rem;
  font-weight: 500;
  letter-spacing: 0.2px;
  transition: all 0.22s cubic-bezier(.34,1.56,.64,1);
  position: relative;
}}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
  background: rgba(77,106,255,0.12) !important;
  color: {TEXT} !important;
  transform: translateY(-1px);
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
  background: linear-gradient(135deg, rgba(4,12,136,0.75), rgba(26,47,255,0.55)) !important;
  color: {WHITE} !important;
  border-bottom: 2px solid {CYAN} !important;
  box-shadow: 0 3px 16px rgba(4,12,136,0.6), 0 0 12px rgba(0,200,255,0.12);
  font-weight: 600;
}}

/* ══════════════════════════════════════════
   BOUTONS — FUTURISTES
══════════════════════════════════════════ */
.stButton > button {{
  background: linear-gradient(135deg, {BRAND} 0%, {BRAND_MED} 60%, #2840ff 100%) !important;
  background-size: 200% 200% !important;
  border: 1px solid rgba(77,106,255,0.5) !important;
  color: {WHITE} !important;
  border-radius: 10px !important;
  font-family: 'Space Grotesk', 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  padding: 11px 22px !important;
  box-shadow: 0 4px 18px rgba(4,12,136,0.55), inset 0 1px 0 rgba(255,255,255,0.1);
  transition: all 0.25s cubic-bezier(.34,1.56,.64,1) !important;
  position: relative !important;
  overflow: hidden !important;
}}
.stButton > button::before {{
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,200,255,0.18), transparent);
  transition: left 0.4s ease;
}}
.stButton > button:hover::before {{
  left: 150%;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, {BRAND_MED} 0%, {CYAN} 100%) !important;
  border-color: {CYAN} !important;
  box-shadow: 0 6px 28px rgba(0,200,255,0.4), 0 0 16px rgba(0,200,255,0.2) !important;
  transform: translateY(-2px) scale(1.02) !important;
}}
.stButton > button:active {{
  transform: translateY(0) scale(0.98) !important;
}}

/* ══════════════════════════════════════════
   TABLEAUX
══════════════════════════════════════════ */
[data-testid="stDataFrame"] {{
  border: 1px solid rgba(26,47,255,0.3) !important;
  border-radius: 14px !important;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(4,12,136,0.2);
  animation: fadeInUp 0.5s ease both;
}}
[data-testid="stDataFrame"] thead tr th {{
  background: rgba(4,12,136,0.45) !important;
  color: {CYAN} !important;
  font-size: 0.73rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.8px !important;
  font-weight: 700 !important;
  border-bottom: 1px solid rgba(0,200,255,0.2) !important;
}}
[data-testid="stDataFrame"] tbody tr {{
  transition: background 0.15s ease;
}}
[data-testid="stDataFrame"] tbody tr:hover td {{
  background: rgba(26,47,255,0.1) !important;
}}

/* ══════════════════════════════════════════
   DIVIDER ANIMÉ
══════════════════════════════════════════ */
.brand-divider {{
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(26,47,255,0.5) 30%,
    {CYAN} 50%,
    rgba(26,47,255,0.5) 70%,
    transparent 100%);
  background-size: 200% 100%;
  margin: 16px 0;
  animation: borderScan 4s linear infinite;
}}

/* ══════════════════════════════════════════
   CARTES
══════════════════════════════════════════ */
.ec-card {{
  background: linear-gradient(145deg, rgba(6,14,50,0.9) 0%, rgba(3,7,26,0.97) 100%);
  border: 1px solid rgba(77,106,255,0.28);
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 4px 24px rgba(4,12,136,0.22), inset 0 1px 0 rgba(77,106,255,0.12);
  margin-bottom: 14px;
  backdrop-filter: blur(10px);
  animation: fadeInUp 0.5s ease both;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}}
.ec-card:hover {{
  border-color: rgba(0,200,255,0.3);
  box-shadow: 0 6px 32px rgba(4,12,136,0.35), 0 0 20px rgba(0,200,255,0.07);
}}
.ec-card-cyan {{
  background: linear-gradient(145deg, rgba(0,40,80,0.25) 0%, rgba(3,7,26,0.97) 100%);
  border: 1px solid rgba(0,200,255,0.25);
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 4px 24px rgba(0,200,255,0.08);
  margin-bottom: 14px;
  backdrop-filter: blur(10px);
}}

/* ══════════════════════════════════════════
   BADGES
══════════════════════════════════════════ */
.badge-ok {{
  background: linear-gradient(90deg, rgba(0,200,255,0.12), rgba(26,47,255,0.18));
  color: {CYAN};
  border: 1px solid rgba(0,200,255,0.45);
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.4px;
  display: inline-block;
  animation: fadeInUp 0.5s ease both;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}}
.badge-ok:hover {{
  background: rgba(0,200,255,0.2);
  box-shadow: 0 0 12px rgba(0,200,255,0.35);
}}
.badge-warn {{
  background: rgba(255,107,53,0.12);
  color: {ORANGE};
  border: 1px solid rgba(255,107,53,0.4);
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 0.76rem;
  font-weight: 700;
  display: inline-block;
}}

/* ══════════════════════════════════════════
   HEADER PRINCIPAL
══════════════════════════════════════════ */
.ec-header-bar {{
  background: linear-gradient(120deg,
    rgba(4,12,136,0.4) 0%,
    rgba(10,20,70,0.6) 50%,
    rgba(0,50,80,0.2) 100%);
  border: 1px solid rgba(77,106,255,0.35);
  border-radius: 18px;
  padding: 22px 30px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 26px;
  box-shadow: 0 6px 40px rgba(4,12,136,0.35),
              inset 0 1px 0 rgba(77,106,255,0.2),
              inset 0 -1px 0 rgba(0,0,0,0.3);
  backdrop-filter: blur(14px) saturate(160%);
  animation: fadeInUp 0.45s ease both;
  position: relative;
  overflow: hidden;
}}
.ec-header-bar::after {{
  content: '';
  position: absolute;
  top: -1px; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,200,255,0.5), transparent);
  animation: neonPulse 2.5s ease-in-out infinite;
}}

/* ══════════════════════════════════════════
   SECTION LABELS
══════════════════════════════════════════ */
.ec-label {{
  color: {BRAND_LT};
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin: 14px 0 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.ec-label::before {{
  content: '';
  display: inline-block;
  width: 3px;
  height: 14px;
  background: linear-gradient(180deg, {CYAN}, {BRAND_MED});
  border-radius: 2px;
  flex-shrink: 0;
}}

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {BG_DEEP}; }}
::-webkit-scrollbar-thumb {{
  background: linear-gradient(180deg, {BRAND_MED}, {BRAND});
  border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {CYAN}; }}

/* ══════════════════════════════════════════
   CAPTION & DIVERS
══════════════════════════════════════════ */
[data-testid="stCaptionContainer"] {{
  color: rgba(120,145,190,0.7) !important;
  font-size: 0.76rem;
}}
.stMarkdown h4, .stMarkdown h5 {{
  color: {BRAND_LT} !important;
  font-weight: 700;
  letter-spacing: 0.5px;
}}

/* ══════════════════════════════════════════
   SUPPRIMER TOUS LES FONDS BLANCS STREAMLIT
══════════════════════════════════════════ */
[data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
.main, .block-container,
[data-testid="column"],
[data-testid="stForm"],
div.stTabs,
div[data-testid="stTabsContent"],
[data-baseweb="tab-panel"] {{
  background: transparent !important;
}}
.block-container {{
  padding-top: 1.5rem !important;
  max-width: 100% !important;
}}
/* Fond des popups / tooltips */
[data-baseweb="tooltip"] > div,
[data-baseweb="popover"] > div {{
  background: {BG_CARD2} !important;
  border: 1px solid {BORDER_LT} !important;
  border-radius: 10px !important;
  color: {TEXT} !important;
}}
/* Inputs / select */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div {{
  background: rgba(4,12,136,0.15) !important;
  border-color: rgba(77,106,255,0.35) !important;
  color: {TEXT} !important;
}}
/* Alertes Streamlit */
[data-testid="stAlert"] {{
  background: rgba(4,12,136,0.2) !important;
  border: 1px solid rgba(77,106,255,0.35) !important;
  border-radius: 12px !important;
  color: {TEXT} !important;
}}
/* Enlever le fond blanc derrière les charts Plotly */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg {{
  background: transparent !important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo blanc dans la sidebar
    st.markdown(f"""
    <div style="padding: 12px 8px 4px; text-align: center;">
      {logo_img(LOGO_WHITE_B64, width="160px", extra="opacity:0.92;")}
    </div>
    <div style="text-align:center; margin: 6px 0 12px;">
      <span style="font-size:0.7rem; color:{TEXT_DIM}; letter-spacing:2px;
                   text-transform:uppercase; font-weight:500;">
        Business Plan V7 · IA
      </span>
    </div>
    <div class="brand-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin:10px 0 6px'>Modèle Économique</p>",
                unsafe_allow_html=True)
    avg_basket = st.slider("Panier moyen (FCFA)", 1500, 6000, 3000, 100)
    avg_cmd    = st.slider("Commandes / MAU / mois", 1.0, 5.0, 2.5, 0.1)
    frais_liv  = st.slider("Frais livraison moy. (FCFA)", 500, 2500, 1200, 50)
    marge_liv  = st.slider("Marge livraison (%)", 20, 65, 40, 1)

    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin:14px 0 6px'>Formules Restaurants</p>",
                unsafe_allow_html=True)
    pct_starter = st.slider("% Starter (gratuit)", 40, 80, 60, 5)
    pct_pro     = st.slider("% Pro (25K/mois)", 10, 50, 30, 5)
    pct_prem    = max(0, 100 - pct_starter - pct_pro)
    st.caption(f"% Premium (50K/mois) = {pct_prem}%")

    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin:14px 0 6px'>Croissance MAU</p>",
                unsafe_allow_html=True)
    mau_L = st.slider("MAU plateau", 40_000, 200_000, 80_000, 5_000,
                      format="%d")
    mau_k = st.slider("Vitesse croissance k", 0.05, 0.20, 0.10, 0.01)

    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin:14px 0 6px'>Monte Carlo</p>",
                unsafe_allow_html=True)
    n_mc = st.slider("Simulations", 200, 2000, 500, 100)
    run_mc_btn = st.button("▶  Lancer Monte Carlo", use_container_width=True)

    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='text-align:center;font-size:0.7rem;color:{TEXT_DIM};line-height:1.6'>
      ISM Dakar · 2025<br>
      <span style='color:{BRAND_LT};font-weight:600'>Adote Mario-Giovani ADUAYI-AKUE</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PARAMÈTRES & CALCULS
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

@st.cache_data(show_spinner="Simulation Monte Carlo…")
def get_mc(pk, n):
    return run_monte_carlo(n=n, params=dict(pk))

params_key = tuple(sorted(params.items()))
res   = get_model(params_key)
m     = res["mau"]
ca    = res["ca_annuel"]
fin   = res["financiers"]
rev_m = res["monthly"]["revenues"]
cst_m = res["monthly"]["costs"]
pft_m = res["monthly"]["profit"]
terr  = res["terrain"]

if "mc" not in st.session_state or run_mc_btn:
    st.session_state["mc"] = get_mc(params_key, n_mc)
mc = st.session_state.get("mc")

YEARS  = ["An 1\n2027","An 2\n2028","An 3\n2029","An 4\n2030","An 5\n2031"]
MONTHS = list(range(1, 61))

# ══════════════════════════════════════════════════════════════
# EN-TÊTE PRINCIPAL
# ══════════════════════════════════════════════════════════════

mau_an3 = m["central"]["an3"]
ca_an3  = ca["central"]["an3"]
ca_an5  = ca["central"]["an5"]
dr      = fin["delai_mois"]
van_ok  = fin["van"] > 0
tri_val = fin["tri"] or 0

st.markdown(f"""
<div class="ec-header-bar">
  <div style="flex-shrink:0">
    {logo_img(LOGO_WHITE_B64, width="180px")}
  </div>
  <div style="flex:1">
    <div style="font-size:0.72rem;color:{TEXT_DIM};letter-spacing:2px;
                text-transform:uppercase;font-weight:500;margin-bottom:4px">
      TABLEAU DE BORD · MODÈLE IA · DAKAR
    </div>
    <div style="font-size:1.55rem;font-weight:800;color:{WHITE};letter-spacing:-0.5px;
                line-height:1.2;">
      Business Plan V7 — Prédictions Financières 2027–2031
    </div>
    <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
      <span class="badge-ok">VAN {fin['van_M']:.1f}M FCFA ✓</span>
      <span class="badge-ok">TRI {tri_val:.0f}% ✓</span>
      <span class="badge-ok">IP {fin['ip']:.1f}x ✓</span>
      <span class="badge-ok">Break-even M{dr}</span>
    </div>
  </div>
  <div style="flex-shrink:0;text-align:right">
    <div style="font-size:0.7rem;color:{TEXT_DIM};text-transform:uppercase;letter-spacing:1px">CA An 5</div>
    <div style="font-size:2rem;font-weight:900;color:{CYAN};letter-spacing:-1px;line-height:1">
      {ca_an5/1e6:.0f}M
    </div>
    <div style="font-size:0.75rem;color:{TEXT_DIM}">FCFA</div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPIs
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("MAU An 1", f"{m['central']['an1']:,}")
k2.metric("MAU An 3", f"{mau_an3:,}", delta="cible")
k3.metric("CA An 1", f"{ca['central']['an1']/1e6:.1f}M FCFA")
k4.metric("CA An 3", f"{ca_an3/1e6:.1f}M FCFA", delta=f"+{(ca_an3/ca['central']['an1']-1)*100:.0f}% vs An1")
k5.metric("VAN (15%)", f"{fin['van_M']:.1f}M FCFA", delta="Positif ✓" if van_ok else "Négatif")

st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ONGLETS
# ══════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Vue d'ensemble",
    "💰  Revenus & Coûts",
    "🌍  Données Terrain",
    "🔀  Scénarios",
    "🎲  Monte Carlo & Sensibilité",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════

with tab1:
    col_l, col_r = st.columns(2)

    # ── Courbe MAU ────────────────────────────────────────────
    with col_l:
        fig = go.Figure()

        # Bande Monte Carlo (fond)
        if mc and "monthly_bands" in mc:
            b = mc["monthly_bands"]
            fig.add_trace(go.Scatter(
                x=MONTHS + MONTHS[::-1],
                y=b["p90"] + b["p10"][::-1],
                fill="toself",
                fillcolor=f"rgba(4,12,136,0.15)",
                line=dict(color="rgba(0,0,0,0)"),
                name="P10–P90 MC", showlegend=True,
                hoverinfo="skip",
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

        # Lignes de séparation annuelles
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color=f"rgba(77,106,255,0.2)", line_width=1)

        fig.update_layout(
            **PLOTLY,
            title=dict(text="Croissance MAU — 5 ans (3 scénarios)",
                       font=dict(color=CYAN, size=14, weight=600)),
            yaxis_title="Utilisateurs actifs mensuels",
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── CA par an ─────────────────────────────────────────────
    with col_r:
        fig = go.Figure()
        for scenario, name, color, opacity in [
            ("optimiste",  "Optimiste",  CYAN,      0.7),
            ("central",    "Central",    BRAND_MED, 0.9),
            ("pessimiste", "Pessimiste", ORANGE,    0.7),
        ]:
            vals = [ca[scenario][f"an{a}"] / 1e6 for a in range(1, 6)]
            fig.add_trace(go.Bar(
                x=YEARS, y=vals, name=name,
                marker=dict(color=color, opacity=opacity,
                            line=dict(color="rgba(255,255,255,0.1)", width=1)),
            ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Chiffre d'Affaires annuel (M FCFA)",
                       font=dict(color=CYAN, size=14, weight=600)),
            barmode="group",
            yaxis_title="Millions FCFA",
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Tableau récap ─────────────────────────────────────────
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>"
                f"Performance par année — Scénario Central</p>", unsafe_allow_html=True)

    rows = []
    for an in range(1, 6):
        rev_an  = sum(r["total_mensuel"] for r in rev_m[(an-1)*12:an*12])
        cout_an = sum(c["total_couts"]   for c in cst_m[(an-1)*12:an*12])
        mg      = rev_an - cout_an
        rows.append({
            "Année":            f"An {an} · {2026+an}",
            "MAU fin d'année":  f"{m['central'][f'an{an}']:>8,}",
            "CA (M FCFA)":      f"{rev_an/1e6:>7.2f}",
            "Coûts (M FCFA)":   f"{cout_an/1e6:>7.2f}",
            "Marge (M FCFA)":   f"{mg/1e6:>7.2f}",
            "Marge nette %":    f"{mg/rev_an*100:.0f}%" if rev_an else "—",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Indicateurs financiers ────────────────────────────────
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    fi1, fi2, fi3, fi4 = st.columns(4)
    fi1.metric("VAN (5 ans, 15%)",       f"{fin['van_M']:.1f}M FCFA",  delta="✓ Positif")
    fi2.metric("TRI",                     f"{tri_val:.1f}%",             delta="✓ > 9% bancaire")
    fi3.metric("Indice Profitabilité",    f"{fin['ip']:.2f}x",           delta="✓ > 1")
    fi4.metric("Budget de lancement",    f"{fin['budget_fcfa']/1e6:.2f}M FCFA")

# ══════════════════════════════════════════════════════════════
# TAB 2 — REVENUS & COÛTS
# ══════════════════════════════════════════════════════════════

with tab2:
    col_a, col_b = st.columns([3, 2])

    # Revenus vs Coûts
    with col_a:
        fig = go.Figure()

        # Coûts (fond rougeâtre)
        fig.add_trace(go.Scatter(
            x=MONTHS, y=[c["total_couts"]/1e6 for c in cst_m],
            name="Coûts", mode="lines",
            line=dict(color=ORANGE, width=2),
            fill="tozeroy", fillcolor="rgba(255,107,53,0.06)",
        ))
        # Revenus (fond bleu)
        fig.add_trace(go.Scatter(
            x=MONTHS, y=[r["total_mensuel"]/1e6 for r in rev_m],
            name="Revenus", mode="lines",
            line=dict(color=BRAND_MED, width=2.8),
            fill="tozeroy", fillcolor="rgba(26,47,255,0.1)",
        ))
        if dr:
            fig.add_vline(x=dr, line_dash="dash", line_color=CYAN, line_width=1.5,
                          annotation_text=f"  Break-even M{dr}",
                          annotation_font=dict(color=CYAN, size=12))

        fig.update_layout(
            **PLOTLY,
            title=dict(text="Revenus vs Coûts mensuels (M FCFA)",
                       font=dict(color=CYAN, size=14, weight=600)),
            height=320, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Donut 7 flux
    with col_b:
        d    = ca["decomp_an1"]
        keys = ["livraison","commission","abonnements","pub","b2b","selection","propres"]
        vals = [d[k] for k in keys]
        fig = go.Figure(go.Pie(
            labels=REV_LABELS, values=vals, hole=0.60,
            marker=dict(colors=REV_COLORS, line=dict(color=BG_DEEP, width=2)),
            textinfo="percent",
            textfont=dict(size=11, color=WHITE),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} FCFA<br>%{percent}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="7 flux — An 1", font=dict(color=CYAN, size=14, weight=600)),
            showlegend=True,
            height=320,
            legend=dict(font_size=10, orientation="v", x=1.02, y=0.5),
            margin=dict(l=0, r=110, t=40, b=0),
            annotations=[dict(
                text=f"<b>{sum(vals)/1e6:.1f}M</b><br>FCFA",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=17, color=WHITE),
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cash flow cumulatif
    fig = go.Figure()
    cumul_vals = [p["cumul"]/1e6 for p in pft_m]
    fig.add_trace(go.Scatter(
        x=MONTHS, y=cumul_vals,
        mode="lines", name="Cumul P&L",
        line=dict(color=CYAN, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,200,255,0.06)",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.25)", line_width=1)
    if dr:
        fig.add_vline(x=dr, line_dash="dash", line_color=CYAN, line_width=1.5)
    fig.update_layout(
        **PLOTLY,
        title=dict(text="Cash Flow Cumulatif depuis investissement initial (M FCFA)",
                   font=dict(color=CYAN, size=14, weight=600)),
        height=260, yaxis_title="M FCFA",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Décomposition coûts + flux revenus côte à côte
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        c1d = cst_m[:12]
        ck  = ["cout_salaires","cout_marketing","cout_tech","cout_operations"]
        cl  = ["Salaires","Marketing","Tech/Infra","Opérations"]
        cc  = [PURPLE, CYAN, TEAL, GOLD]
        fig = go.Figure()
        for k, lbl, col in zip(ck, cl, cc):
            fig.add_trace(go.Bar(
                x=list(range(1,13)), y=[c[k]/1e3 for c in c1d],
                name=lbl, marker_color=col,
                marker_line=dict(width=0),
            ))
        fig.update_layout(
            **PLOTLY, barmode="stack",
            title=dict(text="Structure des coûts — An 1 (K FCFA)",
                       font=dict(color=CYAN, size=13)),
            height=300, showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        fig = go.Figure()
        for k, lbl, col in zip(REV_KEYS, REV_LABELS, REV_COLORS):
            annual = [sum(r[k] for r in rev_m[(an-1)*12:an*12])/1e6 for an in range(1,6)]
            fig.add_trace(go.Bar(x=YEARS, y=annual, name=lbl, marker_color=col,
                                 marker_line=dict(width=0)))
        fig.update_layout(
            **PLOTLY, barmode="stack",
            title=dict(text="Décomposition CA 5 ans (M FCFA)",
                       font=dict(color=CYAN, size=13)),
            height=300, showlegend=True,
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

    st.markdown(f"""
    <div class="ec-card">
      <div style="display:flex;align-items:center;gap:16px">
        <div style="flex:1">
          <span style="font-size:0.78rem;color:{TEXT_DIM};letter-spacing:1px;text-transform:uppercase">
            Collecte de données primaires
          </span>
          <div style="font-size:1rem;font-weight:700;color:{WHITE};margin-top:2px">
            {cli.get('n_repondants',0)} clients · {liv.get('n_entretiens',0)} livreurs ·
            {rest.get('n_discussions',0)} restaurants
          </div>
          <div style="font-size:0.82rem;color:{TEXT_DIM};margin-top:4px">
            Panel extrapolé via benchmarks Chowdeck Nigeria × Facteur Dakar
            <strong style="color:{CYAN}">0.238</strong>
          </div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          <div style="font-size:0.7rem;color:{TEXT_DIM}">Objectif clients</div>
          <div style="font-size:1.4rem;font-weight:800;color:{BRAND_LT}">
            {cli.get('n_repondants',0)}<span style="color:{TEXT_DIM};font-size:1rem">
            /{cli.get('objectif_cible',300)}</span>
          </div>
          <div style="background:{BRAND};border-radius:4px;height:6px;width:120px;margin-top:4px">
            <div style="background:{CYAN};border-radius:4px;height:6px;
              width:{min(cli.get('n_repondants',0)/cli.get('objectif_cible',300)*100,100):.0f}%"></div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        # Clients — indicateurs
        st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:1px;margin:6px 0'>"
                    f"Clients — {cli.get('n_repondants',0)} répondants</p>", unsafe_allow_html=True)

        fig = go.Figure()
        labels = ["Très intéressés","Intérêt total","Wave paiement","Étudiants"]
        vals   = [cli.get("pct_tres_interesse",75), cli.get("pct_interesse_total",100),
                  cli.get("pct_wave",100),          cli.get("pct_etudiants",70)]
        colors_bar = [BRAND_MED, CYAN, PURPLE, TEAL]
        fig.add_trace(go.Bar(
            x=vals, y=labels, orientation="h",
            marker=dict(
                color=colors_bar,
                line=dict(width=0),
            ),
            text=[f"{v:.0f}%" for v in vals],
            textposition="outside",
            textfont=dict(color=WHITE, size=12, weight=600),
        ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Profil clients — indicateurs clés",
                       font=dict(color=CYAN, size=13)),
            xaxis_range=[0, 130], height=240, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Freins
        if cli.get("freins"):
            fr = dict(list(cli["freins"].items())[:5])
            fig = go.Figure(go.Bar(
                x=list(fr.values()), y=list(fr.keys()), orientation="h",
                marker_color=ORANGE, marker_line=dict(width=0),
                text=list(fr.values()), textposition="outside",
                textfont=dict(color=WHITE),
            ))
            fig.update_layout(
                **PLOTLY,
                title=dict(text="Freins principaux", font=dict(color=ORANGE, size=13)),
                height=max(200, len(fr)*50), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Fonctionnalités
        if cli.get("fonctions"):
            fn = dict(list(cli["fonctions"].items())[:5])
            fig = go.Figure(go.Bar(
                x=list(fn.values()), y=list(fn.keys()), orientation="h",
                marker_color=BRAND_LT, marker_line=dict(width=0),
                text=list(fn.values()), textposition="outside",
                textfont=dict(color=WHITE),
            ))
            fig.update_layout(
                **PLOTLY,
                title=dict(text="Fonctionnalités attendues", font=dict(color=BRAND_LT, size=13)),
                height=max(200, len(fn)*50), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_t2:
        # Livreurs
        st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:1px;margin:6px 0'>"
                    f"Livreurs — {liv.get('n_entretiens',0)} entretiens terrain</p>",
                    unsafe_allow_html=True)
        fig = go.Figure()
        llabels = ["Moto personnelle","Wave salaire","Modèle hybride","Disponible soir","Compte Wave"]
        lvals   = [liv.get("pct_moto",96), liv.get("pct_wave_sal",87),
                   liv.get("pct_hybride",70), liv.get("pct_soir",100), liv.get("pct_wave_compte",87)]
        lcolors = [TEAL, BRAND_MED, CYAN, GOLD, PURPLE]
        fig.add_trace(go.Bar(
            x=lvals, y=llabels, orientation="h",
            marker=dict(color=lcolors, line=dict(width=0)),
            text=[f"{v:.0f}%" for v in lvals], textposition="outside",
            textfont=dict(color=WHITE, size=12, weight=600),
        ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Profil livreurs — Terrain",
                       font=dict(color=TEAL, size=13)),
            xaxis_range=[0, 130], height=240, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Zones couvertes
        if liv.get("zones"):
            z = dict(list(sorted(liv["zones"].items(), key=lambda x: -x[1]))[:7])
            fig = go.Figure(go.Bar(
                x=list(z.values()), y=list(z.keys()), orientation="h",
                marker_color=TEAL, marker_line=dict(width=0),
            ))
            fig.update_layout(
                **PLOTLY,
                title=dict(text="Zones couvertes (livreurs)", font=dict(color=TEAL, size=13)),
                height=max(180, len(z)*40), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Restaurants
        st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:1px;margin:6px 0'>"
                    f"Restaurants — {rest.get('n_discussions',0)} discussions</p>",
                    unsafe_allow_html=True)
        rlabels = ["Via WhatsApp","Acceptent Wave","Livreurs propres","Internet stable"]
        rvals   = [rest.get("pct_whatsapp",100), rest.get("pct_wave",80),
                   rest.get("pct_livreurs_propres",40), rest.get("pct_internet_stable",80)]
        rcolors = [BRAND_MED, PURPLE, ORANGE, GOLD]
        fig = go.Figure(go.Bar(
            x=rvals, y=rlabels, orientation="h",
            marker=dict(color=rcolors, line=dict(width=0)),
            text=[f"{v:.0f}%" for v in rvals], textposition="outside",
            textfont=dict(color=WHITE, size=12),
        ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="Profil restaurants", font=dict(color=BRAND_MED, size=13)),
            xaxis_range=[0, 130], height=220, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Concurrents
    if bench:
        st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:1px;margin:6px 0'>"
                    f"Analyse Concurrentielle — Marché Dakar</p>", unsafe_allow_html=True)
        df_b = pd.DataFrame(bench)
        cols = [c for c in ["plateforme","statut","commission_pct","frais_livraison_moy_fcfa",
                             "point_fort","point_faible"] if c in df_b.columns]
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
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color="rgba(77,106,255,0.15)")
        fig.update_layout(
            **PLOTLY,
            title=dict(text="MAU — 3 scénarios (milliers)",
                       font=dict(color=CYAN, size=14)),
            height=340, yaxis_title="MAU (000s)",
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
                marker=dict(size=7, symbol="circle"),
            ))
        fig.update_layout(
            **PLOTLY,
            title=dict(text="CA annuel — 3 scénarios (M FCFA)",
                       font=dict(color=CYAN, size=14)),
            height=340, yaxis_title="M FCFA",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau comparatif
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    rows_s = []
    for an in range(1, 6):
        rows_s.append({
            "Année":             f"An {an} · {2026+an}",
            "MAU Pess.":         f"{m['pessimiste'][f'an{an}']:,}",
            "MAU Central":       f"{m['central'][f'an{an}']:,}",
            "MAU Optim.":        f"{m['optimiste'][f'an{an}']:,}",
            "CA Pess. (M)":      f"{ca['pessimiste'][f'an{an}']/1e6:.2f}",
            "CA Central (M)":    f"{ca['central'][f'an{an}']/1e6:.2f}",
            "CA Optim. (M)":     f"{ca['optimiste'][f'an{an}']/1e6:.2f}",
        })
    st.dataframe(pd.DataFrame(rows_s), use_container_width=True, hide_index=True)

    # Décomposition An 1
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>"
                f"Décomposition CA An 1 — 7 flux nets E-cantine</p>", unsafe_allow_html=True)

    total_an1 = sum(ca["decomp_an1"].values())
    lmap = {"livraison":"① Frais livraison (marge 40%)",
            "commission":"② Commission variable 1–2,5%",
            "abonnements":"③ Abonnements Pro / Premium",
            "pub":"④ Publicité in-app",
            "b2b":"⑤ B2B cantines entreprises",
            "selection":"⑥ Sélection (5%)",
            "propres":"⑦ Livraisons propres (1,5%)"}
    drows = []
    for k, lbl in lmap.items():
        v = ca["decomp_an1"][k]
        drows.append({"Flux":lbl, "FCFA":f"{v:>12,.0f}",
                      "M FCFA":f"{v/1e6:.3f}", "Part":f"{v/total_an1*100:.0f}%"})
    st.dataframe(pd.DataFrame(drows), use_container_width=True, hide_index=True)
    st.markdown(f"""
    <div style='text-align:right;padding:8px 12px;background:rgba(4,12,136,0.2);
                border-radius:8px;margin-top:4px;border:1px solid {BORDER_LT}'>
      <span style='color:{TEXT_DIM};font-size:0.8rem'>TOTAL NET E-CANTINE An 1 : </span>
      <span style='color:{WHITE};font-size:1.2rem;font-weight:800'>{total_an1/1e6:.2f}M FCFA</span>
      <span style='color:{TEXT_DIM};font-size:0.75rem;margin-left:8px'>
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
                marker=dict(color=BRAND_MED, opacity=0.8,
                            line=dict(color=BG_DEEP, width=0.5)),
            ))
            for perc, val, col in [
                ("P10", mc["ca5"]["p10"]/1e6, ORANGE),
                ("P50", mc["ca5"]["p50"]/1e6, WHITE),
                ("P90", mc["ca5"]["p90"]/1e6, CYAN),
            ]:
                fig.add_vline(x=val, line_dash="dash", line_color=col, line_width=2,
                              annotation_text=f"  {perc}: {val:.0f}M",
                              annotation_font=dict(color=col, size=11))
            fig.update_layout(
                **PLOTLY,
                title=dict(text=f"Distribution CA An5 — {mc['n_simulations']} simulations",
                           font=dict(color=CYAN, size=14)),
                height=320, xaxis_title="CA An5 (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_m2:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=[v/1e6 for v in mc["van"]["values"]],
                nbinsx=35, name="VAN",
                marker=dict(color=CYAN, opacity=0.75,
                            line=dict(color=BG_DEEP, width=0.5)),
            ))
            fig.add_vline(x=0, line_dash="dot", line_color=ORANGE, line_width=2,
                          annotation_text="  Seuil 0",
                          annotation_font=dict(color=ORANGE, size=11))
            fig.update_layout(
                **PLOTLY,
                title=dict(
                    text=f"Distribution VAN — {mc['van']['pct_positive']:.0f}% de simulations positives",
                    font=dict(color=CYAN, size=14)),
                height=320, xaxis_title="VAN (M FCFA)", yaxis_title="Fréquence",
            )
            st.plotly_chart(fig, use_container_width=True)

        # KPIs Monte Carlo
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("CA An5 · P10",    f"{mc['ca5']['p10']/1e6:.0f}M FCFA")
        mc2.metric("CA An5 · P50",    f"{mc['ca5']['p50']/1e6:.0f}M FCFA")
        mc3.metric("CA An5 · P90",    f"{mc['ca5']['p90']/1e6:.0f}M FCFA")
        mc4.metric("VAN positive",    f"{mc['van']['pct_positive']:.0f}%",
                   delta="✓ Robuste" if mc["van"]["pct_positive"] > 80 else "")
        mc5.metric("Simulations",     f"{mc['n_simulations']:,}")

    else:
        st.markdown(f"""
        <div class="ec-card-cyan" style="text-align:center;padding:40px">
          <div style="font-size:2.5rem;margin-bottom:12px">🎲</div>
          <div style="font-size:1rem;color:{WHITE};font-weight:600">Monte Carlo non lancé</div>
          <div style="color:{TEXT_DIM};font-size:0.85rem;margin-top:6px">
            Clique sur <strong style="color:{CYAN}">▶ Lancer Monte Carlo</strong> dans la sidebar
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Tornado Sensibilité
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{BRAND_LT};font-size:0.82rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>"
                f"Analyse de Sensibilité — Impact sur CA An 3</p>", unsafe_allow_html=True)

    sens = res.get("sensitivity", [])
    if sens:
        fig = go.Figure()
        labels_s = [s["label"] for s in sens]
        ups  = [s["impact_up"] for s in sens]
        dns  = [s["impact_dn"] for s in sens]

        fig.add_trace(go.Bar(
            y=labels_s, x=ups, orientation="h",
            name=f"+Δ paramètre",
            marker=dict(color=CYAN, opacity=0.85, line=dict(width=0)),
            text=[f"+{v:.1f}%" for v in ups],
            textposition="outside",
            textfont=dict(color=WHITE, size=11),
        ))
        fig.add_trace(go.Bar(
            y=labels_s, x=dns, orientation="h",
            name=f"−Δ paramètre",
            marker=dict(color=ORANGE, opacity=0.85, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in dns],
            textposition="outside",
            textfont=dict(color=WHITE, size=11),
        ))
        fig.add_vline(x=0, line_color=f"rgba(255,255,255,0.2)", line_width=1)
        fig.update_layout(
            **PLOTLY,
            barmode="overlay",
            title=dict(text="Tornado — Impact ±Δ% sur CA An3",
                       font=dict(color=CYAN, size=14)),
            xaxis_title="Impact sur CA An3 (%)",
            height=420,
            legend=dict(orientation="h", y=1.12),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Paramètre le plus impactant en tête. Priorité : maîtriser le panier moyen et le volume de commandes.")

    # Note méthodologique
    st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ec-card">
      <div style="display:flex;align-items:flex-start;gap:16px">
        <div style="font-size:1.8rem;flex-shrink:0">🔬</div>
        <div>
          <div style="font-size:0.85rem;font-weight:700;color:{BRAND_LT};
                      text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">
            Note Méthodologique
          </div>
          <div style="font-size:0.83rem;color:{TEXT_DIM};line-height:1.7">
            Les projections utilisent un modèle de prédiction statistique
            <strong style="color:{WHITE}">(courbe S logistique)</strong>
            calibré sur <strong style="color:{WHITE}">Chowdeck Nigeria (Lagos)</strong>
            × Facteur Dakar <strong style="color:{CYAN}">0.238</strong>
            (population × pouvoir d'achat × pénétration mobile).<br><br>
            Le Monte Carlo simule <strong style="color:{WHITE}">{mc['n_simulations'] if mc else n_mc} variantes</strong>
            en perturbant aléatoirement les paramètres clés (±20–30%), fournissant des
            intervalles de confiance P10–P90 défendables devant jury.<br><br>
            <span style="color:{ORANGE}">Panel terrain limité</span> —
            estimations affinées dès l'atteinte de
            <strong style="color:{WHITE}">300 répondants clients</strong>.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown("<div class='brand-divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 4px;flex-wrap:wrap;gap:8px">
  <div>
    {logo_img(LOGO_WHITE_B64, width="110px", extra="opacity:0.6;")}
  </div>
  <div style="color:{TEXT_DIM};font-size:0.73rem;text-align:center">
    Business Plan V7 · ISM Dakar · 2025 ·
    <strong style="color:{BRAND_LT}">Adote Mario-Giovani ADUAYI-AKUE</strong>
  </div>
  <div style="font-size:0.7rem;color:{TEXT_DIM}">
    Modèle IA · Courbe S × Benchmarks Africains
  </div>
</div>
""", unsafe_allow_html=True)
