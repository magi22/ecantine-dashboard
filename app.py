"""
E-CANTINE · TABLEAU DE BORD IA · BUSINESS PLAN
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

REV_COLORS = [BRAND_MED, CYAN, PURPLE, TEAL2, GOLD, ORANGE]
REV_LABELS = ["① Livraison","② Commission","③ Abonnements (pub incluse)","④ Vitrine","⑤ Propres","⑥ B2B"]
REV_KEYS   = ["rev_livraison","rev_commission","rev_abonnements","rev_selection","rev_propres","rev_b2b"]
YEARS      = ["An 1","An 2","An 3","An 4","An 5"]
MONTHS     = list(range(1, 61))

# ── Helpers layout Plotly ──────────────────────────────────────
# Fonction au lieu de dict spread (**) → impossible d'avoir des doublons de clés
_FONT   = dict(color=TEXT, family="Inter, sans-serif", size=12)
_XAXIS  = dict(gridcolor="#e8ecff", zerolinecolor="#e8ecff",
               tickfont=dict(color=TEXT_DIM, size=11))
_YAXIS  = dict(gridcolor="#e8ecff", zerolinecolor="#e8ecff",
               tickfont=dict(color=TEXT_DIM, size=11))
_BG     = "rgba(0,0,0,0)"
_PLOT   = "rgba(245,247,255,0.5)"
_LEG_H  = dict(bgcolor=_BG, font=dict(size=11),
               orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
_LEG_V  = dict(bgcolor=_BG, font=dict(size=10), orientation="v", x=1.02, y=0.5)

def _layout(title_text="", title_color=None, height=350,
            y_title="", x_title="",
            margin=None, legend=None, showlegend=None,
            barmode=None, xaxis_range=None, pie=False, **extra):
    """Génère un dict layout Plotly sans aucun doublon de clé possible."""
    tc = title_color or TEXT
    mg = margin or dict(l=10, r=10, t=42, b=10)
    d = dict(
        paper_bgcolor=_BG,
        plot_bgcolor=_PLOT,
        font=_FONT,
        margin=mg,
        height=height,
    )
    if title_text:
        d["title"] = dict(text=title_text, font=dict(color=tc, size=14))
    if y_title:
        d["yaxis_title"] = y_title
    if x_title:
        d["xaxis_title"] = x_title
    if legend is not None:
        d["legend"] = legend
    if showlegend is not None:
        d["showlegend"] = showlegend
    if barmode is not None:
        d["barmode"] = barmode
    if xaxis_range is not None:
        d["xaxis_range"] = xaxis_range
    if not pie:
        d["xaxis"] = _XAXIS
        d["yaxis"] = _YAXIS
    for k, v in extra.items():
        d[k] = v
    return d

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

/* ── Métriques — anti-troncature ── */
[data-testid="metric-container"] {{
  background: {WHITE} !important;
  border: 1px solid {BORDER} !important;
  border-top: 3px solid {BRAND_MED} !important;
  border-radius: 14px !important;
  padding: 16px 12px 12px !important;
  box-shadow: 0 2px 16px rgba(4,12,136,0.09) !important;
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: visible !important;
}}
[data-testid="metric-container"]:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(4,12,136,0.16) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
  color: {BRAND} !important;
  font-size: 1.15rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.3px !important;
  white-space: nowrap !important;
  overflow: visible !important;
  line-height: 1.3 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
  color: {TEXT_DIM} !important;
  font-size: 0.70rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.8px !important;
  font-weight: 600 !important;
  white-space: normal !important;
  line-height: 1.3 !important;
  margin-bottom: 4px !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
  color: {GREEN} !important;
  font-size: 0.76rem !important;
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
/* Fix: Streamlit enveloppe le texte du bouton dans un <p> dans certaines versions */
.stButton > button p,
.stButton > button span,
.stButton > button div {{
  color: {WHITE} !important;
  margin: 0 !important;
  font-size: inherit !important;
  font-weight: inherit !important;
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

/* ── Badges — base commune ── */
.badge-ok, .badge-success, .badge-warn, .badge-info {{
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  letter-spacing: 0.2px;
  line-height: 1;
}}
/* bleu — indicateur financier neutre */
.badge-ok {{
  background: #eff6ff;
  color: {BRAND_MED};
  border: 1px solid #bfdbfe;
}}
/* vert — indicateur positif confirmé */
.badge-success {{
  background: #f0fdf4;
  color: #065f46;
  border: 1px solid #a7f3d0;
}}
/* violet — indicateur de rentabilité */
.badge-purple {{
  background: #f5f3ff;
  color: #5b21b6;
  border: 1px solid #ddd6fe;
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  letter-spacing: 0.2px;
  line-height: 1;
}}
/* orange — attention / seuil */
.badge-warn {{
  background: #fff7ed;
  color: #9a3412;
  border: 1px solid #fed7aa;
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

/* ── Forcer couleur texte visible partout dans sidebar ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {{
  color: {TEXT} !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stTickBar"] span,
[data-testid="stSidebar"] [data-testid="stSlider"] p {{
  color: {TEXT_DIM} !important;
}}
/* Valeur du slider en sidebar */
[data-testid="stSidebar"] [data-testid="stSlider"] input {{
  color: {BRAND} !important;
}}
/* Forcer texte visible dans caption (parfois blanc sur blanc) */
[data-testid="stCaptionContainer"] p,
.stCaption p {{
  color: {TEXT_DIM} !important;
  font-size: 0.76rem !important;
}}
/* Fix checkbox et radio labels */
[data-testid="stSidebar"] .stCheckbox label p,
[data-testid="stSidebar"] .stRadio label p {{
  color: {TEXT} !important;
}}

/* ── Profondeur — zone principale ── */
.main .block-container {{
  padding-left: 1.2rem !important;
  padding-right: 1.2rem !important;
}}
/* Graphiques Plotly — carte avec ombre */
[data-testid="stPlotlyChart"] {{
  background: {WHITE} !important;
  border: 1px solid {BORDER} !important;
  border-radius: 14px !important;
  padding: 6px !important;
  box-shadow: 0 2px 14px rgba(4,12,136,0.07) !important;
  margin-bottom: 6px !important;
}}
/* Dataframe — ombre douce */
[data-testid="stDataFrame"] {{
  box-shadow: 0 2px 14px rgba(4,12,136,0.07) !important;
}}

/* ── Sidebar — sections colorées ── */
.sb-section {{
  background: {GREY_BG};
  border: 1px solid {BORDER};
  border-radius: 10px;
  padding: 10px 12px 12px;
  margin-bottom: 10px;
}}
.sb-section-title {{
  font-size: 0.68rem !important;
  color: {BRAND} !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  margin-bottom: 8px !important;
  display: flex;
  align-items: center;
  gap: 6px;
}}

/* ── Forcer couleur texte visible partout dans sidebar ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([data-baseweb]),
[data-testid="stSidebar"] div:not([data-baseweb]),
[data-testid="stSidebar"] label {{
  color: {TEXT} !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] p {{
  color: {TEXT_DIM} !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] input {{
  color: {BRAND} !important;
}}
[data-testid="stSidebar"] .stCheckbox label p,
[data-testid="stSidebar"] .stRadio label p {{
  color: {TEXT} !important;
}}

/* ── Caption ── */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.stCaption, .stCaption p {{
  color: {TEXT_DIM} !important;
  font-size: 0.76rem !important;
}}

/* ── Boutons — texte blanc garanti ── */
.stButton > button,
.stButton > button p,
.stButton > button span,
.stButton > button div {{
  color: {WHITE} !important;
}}

/* ── Texte global — anti blanc-sur-blanc ── */
.stMarkdown p, .stMarkdown li, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown span {{
  color: {TEXT} !important;
}}
.stMarkdown a {{ color: {BRAND_MED} !important; }}

/* ── Alerte / info boxes ── */
[data-testid="stAlert"] {{
  border-radius: 12px !important;
}}

/* ── Section card wrapper ── */
.ec-section-wrap {{
  background: {WHITE};
  border: 1px solid {BORDER};
  border-radius: 16px;
  padding: 20px 22px;
  margin-bottom: 18px;
  box-shadow: 0 2px 14px rgba(4,12,136,0.06);
}}

/* ── Typographie hiérarchie ── */
.h-section {{
  font-size: 1.05rem;
  font-weight: 700;
  color: {BRAND};
  margin: 18px 0 10px;
  letter-spacing: -0.2px;
}}
.h-subsection {{
  font-size: 0.88rem;
  font-weight: 600;
  color: {TEXT};
  margin: 12px 0 6px;
}}
.t-body {{
  font-size: 0.84rem;
  color: {TEXT};
  line-height: 1.7;
}}
.t-dim {{
  font-size: 0.78rem;
  color: {TEXT_DIM};
  line-height: 1.6;
}}

/* ── Slider min/max toujours visibles ── */
[data-testid="stSlider"] [data-baseweb="slider"] {{
  padding-bottom: 4px !important;
}}
/* Tick bar (min / max) */
[data-testid="stSlider"] [data-testid="stTickBar"] {{
  display: flex !important;
  justify-content: space-between !important;
  margin-top: 2px !important;
}}
[data-testid="stSlider"] [data-testid="stTickBar"] span,
[data-testid="stSlider"] [data-testid="stTickBarMax"],
[data-testid="stSlider"] [data-testid="stTickBarMin"] {{
  display: inline-block !important;
  visibility: visible !important;
  opacity: 1 !important;
  font-size: 0.68rem !important;
  color: {TEXT_DIM} !important;
  font-weight: 500 !important;
}}
/* Valeur courante au-dessus du curseur */
[data-testid="stSlider"] [data-baseweb="thumb-value"],
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {{
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  font-size: 0.75rem !important;
  color: {BRAND} !important;
  font-weight: 700 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {GREY_BG}; }}
::-webkit-scrollbar-thumb {{ background: {BRAND_LT}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {BRAND_MED}; }}
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
                   text-transform:uppercase;font-weight:600">Business Plan · IA</span>
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
    mau_L = st.slider("MAU plateau",         40_000, 200_000, 60_000, 5_000)
    mau_k = st.slider("Vitesse croissance k", 0.05,   0.20,    0.07,   0.01)

    st.markdown(f"<p class='ec-label'>Simulation Opérationnelle</p>", unsafe_allow_html=True)
    cmd_par_livreur_j  = st.slider("Cmd/livreur/jour",   4,  20, 8,  1)
    jours_actifs_mois  = st.slider("Jours actifs/mois",  15, 28, 22, 1)
    nb_rest_cible      = st.slider("Restaurants cible An1", 50, 400, 150, 10)
    mau_par_rest       = st.slider("MAU par restaurant", 10, 80, 35, 5)

    st.markdown(f"<p class='ec-label'>Monte Carlo</p>", unsafe_allow_html=True)
    n_mc       = st.slider("Simulations", 200, 2000, 1000, 100)
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
    "nb_rest_cible_an1":   nb_rest_cible,
}

# ── Paramètres opérationnels (hors modèle prédictif) ─────────
OPS = {
    "cmd_par_livreur_j": cmd_par_livreur_j,
    "jours_actifs_mois": jours_actifs_mois,
    "mau_par_rest":      mau_par_rest,
    "nb_rest_cible_an1": nb_rest_cible,
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
    {logo_img(LOGO_BLUE_B64, width="180px")}
  </div>
  <div style="flex:1;padding-left:8px">
    <div style="font-size:0.68rem;color:{TEXT_DIM};letter-spacing:1.5px;
                text-transform:uppercase;font-weight:600;margin-bottom:3px">
      Tableau de Bord · Modèle IA · Dakar 2027–2031
    </div>
    <div style="font-size:1.4rem;font-weight:800;color:{BRAND};letter-spacing:-0.5px">
      Business Plan — Prédictions Financières
    </div>
    <div style="margin-top:10px;display:flex;gap:7px;flex-wrap:wrap">
      <span class="badge-success">✓ VAN {fin['van_M']:.1f}M FCFA</span>
      <span class="badge-success">✓ TRI {tri_val:.0f}%</span>
      <span class="badge-purple">◆ IP {fin['ip']:.1f}x</span>
      <span class="badge-ok">⏱ Break-even M{dr}</span>
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊  Vue d'ensemble",
    "💰  Revenus & Coûts",
    "🌍  Données Terrain",
    "🔀  Scénarios",
    "🎲  Monte Carlo",
    "💸  Charges & Trésorerie",
    "📦  Opérationnel",
    "📖  Glossaire & Guide",
    "🗺️  À propos du Modèle",
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
            **_layout("Croissance MAU — 5 ans", BRAND, 330, y_title="Utilisateurs actifs", legend=_LEG_H),
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
            **_layout("CA Annuel — 3 scénarios (M FCFA)", BRAND, 330, y_title="Millions FCFA", legend=_LEG_H, barmode="group"),
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

    # ── Interprétation dynamique liée aux sliders actuels ────────
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Interprétation — paramètres actuels</p>",
                unsafe_allow_html=True)

    ca_an1_v  = ca["central"]["an1"] / 1e6
    ca_an3_v  = ca["central"]["an3"] / 1e6
    ca_an5_v  = ca["central"]["an5"] / 1e6
    mau_an1_v = m["central"]["an1"]
    mau_an3_v = m["central"]["an3"]
    cmd_an1   = sum(r["commandes"] for r in rev_m[:12])
    cmd_an3   = sum(r["commandes"] for r in rev_m[24:36])

    # Verdict panier moyen
    if avg_basket >= 4000:
        panier_msg = f"Le panier moyen de <b>{avg_basket:,} FCFA</b> est élevé — hypothèse optimiste, à valider terrain."
        panier_col = ORANGE
    elif avg_basket >= 2500:
        panier_msg = f"Le panier moyen de <b>{avg_basket:,} FCFA</b> est réaliste pour Dakar (repas + boisson)."
        panier_col = GREEN
    else:
        panier_msg = f"Le panier moyen de <b>{avg_basket:,} FCFA</b> est conservateur — marge de progression importante."
        panier_col = TEAL2

    # Verdict MAU plateau
    if mau_L >= 100_000:
        mau_msg = f"Objectif MAU plateau <b>{mau_L:,}</b> ambitieux — nécessite une couverture multi-quartiers Dakar."
        mau_col = ORANGE
    elif mau_L >= 60_000:
        mau_msg = f"Objectif MAU plateau <b>{mau_L:,}</b> — cohérent avec la population cible (étudiants + actifs)."
        mau_col = GREEN
    else:
        mau_msg = f"Objectif MAU plateau <b>{mau_L:,}</b> — scénario prudent, atteint plus tôt (break-even accéléré)."
        mau_col = TEAL2

    # Verdict croissance
    if mau_k >= 0.15:
        k_msg = f"Vitesse k={mau_k:.2f} très élevée — suppose un effet viral fort (bouche à oreille + réseaux sociaux)."
        k_col = ORANGE
    elif mau_k >= 0.09:
        k_msg = f"Vitesse k={mau_k:.2f} — croissance progressive, cohérente avec Chowdeck Lagos phase 1."
        k_col = GREEN
    else:
        k_msg = f"Vitesse k={mau_k:.2f} — croissance lente, bon pour le scénario pessimiste (prudence BP)."
        k_col = TEAL2

    # Verdict global
    if fin["van_M"] > 500 and tri_val > 100:
        glob_icon, glob_msg, glob_col = "🟢", f"Excellent : VAN {fin['van_M']:.0f}M + TRI {tri_val:.0f}% → projet très rentable avec ces paramètres.", GREEN
    elif fin["van_M"] > 100 and tri_val > 30:
        glob_icon, glob_msg, glob_col = "✅", f"Bon : VAN {fin['van_M']:.0f}M + TRI {tri_val:.0f}% → projet rentable et viable.", TEAL2
    elif fin["van_M"] > 0:
        glob_icon, glob_msg, glob_col = "🟡", f"Acceptable : VAN positive ({fin['van_M']:.0f}M) mais TRI {tri_val:.0f}% — optimiser les leviers.", GOLD
    else:
        glob_icon, glob_msg, glob_col = "🔴", f"Attention : VAN négative ({fin['van_M']:.0f}M) avec ces paramètres — ajuster panier/MAU.", ORANGE

    st.markdown(f"""
    <div class="ec-card" style="border-left:4px solid {glob_col}">
      <div style="font-size:0.9rem;font-weight:700;color:{glob_col};margin-bottom:12px">
        {glob_icon} Verdict global avec ces paramètres
      </div>
      <div style="font-size:0.84rem;color:{TEXT};line-height:1.8;margin-bottom:10px">
        {glob_msg}<br>
        CA An 1 = <b>{ca_an1_v:.1f}M</b> → An 3 = <b>{ca_an3_v:.1f}M</b> → An 5 = <b>{ca_an5_v:.1f}M</b> FCFA
        (croissance ×{ca_an5_v/ca_an1_v:.1f} sur 5 ans).<br>
        En An 1 : <b>{cmd_an1:,} commandes totales</b> · En An 3 : <b>{cmd_an3:,} commandes</b>.
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:8px">
        <div style="background:{GREY_BG};border-radius:8px;padding:8px 12px;
                    font-size:0.80rem;color:{TEXT};border-left:3px solid {panier_col}">
          {panier_msg}
        </div>
        <div style="background:{GREY_BG};border-radius:8px;padding:8px 12px;
                    font-size:0.80rem;color:{TEXT};border-left:3px solid {mau_col}">
          {mau_msg}
        </div>
        <div style="background:{GREY_BG};border-radius:8px;padding:8px 12px;
                    font-size:0.80rem;color:{TEXT};border-left:3px solid {k_col}">
          {k_msg}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

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
            **_layout("Revenus vs Coûts mensuels (M FCFA)", BRAND, 310, y_title="M FCFA", legend=_LEG_H),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        d    = ca["decomp_an1"]
        keys = ["livraison","commission","abonnements","selection","propres","b2b"]
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
            **_layout("6 flux revenus nets — An 1", BRAND, 310,
                      legend=_LEG_V, showlegend=True,
                      margin=dict(l=0, r=115, t=42, b=0), pie=True),
        )
        fig.add_annotation(
            text=f"<b>{total_donut/1e6:.1f}M</b><br>FCFA",
            x=0.44, y=0.5, showarrow=False,
            font=dict(size=16, color=BRAND),
            xref="paper", yref="paper",
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
        **_layout("Cash Flow Cumulatif depuis investissement (M FCFA)", BRAND, 260, y_title="M FCFA", legend=_LEG_H),
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
        _leg4 = dict(bgcolor=_BG, font=dict(size=10), orientation="h",
                     yanchor="top", y=-0.15, xanchor="center", x=0.5)
        fig.update_layout(
            **_layout("Coûts An 1 (K FCFA)", BRAND, 320, barmode="stack", legend=_leg4,
                      margin=dict(l=10, r=10, t=42, b=60)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        fig = go.Figure()
        for k, lbl, col in zip(REV_KEYS, REV_LABELS, REV_COLORS):
            annual = [sum(r[k] for r in rev_m[(an-1)*12:an*12])/1e6 for an in range(1,6)]
            fig.add_trace(go.Bar(x=YEARS, y=annual, name=lbl,
                                 marker=dict(color=col, line=dict(width=0))))
        _leg7 = dict(bgcolor=_BG, font=dict(size=10), orientation="h",
                     yanchor="top", y=-0.18, xanchor="center", x=0.5)
        fig.update_layout(
            **_layout("Décomposition CA 5 ans (M FCFA)", BRAND, 340,
                      barmode="stack", legend=_leg7,
                      margin=dict(l=10, r=10, t=42, b=80)),
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
    n_obj = cli.get("objectif_cible", 1_000)
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
            Réseau de connaissance du fondateur — personnes commandant régulièrement à Dakar.<br>
            Modèle calibré sur Chowdeck Nigeria × Facteur Dakar <b style="color:{BRAND_MED}">0.238</b>
            (Chowdeck = benchmark calibration uniquement — hors Sénégal)
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
            **_layout(height=220, showlegend=False, xaxis_range=[0,125],
                      margin=dict(l=10, r=50, t=10, b=10)),
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
                **_layout("Freins principaux", BRAND, max(180, len(fr)*48),
                          showlegend=False, margin=dict(l=10, r=50, t=42, b=10)),
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
            **_layout(height=220, showlegend=False, xaxis_range=[0,125],
                      margin=dict(l=10, r=50, t=10, b=10)),
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
            **_layout(height=200, showlegend=False, xaxis_range=[0,125],
                      margin=dict(l=10, r=50, t=10, b=10)),
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
            **_layout("MAU — 3 scénarios (milliers)", BRAND, 330, y_title="MAU (000s)", legend=_LEG_H),
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
            **_layout("CA annuel — 3 scénarios (M FCFA)", BRAND, 330, y_title="M FCFA", legend=_LEG_H),
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
    st.markdown("<p class='ec-label'>Décomposition CA An 1 — 6 flux nets E-cantine</p>",
                unsafe_allow_html=True)
    total_an1 = sum(v for k, v in ca["decomp_an1"].items() if k != "pub")
    lmap = {"livraison":"① Frais livraison (marge 40%)",
            "commission":"② Commission dégrésive 1–2,5%",
            "abonnements":"③ Abonnements Pro/Premium (pub incluse)",
            "selection":"④ E-cantine Vitrine (5%)",
            "propres":"⑤ Livr. propres (2,5%)",
            "b2b":"⑥ B2B cantines entreprises"}
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
        (Frais BCEAO 1% max 5 000 FCFA — reversés à Wave / Orange Money / Mix by Yass — pas un revenu E-cantine)
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
                **_layout(f"Distribution CA An5 — {mc['n_simulations']} simulations",
                          BRAND, 310, x_title="CA An5 (M FCFA)", y_title="Fréquence", showlegend=False),
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
                **_layout(f"Distribution VAN — {mc['van']['pct_positive']:.0f}% positives",
                          BRAND, 310, x_title="VAN (M FCFA)", y_title="Fréquence", showlegend=False),
            )
            st.plotly_chart(fig, use_container_width=True)

        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("CA An5 · P10", f"{mc['ca5']['p10']/1e6:.0f}M FCFA")
        mc2.metric("CA An5 · P50", f"{mc['ca5']['p50']/1e6:.0f}M FCFA")
        mc3.metric("CA An5 · P90", f"{mc['ca5']['p90']/1e6:.0f}M FCFA")
        mc4.metric("VAN positive",  f"{mc['van']['pct_positive']:.0f}%",
                   delta="robuste" if mc["van"]["pct_positive"] > 80 else "")
        mc5.metric("Simulations",   f"{mc['n_simulations']:,}")

        # ── Interprétation automatique Monte Carlo ────────────────
        st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
        st.markdown("<p class='ec-label'>Interprétation des Résultats</p>",
                    unsafe_allow_html=True)
        pct_pos  = mc["van"]["pct_positive"]
        ca5_p10  = mc["ca5"]["p10"] / 1e6
        ca5_p50  = mc["ca5"]["p50"] / 1e6
        ca5_p90  = mc["ca5"]["p90"] / 1e6
        van_p50  = mc["van"].get("p50", 0) / 1e6 if "p50" in mc["van"] else None
        if pct_pos >= 90:
            verdict_icon, verdict_txt, verdict_col = "✅", "Très favorable — projet robuste", GREEN
        elif pct_pos >= 70:
            verdict_icon, verdict_txt, verdict_col = "🟢", "Favorable — bonne visibilité", TEAL2
        elif pct_pos >= 50:
            verdict_icon, verdict_txt, verdict_col = "🟡", "Neutre — incertitude modérée", GOLD
        else:
            verdict_icon, verdict_txt, verdict_col = "⚠️", "Risqué — forte incertitude", ORANGE
        fourchette_ecart = ca5_p90 - ca5_p10
        st.markdown(f"""
        <div class="ec-card-accent">
          <div style="font-size:1.1rem;font-weight:700;color:{verdict_col};margin-bottom:10px">
            {verdict_icon} Verdict global : {verdict_txt}
          </div>
          <div style="font-size:0.88rem;color:{TEXT};line-height:1.8">
            Sur <b>{mc['n_simulations']:,} simulations</b> avec des paramètres variés aléatoirement (±20-30%) :
            <ul style="margin:8px 0;padding-left:20px">
              <li><b style="color:{verdict_col}">{pct_pos:.0f}%</b> des scénarios donnent une VAN positive
                — le projet est rentable dans <b>{pct_pos:.0f}%</b> des cas testés.</li>
              <li>CA An 5 entre <b>{ca5_p10:.0f}M</b> (cas pessimiste P10)
                et <b>{ca5_p90:.0f}M FCFA</b> (cas optimiste P90),
                avec une valeur centrale (P50) de <b>{ca5_p50:.0f}M FCFA</b>.</li>
              <li>L'écart P90–P10 est de <b>{fourchette_ecart:.0f}M FCFA</b>
                — {'fourchette serrée, projections fiables' if fourchette_ecart < ca5_p50 else 'fourchette large, sensibilité élevée aux hypothèses'}.</li>
            </ul>
            <b>À retenir pour le jury :</b> même dans le scénario le plus défavorable (P10),
            le CA An 5 atteint <b>{ca5_p10:.0f}M FCFA</b>.
            La robustesse du modèle est confirmée par {pct_pos:.0f}% de VAN positive.
          </div>
        </div>
        """, unsafe_allow_html=True)

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
            **_layout("Tornado — Impact ±Δ% sur CA An3", BRAND, 400,
                      x_title="Impact (%)", barmode="overlay",
                      legend=dict(bgcolor=_BG, font=dict(size=11), orientation="h", y=1.12)),
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
            100 entretiens réseau de connaissance + 23 livreurs terrain + 8 restaurants (Trophet, Chez Mervi, Chez Maman Gaga…).
            Modèle calibré sur <b style="color:{TEXT}">Chowdeck Nigeria</b>
            × Facteur Dakar <b style="color:{BRAND_MED}">0.238</b>
            (Chowdeck = benchmark calibration — non présent au Sénégal).<br>
            Monte Carlo : <b style="color:{TEXT}">{mc['n_simulations'] if mc else n_mc} variantes</b>
            avec perturbation aléatoire ±20–30% → intervalles P10–P90.<br>
            Objectif : <b style="color:{TEXT}">1 000 répondants</b> via formulaire in-app An 1
            (IC 95%, marge ±3,1%).
            Dashboard : <a href="https://ecantine-dash.streamlit.app/" style="color:{BRAND_MED}">ecantine-dash.streamlit.app</a>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 6 — CHARGES & TRÉSORERIE
# ══════════════════════════════════════════════════════════════
with tab6:
    ck = ["cout_salaires", "cout_marketing", "cout_tech", "cout_operations"]
    cl = ["Salaires", "Marketing", "Tech/Infra", "Opérations"]
    cc = [BRAND_MED, CYAN, TEAL2, GOLD]

    col_ch1, col_ch2 = st.columns(2)

    with col_ch1:
        st.markdown("<p class='ec-label'>Charges empilées — 60 mois</p>",
                    unsafe_allow_html=True)
        fig = go.Figure()
        for k, lbl, col in zip(ck, cl, cc):
            fig.add_trace(go.Scatter(
                x=MONTHS, y=[c[k] / 1e6 for c in cst_m],
                name=lbl, mode="lines",
                line=dict(color=col, width=1),
                stackgroup="one",
            ))
        fig.update_layout(
            **_layout("Décomposition des charges mensuelles (M FCFA)", BRAND, 320,
                      y_title="M FCFA", legend=_LEG_H),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_ch2:
        st.markdown("<p class='ec-label'>Marge nette mensuelle</p>",
                    unsafe_allow_html=True)
        fig = go.Figure()
        marge_vals = [c.get("marge_pct", 0) for c in cst_m]
        colors_bar = [GREEN if v >= 0 else ORANGE for v in marge_vals]
        fig.add_trace(go.Bar(
            x=MONTHS, y=marge_vals,
            marker=dict(color=colors_bar, line=dict(width=0)),
            name="Marge nette %",
        ))
        fig.add_hline(y=0, line_dash="dot", line_color=TEXT_DIM, line_width=1)
        if dr:
            fig.add_vline(x=dr, line_dash="dash", line_color=GREEN, line_width=2,
                          annotation_text=f"  Break-even M{dr}",
                          annotation_font=dict(color=GREEN, size=11))
        fig.update_layout(
            **_layout("Marge nette mensuelle (%)", BRAND, 320,
                      y_title="%", showlegend=False),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Plan de trésorerie cumulatif
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Plan de Trésorerie Cumulatif</p>",
                unsafe_allow_html=True)

    fig = go.Figure()
    cumul_tres = [p["cumul"] / 1e6 for p in pft_m]
    profit_m_vals = [p["profit_mensuel"] / 1e6 for p in pft_m]
    # Zone rouge sous 0, verte au-dessus
    fig.add_trace(go.Scatter(
        x=MONTHS, y=cumul_tres,
        mode="lines", name="Trésorerie cumulée",
        line=dict(color=BRAND_MED, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(26,47,255,0.08)",
    ))
    fig.add_trace(go.Bar(
        x=MONTHS, y=profit_m_vals,
        name="Profit mensuel",
        marker=dict(
            color=[GREEN if v >= 0 else ORANGE for v in profit_m_vals],
            opacity=0.4, line=dict(width=0),
        ),
        yaxis="y2",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color=ORANGE, line_width=1.5)
    if dr:
        fig.add_vline(x=dr, line_dash="dash", line_color=GREEN, line_width=2,
                      annotation_text=f"  Break-even M{dr}",
                      annotation_font=dict(color=GREEN, size=12))
    fig.update_layout(
        **_layout("Trésorerie cumulée & Profit mensuel (M FCFA)", BRAND, 320,
                  y_title="Trésorerie cumulée (M)", legend=_LEG_H,
                  yaxis2=dict(overlaying="y", side="right",
                              title=dict(text="Profit mensuel (M)", font=dict(color=TEXT_DIM, size=11)),
                              tickfont=dict(color=TEXT_DIM, size=10),
                              gridcolor="rgba(0,0,0,0)")),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tableaux annuels détaillés
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='ec-label'>Charges annuelles détaillées vs CA</p>",
                unsafe_allow_html=True)
    rows_ch = []
    for an in range(1, 6):
        s, e = (an - 1) * 12, an * 12
        rev_an  = sum(r["total_mensuel"]    for r in rev_m[s:e])
        ch_tot  = sum(c["total_couts"]      for c in cst_m[s:e])
        ch_sal  = sum(c["cout_salaires"]    for c in cst_m[s:e])
        ch_mkt  = sum(c["cout_marketing"]   for c in cst_m[s:e])
        ch_tec  = sum(c["cout_tech"]        for c in cst_m[s:e])
        ch_ops  = sum(c["cout_operations"]  for c in cst_m[s:e])
        res_an  = rev_an - ch_tot
        rows_ch.append({
            "Année":                  f"An {an} · {2026+an}",
            "CA (M FCFA)":            f"{rev_an/1e6:.2f}",
            "Total Charges (M)":      f"{ch_tot/1e6:.2f}",
            "· Salaires (M)":         f"{ch_sal/1e6:.2f}",
            "· Marketing (M)":        f"{ch_mkt/1e6:.2f}",
            "· Tech/Infra (M)":       f"{ch_tec/1e6:.2f}",
            "· Opérations (M)":       f"{ch_ops/1e6:.2f}",
            "Résultat net (M)":       f"{res_an/1e6:.2f}",
            "Marge nette":            f"{res_an/rev_an*100:.0f}%" if rev_an else "—",
        })
    st.dataframe(pd.DataFrame(rows_ch), use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;
                padding:14px 18px;margin-top:8px;font-size:0.84rem;color:{TEXT}">
      <b style="color:{BRAND}">Investissement initial :</b>
      {fin['budget_fcfa']/1e6:.2f}M FCFA — récupéré au mois
      <b style="color:{GREEN}">M{fin['delai_mois']}</b> (break-even cumulatif).<br>
      <span style="color:{TEXT_DIM}">Taux d'actualisation utilisé pour la VAN : 15% (coût opportunité ISM/UEMOA).</span><br>
      <span style="color:{TEXT_DIM}"><b>Frais BCEAO 1%</b> (max 5 000 FCFA) : réglementaires, reversés à Wave / Orange Money / Mix by Yass — <b>pas un revenu E-cantine</b>.</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 7 — OPÉRATIONNEL (simulation livreurs, restaurants, cmd)
# ══════════════════════════════════════════════════════════════
with tab7:
    # Calcul des séries opérationnelles à partir des données modèle
    cap_liv_mois = OPS["cmd_par_livreur_j"] * OPS["jours_actifs_mois"]
    n_liv_m  = [max(1, int(np.ceil(r["commandes"] / cap_liv_mois))) for r in rev_m]
    # n_restaurants calculé directement ici (compatible avec cache ancien)
    n_rest_m = [r.get("n_restaurants",
                       int(min(r["mau"] / max(OPS["mau_par_rest"], 1), nb_rest_cible)))
                for r in rev_m]
    cmd_m    = [r["commandes"] for r in rev_m]

    # Comparaison terrain vs modèle
    n_liv_terrain  = terr.get("livreurs", {}).get("n_entretiens", 23)
    n_rest_terrain = terr.get("restaurants", {}).get("n_discussions", 5)

    # ── KPIs opérationnels An 1 et An 3 ──────────────────────
    o1, o2, o3, o4, o5 = st.columns(5)
    o1.metric("Commandes An 1",   f"{sum(cmd_m[:12]):,}")
    o2.metric("Commandes An 3",   f"{sum(cmd_m[24:36]):,}",
              delta=f"+{sum(cmd_m[24:36])/sum(cmd_m[:12])*100-100:.0f}%")
    o3.metric("Livreurs An 1",    f"{max(n_liv_m[:12]):,}", delta="pic mensuel")
    o4.metric("Livreurs An 3",    f"{max(n_liv_m[24:36]):,}", delta="pic mensuel")
    o5.metric("Restaurants An 1", f"{max(n_rest_m[:12]):,}", delta=f"cible {nb_rest_cible}")

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)

    col_op1, col_op2 = st.columns(2)

    with col_op1:
        # Graphique commandes mensuelles
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS, y=cmd_m, mode="lines", name="Commandes/mois",
            line=dict(color=BRAND_MED, width=2.5),
            fill="tozeroy", fillcolor="rgba(26,47,255,0.07)",
        ))
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color="rgba(4,12,136,0.15)", line_width=1)
        fig.update_layout(
            **_layout("Commandes mensuelles simulées", BRAND, 290,
                      y_title="Commandes", showlegend=False),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Interprétation commandes
        cmd_an1_total = sum(cmd_m[:12])
        cmd_an5_total = sum(cmd_m[48:60])
        cmd_moy_an1   = cmd_an1_total // 12
        if cmd_moy_an1 < 500:
            cmd_msg, cmd_col = f"Volume An 1 faible ({cmd_moy_an1:,} cmd/mois) — priorité : acquisition clients et fidélisation.", ORANGE
        elif cmd_moy_an1 < 2000:
            cmd_msg, cmd_col = f"Volume An 1 modéré ({cmd_moy_an1:,} cmd/mois) — réaliste pour un démarrage à Dakar.", TEAL2
        else:
            cmd_msg, cmd_col = f"Volume An 1 élevé ({cmd_moy_an1:,} cmd/mois) — suppose une adoption rapide dès le lancement.", GREEN
        st.markdown(f"""
        <div style="background:{GREY_BG};border-left:3px solid {cmd_col};border-radius:8px;
                    padding:8px 12px;font-size:0.81rem;color:{TEXT};margin-top:4px">
          {cmd_msg}<br>
          <span style="color:{TEXT_DIM}">An 1 : <b>{cmd_an1_total:,}</b> commandes totales →
          An 5 : <b>{cmd_an5_total:,}</b> (×{cmd_an5_total/cmd_an1_total:.1f})</span>
        </div>
        """, unsafe_allow_html=True)

    with col_op2:
        # Graphique livreurs nécessaires
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS, y=n_liv_m, mode="lines", name="Livreurs nécessaires",
            line=dict(color=PURPLE, width=2.5),
            fill="tozeroy", fillcolor="rgba(124,58,237,0.07)",
        ))
        fig.add_hline(y=n_liv_terrain, line_dash="dash", line_color=ORANGE, line_width=2,
                      annotation_text=f"  Terrain actuel : {n_liv_terrain}",
                      annotation_font=dict(color=ORANGE, size=11))
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color="rgba(4,12,136,0.15)", line_width=1)
        fig.update_layout(
            **_layout("Livreurs nécessaires (simulation)", BRAND, 290,
                      y_title="Nb livreurs", showlegend=False),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Interprétation livreurs
        liv_an1_max = max(n_liv_m[:12])
        liv_an3_max = max(n_liv_m[24:36])
        ecart_terrain = liv_an1_max - n_liv_terrain
        if ecart_terrain > 50:
            liv_msg = f"<b>{ecart_terrain} livreurs supplémentaires</b> à recruter avant An 1 (base terrain : {n_liv_terrain})."
            liv_col = ORANGE
        elif ecart_terrain > 10:
            liv_msg = f"<b>{ecart_terrain} livreurs</b> à recruter en plus de la base terrain ({n_liv_terrain}) — faisable progressivement."
            liv_col = GOLD
        else:
            liv_msg = f"Base terrain ({n_liv_terrain} livreurs) suffisante pour An 1 ({liv_an1_max} nécessaires)."
            liv_col = GREEN
        st.markdown(f"""
        <div style="background:{GREY_BG};border-left:3px solid {liv_col};border-radius:8px;
                    padding:8px 12px;font-size:0.81rem;color:{TEXT};margin-top:4px">
          {liv_msg}<br>
          <span style="color:{TEXT_DIM}">Capacité par livreur :
          <b>{OPS['cmd_par_livreur_j']} cmd/jour × {OPS['jours_actifs_mois']} j = {cap_liv_mois} cmd/mois</b>.
          Ajuste le slider "Cmd/livreur/jour" pour tester.</span>
        </div>
        """, unsafe_allow_html=True)

    # Graphique restaurants
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    col_op3, col_op4 = st.columns(2)

    with col_op3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS, y=n_rest_m, mode="lines", name="Restaurants partenaires",
            line=dict(color=TEAL2, width=2.5),
            fill="tozeroy", fillcolor="rgba(20,184,166,0.08)",
        ))
        fig.add_hline(y=n_rest_terrain, line_dash="dash", line_color=ORANGE, line_width=2,
                      annotation_text=f"  Terrain actuel : {n_rest_terrain}",
                      annotation_font=dict(color=ORANGE, size=11))
        fig.add_hline(y=nb_rest_cible, line_dash="dot", line_color=GREEN, line_width=1.5,
                      annotation_text=f"  Cible An 1 : {nb_rest_cible}",
                      annotation_font=dict(color=GREEN, size=11))
        for idx in [12, 24, 36, 48]:
            fig.add_vline(x=idx, line_dash="dot",
                          line_color="rgba(4,12,136,0.15)", line_width=1)
        fig.update_layout(
            **_layout("Restaurants partenaires (simulation)", BRAND, 290,
                      y_title="Nb restaurants", showlegend=False),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Interprétation restaurants
        rest_an1 = max(n_rest_m[:12])
        rest_an3 = max(n_rest_m[24:36])
        ecart_rest = rest_an1 - n_rest_terrain
        if ecart_rest > 100:
            rest_msg = f"<b>{ecart_rest} restaurants</b> à convaincre avant An 1 — effort commercial majeur (base : {n_rest_terrain})."
            rest_col = ORANGE
        elif ecart_rest > 30:
            rest_msg = f"<b>{ecart_rest} restaurants</b> à signer en An 1 — faisable avec 2-3 commerciaux terrain."
            rest_col = GOLD
        else:
            rest_msg = f"Base terrain ({n_rest_terrain}) couvre les besoins An 1 ({rest_an1} nécessaires)."
            rest_col = GREEN
        st.markdown(f"""
        <div style="background:{GREY_BG};border-left:3px solid {rest_col};border-radius:8px;
                    padding:8px 12px;font-size:0.81rem;color:{TEXT};margin-top:4px">
          {rest_msg}<br>
          <span style="color:{TEXT_DIM}">Ratio modèle : 1 restaurant pour <b>{OPS['mau_par_rest']} MAU</b>.
          Ajuste "MAU par restaurant" sidebar pour changer ce ratio.</span>
        </div>
        """, unsafe_allow_html=True)

    with col_op4:
        # Tableau annuel opérationnel
        st.markdown("<p class='ec-label'>Récap opérationnel annuel</p>",
                    unsafe_allow_html=True)
        rows_ops = []
        for an in range(1, 6):
            s, e = (an-1)*12, an*12
            rows_ops.append({
                "Année":               f"An {an} · {2026+an}",
                "MAU fin an":          f"{m['central'][f'an{an}']:,}",
                "Commandes totales":   f"{sum(cmd_m[s:e]):,}",
                "Cmd/mois moy":        f"{sum(cmd_m[s:e])//12:,}",
                "Livreurs (pic)":      f"{max(n_liv_m[s:e]):,}",
                "Restaurants (fin)":   f"{n_rest_m[e-1]:,}",
            })
        st.dataframe(pd.DataFrame(rows_ops), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;
                    padding:12px 14px;margin-top:8px;font-size:0.80rem;color:{TEXT}">
          <b style="color:{BRAND}">Comment lire ce tableau :</b><br>
          <span style="color:{TEXT_DIM}">
          • <b>Livreurs (pic)</b> = nombre max nécessaire dans le mois le plus chargé de l'année.<br>
          • <b>Restaurants (fin)</b> = partenaires actifs en fin d'année selon le ratio MAU/restaurant.<br>
          • Ajuste les sliders sidebar <i>Cmd/livreur/jour</i> et <i>MAU par restaurant</i>
            pour tester différentes hypothèses opérationnelles.
          </span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 8 — GLOSSAIRE & GUIDE
# ══════════════════════════════════════════════════════════════
with tab8:
    st.markdown("<p class='ec-label'>Comprendre le Dashboard — Termes et Définitions</p>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.82rem;color:{TEXT_DIM};margin-bottom:16px">
      Ce guide explique chaque terme utilisé dans le dashboard en langage simple,
      adapté à une présentation devant un jury académique.
    </div>
    """, unsafe_allow_html=True)

    def _glossaire_card(emoji, titre, definition, exemple="", color=BRAND_MED):
        ex_html = f'<div style="margin-top:6px;background:#f0f3ff;border-radius:8px;padding:8px 12px;font-size:0.8rem;color:{BRAND}"><b>Exemple :</b> {exemple}</div>' if exemple else ""
        return f"""
        <div class="ec-card" style="margin-bottom:10px">
          <div style="display:flex;align-items:flex-start;gap:14px">
            <div style="font-size:1.6rem;flex-shrink:0">{emoji}</div>
            <div style="flex:1">
              <div style="font-size:0.9rem;font-weight:700;color:{color};margin-bottom:5px">{titre}</div>
              <div style="font-size:0.84rem;color:{TEXT};line-height:1.7">{definition}</div>
              {ex_html}
            </div>
          </div>
        </div>
        """

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("<p class='ec-label'>Indicateurs Financiers</p>",
                    unsafe_allow_html=True)
        st.markdown(_glossaire_card(
            "💰", "VAN — Valeur Actuelle Nette",
            "C'est le gain total du projet en euros d'aujourd'hui, après avoir retiré l'investissement de départ. "
            "Une VAN positive = le projet rapporte plus qu'il ne coûte. "
            "On utilise un taux de 15% pour tenir compte du fait qu'1 000 FCFA aujourd'hui vaut plus que 1 000 FCFA dans 5 ans.",
            f"VAN = {fin['van_M']:.1f}M FCFA → le projet crée {fin['van_M']:.1f}M de valeur nette en 5 ans.",
            BRAND
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "📈", "TRI — Taux de Rentabilité Interne",
            "C'est le taux de rendement annuel que rapporte le projet. "
            "Plus il est élevé, plus le projet est rentable. "
            "Un TRI supérieur au taux bancaire (≈ 9%) signifie qu'il vaut mieux investir dans ce projet que de mettre l'argent en banque.",
            f"TRI = {tri_val:.0f}% vs 9% bancaire → le projet est {tri_val/9:.1f}x plus rentable que la banque.",
            PURPLE
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "✖️", "IP — Indice de Profitabilité",
            "C'est le rapport entre ce que le projet rapporte et ce qu'il coûte. "
            "Un IP de 2 signifie que chaque franc investi en rapporte 2. "
            "Au-dessus de 1 = projet rentable.",
            f"IP = {fin['ip']:.2f}x → chaque franc investi rapporte {fin['ip']:.2f} FCFA.",
            TEAL2
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "⏱️", f"Break-even (Délai de Récupération)",
            "C'est le moment où les revenus cumulés dépassent l'investissement initial. "
            "Avant ce mois, le projet est encore en déficit cumulé. Après, il est bénéficiaire.",
            f"Break-even au mois {fin['delai_mois'] or '?'} ({(2026 + fin['delai_mois']//12) if fin['delai_mois'] else 'N/A'}) — l'investissement de {fin['budget_fcfa']/1e6:.2f}M FCFA est récupéré.",
            GREEN
        ), unsafe_allow_html=True)

    with col_g2:
        st.markdown("<p class='ec-label'>Modèle & Statistiques</p>",
                    unsafe_allow_html=True)
        st.markdown(_glossaire_card(
            "👥", "MAU — Monthly Active Users",
            "Le nombre d'utilisateurs actifs chaque mois sur la plateforme. "
            "C'est l'indicateur principal de croissance d'une startup numérique. "
            "Un utilisateur est 'actif' s'il a passé au moins une commande dans le mois.",
            f"MAU An 1 = {m['central']['an1']:,} · MAU An 5 plateau = {mau_L:,}",
            BRAND_MED
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "📉", "Courbe S (Logistique)",
            "Le modèle de croissance utilisé. Une startup grandit lentement au début (adoption), "
            "puis très vite (viralité), puis ralentit quand le marché est saturé. "
            "Cette courbe en forme de S est la plus réaliste pour les plateformes numériques.",
            "Paramètre k = vitesse · t0 = point d'inflexion (accélération max) · L = plateau maximum.",
            ORANGE
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "🎲", "Monte Carlo",
            "Une technique statistique qui simule des centaines ou milliers de scénarios possibles "
            "en faisant varier les paramètres au hasard (panier moyen, nombre de commandes, etc.). "
            "Le résultat montre la fourchette de résultats possibles avec leur probabilité.",
            f"Sur {mc['n_simulations'] if mc else n_mc} simulations, {mc['van']['pct_positive']:.0f}% donnent une VAN positive." if mc else "Lance Monte Carlo pour voir les résultats.",
            CYAN
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "📊", "P10 / P50 / P90",
            "Ce sont des percentiles issus du Monte Carlo. "
            "<b>P10</b> = résultat dépassé dans 90% des simulations (cas pessimiste). "
            "<b>P50</b> = résultat médian, 50% au-dessus, 50% en dessous. "
            "<b>P90</b> = résultat atteint dans seulement 10% des cas (cas optimiste).",
            f"CA An5 : P10={mc['ca5']['p10']/1e6:.0f}M · P50={mc['ca5']['p50']/1e6:.0f}M · P90={mc['ca5']['p90']/1e6:.0f}M FCFA" if mc else "",
            GOLD
        ), unsafe_allow_html=True)

    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    col_g3, col_g4 = st.columns(2)

    with col_g3:
        st.markdown("<p class='ec-label'>Données & Hypothèses</p>",
                    unsafe_allow_html=True)
        st.markdown(_glossaire_card(
            "🌍", "Facteur Dakar 0.238",
            "Le marché de Dakar est plus petit que Lagos (Nigeria). "
            "Pour calibrer le modèle, on multiplie les benchmarks Chowdeck Nigeria "
            "par 0.238, calculé selon : population Dakar / population Lagos × pouvoir d'achat × taux de pénétration mobile.",
            "Chowdeck Lagos : 2M MAU × 0.238 = ~476K MAU pour Dakar au même stade.",
            TEAL
        ), unsafe_allow_html=True)

        st.markdown(_glossaire_card(
            "🌪️", "Analyse Tornado",
            "Un graphique qui montre quels paramètres ont le plus d'impact sur le résultat. "
            "Le paramètre en haut est le 'levier' le plus puissant : le faire varier de ±10% "
            "change le résultat final plus que n'importe quel autre paramètre.",
            "Si 'Panier moyen' est en tête → augmenter le panier moyen est la priorité stratégique n°1.",
            PINK
        ), unsafe_allow_html=True)

    with col_g4:
        st.markdown("<p class='ec-label'>Flux de Revenus</p>",
                    unsafe_allow_html=True)
        rev_cards = [
            ("① Frais livraison (40% marge)", f"Frais payés par le client pour la livraison. E-cantine garde {marge_liv}% de marge."),
            ("② Commission restaurant (1–2,5%)", "Pourcentage prélevé sur chaque commande passée via la plateforme."),
            ("③ Abonnements restaurants", "Formule Pro (25K/mois) ou Premium (50K/mois) pour les restaurants partenaires."),
            ("④ Publicité in-app", "Les restaurants ou marques paient pour être mis en avant dans l'application."),
            ("⑤ B2B entreprises", "Contrats avec des entreprises pour livrer des repas à leurs employés (ex. déjeuners)."),
            ("⑥ E-cantine Vitrine (5%)", "Commission 5% sur les commandes passées via le menu 'E-cantine Vitrine' (menus prix fixe mis en avant)."),
            ("⑦ Livraisons propres (1,5%)", "Livraisons effectuées par les propres livreurs E-cantine, marge supplémentaire."),
        ]
        for titre, desc in rev_cards:
            st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:6px;
                        background:#f8f9ff;border-radius:10px;padding:8px 12px;border:1px solid {BORDER}">
              <div style="font-size:0.82rem;color:{TEXT};line-height:1.6;flex:1">
                <b style="color:{BRAND_MED}">{titre}</b><br>
                <span style="color:{TEXT_DIM}">{desc}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 9 — À PROPOS DU MODÈLE
# ══════════════════════════════════════════════════════════════
with tab9:

    # ── Intro ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="ec-card-accent" style="margin-bottom:18px">
      <div style="font-size:1.1rem;font-weight:800;color:{BRAND};margin-bottom:8px">
        🗺️ Pourquoi ce dashboard existe — et comment l'utiliser
      </div>
      <div class="t-body">
        Ce tableau de bord est l'outil central du Business Plan de <b>E-Cantine</b>,
        une startup de livraison de repas à Dakar. Il remplace les tableaux Excel statiques
        par un <b>modèle prédictif interactif</b> : chaque paramètre de la sidebar
        recalcule instantanément toutes les projections.<br><br>
        <b style="color:{BRAND_MED}">À qui s'adresse ce dashboard ?</b><br>
        — Au <b>jury académique</b> (ISM Dakar) pour valider la rigueur du BP<br>
        — Aux <b>investisseurs potentiels</b> pour tester la robustesse des projections<br>
        — À l'<b>équipe fondatrice</b> pour piloter les décisions stratégiques
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        # ── Ce que le modèle fait ──────────────────────────────
        st.markdown(f"<div class='h-section'>🔧 Ce que le modèle calcule</div>",
                    unsafe_allow_html=True)
        items_model = [
            ("📈 Croissance MAU sur 60 mois",
             "Le modèle simule le nombre d'utilisateurs actifs chaque mois avec une "
             "<b>courbe S logistique</b> — le standard des plateformes numériques. "
             "Elle intègre une phase lente d'adoption, une phase rapide de viralité, "
             "puis une stabilisation au plateau du marché."),
            ("💰 Chiffre d'affaires multi-flux",
             "Le CA est décomposé en <b>7 flux indépendants</b> : frais de livraison, "
             "commissions restaurants, abonnements Pro/Premium, publicité in-app, "
             "contrats B2B, sélection du jour, livraisons propres. Chaque flux a sa "
             "propre logique de calcul liée aux MAU."),
            ("💸 Structure de coûts réaliste",
             "4 postes de charges modélisés mois par mois : <b>Salaires</b> (équipe), "
             "<b>Marketing</b> (acquisition client), <b>Tech/Infra</b> (hébergement, développement), "
             "<b>Opérations</b> (logistique, support). Les coûts croissent avec le volume "
             "mais moins vite que les revenus — effet d'échelle."),
            ("📊 Indicateurs financiers (VAN, TRI, IP)",
             "À partir des flux nets mensuels, le modèle calcule automatiquement la "
             "<b>Valeur Actuelle Nette</b> (gain total actualisé à 15%), le "
             "<b>Taux de Rentabilité Interne</b> (rendement annuel du projet), "
             "l'<b>Indice de Profitabilité</b> (rapport gain/investissement), "
             "et le <b>délai de récupération</b> de l'investissement."),
            ("🎲 Monte Carlo (incertitude)",
             "Le modèle lance N simulations en faisant varier aléatoirement ±20-30% "
             "tous les paramètres clés. Résultat : une <b>distribution de probabilités</b> "
             "des résultats possibles — pas juste une valeur centrale, mais une fourchette "
             "P10–P90 qui montre la robustesse des projections."),
            ("🌪️ Analyse de sensibilité Tornado",
             "Identifie les <b>paramètres les plus critiques</b> : quelle variable, "
             "si elle varie de ±10%, change le plus le CA An 3 ? "
             "Résultat direct : les leviers prioritaires de l'équipe fondatrice."),
        ]
        for titre, desc in items_model:
            st.markdown(f"""
            <div style="background:{GREY_BG};border:1px solid {BORDER};border-left:3px solid {BRAND_MED};
                        border-radius:10px;padding:10px 14px;margin-bottom:8px">
              <div style="font-size:0.84rem;font-weight:700;color:{BRAND};margin-bottom:4px">{titre}</div>
              <div style="font-size:0.81rem;color:{TEXT};line-height:1.65">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_a2:
        # ── Rôle de chaque onglet ──────────────────────────────
        st.markdown(f"<div class='h-section'>📑 Rôle de chaque onglet</div>",
                    unsafe_allow_html=True)
        onglets = [
            ("📊", "Vue d'ensemble",
             "Tableau de bord synthétique : courbe de croissance MAU, CA annuel 3 scénarios, "
             "tableau récapitulatif 5 ans, et 4 KPI financiers centraux. "
             "<b>Usage : première slide à montrer au jury.</b>"),
            ("💰", "Revenus & Coûts",
             "Graphique revenus vs coûts mensuels avec point de break-even visuellement marqué, "
             "répartition des 7 flux par donut chart, cash flow cumulatif, "
             "décomposition des coûts An 1 et évolution du CA sur 5 ans. "
             "<b>Usage : démontrer la viabilité économique.</b>"),
            ("🌍", "Données Terrain",
             "Visualisation des données primaires collectées : 20 clients, 23 livreurs, "
             "5 restaurants — indicateurs clés (% intéressés, % Wave), freins identifiés, "
             "tableau des concurrents. "
             "<b>Usage : ancrer les projections dans la réalité du marché dakarois.</b>"),
            ("🔀", "Scénarios",
             "Comparaison côte-à-côte des 3 scénarios (pessimiste / central / optimiste) "
             "sur MAU et CA, tableau détaillé par année, décomposition des 7 flux An 1. "
             "<b>Usage : montrer la robustesse même dans le pire cas.</b>"),
            ("🎲", "Monte Carlo",
             "Distribution statistique du CA An 5 et de la VAN sur N simulations, "
             "KPIs P10/P50/P90, interprétation automatique du verdict, "
             "analyse tornado des leviers. "
             "<b>Usage : argument de rigueur méthodologique pour le jury.</b>"),
            ("💸", "Charges & Trésorerie",
             "Aires empilées des 4 postes de coûts mensuels, évolution de la marge nette, "
             "plan de trésorerie cumulatif avec axe double (tréso + profit mensuel), "
             "tableau annuel détaillé charges vs CA. "
             "<b>Usage : rassurer sur la gestion des coûts et la liquidité.</b>"),
            ("📖", "Glossaire & Guide",
             "Définitions simples de tous les termes financiers et statistiques utilisés "
             "(VAN, TRI, MAU, Monte Carlo, P10/P90, Facteur Dakar, Tornado…). "
             "<b>Usage : rendre le dashboard accessible à tout jury, même non-financier.</b>"),
            ("🗺️", "À propos du Modèle",
             "Ce que vous lisez maintenant — architecture complète du modèle, "
             "sources de données, hypothèses clés, calibration sur les benchmarks africains, "
             "limites et voies d'amélioration. "
             "<b>Usage : transparence méthodologique pour les évaluateurs.</b>"),
        ]
        for ico, titre, desc in onglets:
            st.markdown(f"""
            <div style="background:{WHITE};border:1px solid {BORDER};
                        border-radius:10px;padding:10px 14px;margin-bottom:7px;
                        box-shadow:0 1px 6px rgba(4,12,136,0.05)">
              <div style="font-size:0.84rem;font-weight:700;color:{BRAND};margin-bottom:3px">
                {ico} {titre}</div>
              <div style="font-size:0.80rem;color:{TEXT};line-height:1.6">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Méthodologie & calibration ──────────────────────────────
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns([3, 2])

    with col_b1:
        st.markdown(f"<div class='h-section'>🔬 Méthodologie & Sources</div>",
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ec-card">
          <div class="t-body">
            <b style="color:{BRAND}">Modèle de croissance :</b> Courbe logistique de Bass
            (S-curve) — utilisée par Uber, Jumia, Chowdeck pour modéliser l'adoption d'une
            plateforme dans un nouveau marché.<br><br>
            <b style="color:{BRAND}">Calibration :</b>
            Les paramètres de plateau (L) et de vitesse (k) sont calibrés sur
            <b>Chowdeck Nigeria (Lagos)</b> — la plateforme africaine de référence la plus
            comparable, ajustée par le <b>Facteur Dakar 0.238</b>.<br><br>
            <b style="color:{BRAND}">Facteur Dakar 0.238 =</b>
            <span style="color:{TEXT_DIM}">
              population Dakar (3,7M) / population Lagos (15,6M)
              × ratio PIB/habitant Sénégal/Nigeria (0.62)
              × ratio pénétration mobile (0.87)
            </span><br><br>
            <b style="color:{BRAND}">Données terrain :</b>
            {terr.get('clients', {}).get('n_repondants', 20)} clients (questionnaire),
            {terr.get('livreurs', {}).get('n_entretiens', 23)} livreurs (entretiens),
            {terr.get('restaurants', {}).get('n_discussions', 5)} restaurants (discussions).
            Panel exploratoire (100 réseau de connaissance) — objectif <b>1 000 répondants</b> via formulaire in-app (fin An 1 commercial).<br><br>
            <b style="color:{BRAND}">Taux d'actualisation :</b>
            15% — coût du capital estimé dans le contexte UEMOA/ISM Dakar
            (supérieur au taux bancaire BCAO ≈ 9% + prime de risque startup ≈ 6%).
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown(f"<div class='h-section'>⚠️ Hypothèses clés</div>",
                    unsafe_allow_html=True)
        hypos = [
            ("Panier moyen", f"{params['avg_basket']:,} FCFA", "Modifiable sidebar"),
            ("Commandes/MAU/mois", f"{params['avg_cmd_par_mau']:.1f}", "Modifiable sidebar"),
            ("Marge livraison", f"{params['marge_livraison']*100:.0f}%", "Modifiable sidebar"),
            ("MAU plateau", f"{params['mau_L']:,}", "Modifiable sidebar"),
            ("Taux croissance k", f"{params['mau_k']:.2f}", "Modifiable sidebar"),
            ("Investissement initial", f"{fin['budget_fcfa']/1e6:.2f}M FCFA", "Fixe modèle"),
            ("Durée projection", "60 mois (5 ans)", "Standard BP"),
            ("Facteur Dakar", "0.238", "Calculé terrain"),
        ]
        for label, valeur, note in hypos:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:7px 12px;border-bottom:1px solid {BORDER};font-size:0.81rem">
              <span style="color:{TEXT};font-weight:600">{label}</span>
              <span style="color:{BRAND_MED};font-weight:700">{valeur}</span>
              <span style="color:{TEXT_DIM};font-size:0.74rem">{note}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='h-section'>🚧 Limites connues</div>",
                    unsafe_allow_html=True)
        limites = [
            "Panel exploratoire (100 réseau de connaissance) — objectif 1 000 via formulaire in-app An 1",
            "Pas encore de données réelles de transactions",
            "Facteur Dakar calculé, non validé empiriquement",
            "Modèle déterministe de coûts (pas de choc externe)",
            "Projections > 3 ans à prendre avec précaution",
        ]
        for lim in limites:
            st.markdown(f"""
            <div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:6px;
                        font-size:0.80rem;color:{TEXT}">
              <span style="color:{ORANGE};flex-shrink:0">⚠</span>
              <span>{lim}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Interactivité sidebar ──────────────────────────────────
    st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='h-section'>🎛️ Utiliser la sidebar pour tester des scénarios</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ec-card">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
        <div>
          <div class="h-subsection">Modèle Économique</div>
          <div class="t-dim">
            <b>Panier moyen :</b> valeur moyenne d'une commande — augmenter améliore toutes les marges.<br>
            <b>Commandes/MAU/mois :</b> fréquence d'achat — clé pour le CA total.<br>
            <b>Frais livraison :</b> prix affiché au client pour la livraison.<br>
            <b>Marge livraison :</b> la part que E-cantine conserve sur ces frais.
          </div>
        </div>
        <div>
          <div class="h-subsection">Formules Restaurants</div>
          <div class="t-dim">
            <b>% Starter (gratuit) :</b> restaurants sans abonnement — E-cantine ne prend que la commission.<br>
            <b>% Pro (25K/mois) :</b> restaurants payant un abonnement mensuel.<br>
            <b>% Premium (50K/mois) :</b> calculé automatiquement = 100% - Starter - Pro.
          </div>
        </div>
        <div>
          <div class="h-subsection">Croissance MAU</div>
          <div class="t-dim">
            <b>MAU plateau :</b> le maximum d'utilisateurs actifs que le marché dakarois peut absorber.<br>
            <b>Vitesse k :</b> à 0.10 = croissance modérée (réaliste). À 0.20 = croissance agressive.
          </div>
        </div>
        <div>
          <div class="h-subsection">Monte Carlo</div>
          <div class="t-dim">
            <b>Simulations :</b> 200 = rapide (aperçu), 1000+ = résultats statistiquement fiables.<br>
            Cliquer sur <b>▶ Lancer Monte Carlo</b> pour générer les distributions de probabilités.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("<div class='ec-divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            flex-wrap:wrap;gap:10px;padding:8px 4px 14px">
  <div>{logo_img(LOGO_BLUE_B64, width="80px", extra="opacity:0.65;")}</div>
  <div style="text-align:center">
    <div style="color:{TEXT_DIM};font-size:0.72rem;font-weight:500">
      <b style="color:{BRAND};font-weight:700">E-Cantine · Business Plan</b>
      &nbsp;·&nbsp; ISM Dakar &nbsp;·&nbsp; 2025
    </div>
    <div style="color:{TEXT_DIM};font-size:0.70rem;margin-top:2px">
      Adote Mario-Giovani ADUAYI-AKUE
    </div>
  </div>
  <div style="font-size:0.70rem;color:{TEXT_DIM};text-align:right;line-height:1.5">
    Modèle IA · Courbe S logistique<br>
    Benchmarks Africains × Facteur Dakar
  </div>
</div>
""", unsafe_allow_html=True)
