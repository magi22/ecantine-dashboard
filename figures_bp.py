"""
E-CANTINE — Génération des figures pour le Business Plan
Exporte 14 graphiques PNG à insérer dans le document Word/PDF.
Usage : python figures_bp.py
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import matplotlib.pyplot as plt
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "outputs", "figures")
os.makedirs(OUT, exist_ok=True)

# Couleurs brand E-cantine
BLUE  = "#040c88"
GREEN = "#2e7d32"

def save(name):
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ {name}")

print("\nGénération des figures BP — E-cantine (n=100 clients · 23 livreurs · 8 restaurants)\n")

# ── Figure 1 — Tranches d'âge
fig, ax = plt.subplots(figsize=(8, 5))
ages = ["18–24 ans", "25–34 ans", "35–44 ans"]
vals = [65, 26, 9]
bars = ax.barh(ages, vals, color=[BLUE, "#1565c0", "#42a5f5"])
for bar, val in zip(bars, vals):
    ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
            f"{val}%", va='center', fontweight='bold')
ax.set_xlabel("% des répondants")
ax.set_title("Tranches d'âge des répondants — Enquête clients (n=100)", fontweight='bold')
ax.set_xlim(0, 80)
ax.axvline(x=50, color='gray', linestyle='--', alpha=0.3)
plt.tight_layout()
save("fig1_ages.png")

# ── Figure 2 — Quartiers
fig, ax = plt.subplots(figsize=(8, 5))
quartiers = ["Grand Yoff", "Sacré-Cœur", "Médina", "Plateau", "Ouakam", "Almadies"]
vals = [13, 12, 12, 10, 10, 10]
colors_q = [BLUE if v == max(vals) else "#1976d2" for v in vals]
bars = ax.barh(quartiers, vals, color=colors_q)
for bar, val in zip(bars, vals):
    ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
            f"{val}", va='center', fontweight='bold')
ax.set_xlabel("Nombre de répondants")
ax.set_title("Quartiers de résidence — Enquête clients (n=100)", fontweight='bold')
plt.tight_layout()
save("fig2_quartiers.png")

# ── Figure 3 — Freins
fig, ax = plt.subplots(figsize=(8, 5))
freins = ["Délai incertain", "Doute qualité plats",
          "Préfère se déplacer", "Manque confiance app",
          "Aucun frein", "Prix trop élevé"]
vals = [41, 20, 12, 11, 10, 6]
colors_f = [BLUE if v == max(vals) else "#1565c0" if v > 15 else "#42a5f5" for v in vals]
bars = ax.barh(freins, vals, color=colors_f)
for bar, val in zip(bars, vals):
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
            f"{val}%", va='center', fontweight='bold')
ax.set_xlabel("% des répondants")
ax.set_title("Freins principaux à la commande en ligne (n=100)", fontweight='bold')
ax.axvline(x=41, color='red', linestyle='--', alpha=0.4, label="Frein dominant")
plt.tight_layout()
save("fig3_freins.png")

# ── Figure 4 — Fonctionnalités souhaitées
fig, ax = plt.subplots(figsize=(8, 5))
fonctions = ["Paiement Wave/OM", "Rapidité < 35min",
             "Suivi GPS temps réel", "Commande groupée",
             "Cuisine africaine locale"]
vals = [33, 23, 19, 16, 9]
bars = ax.barh(fonctions, vals, color=[BLUE, BLUE, "#1565c0", "#1976d2", "#42a5f5"])
for bar, val in zip(bars, vals):
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
            f"{val}%", va='center', fontweight='bold')
ax.set_xlabel("% des répondants")
ax.set_title("Fonctionnalités prioritaires souhaitées (n=100)", fontweight='bold')
plt.tight_layout()
save("fig4_fonctions.png")

# ── Figure 5 — Prix livraison acceptable
fig, ax = plt.subplots(figsize=(7, 5))
labels = ["500–1 000 FCFA", "1 000–1 500 FCFA", "1 500–2 500 FCFA"]
vals = [56, 33, 11]
colors_p = [GREEN, "#1565c0", "#90caf9"]
wedges, texts, autotexts = ax.pie(vals, labels=labels, colors=colors_p,
                                   autopct='%1.0f%%', startangle=90,
                                   textprops={'fontsize': 11})
for at in autotexts:
    at.set_fontweight('bold')
ax.set_title("Prix de livraison acceptable selon les clients (n=100)",
             fontweight='bold', pad=15)
plt.tight_layout()
save("fig5_prix.png")

# ── Figure 6 — Intérêt E-cantine
fig, ax = plt.subplots(figsize=(7, 5))
labels = ["Très intéressé", "Intéressé"]
vals = [82, 18]
colors_i = [GREEN, "#66bb6a"]
wedges, texts, autotexts = ax.pie(vals, labels=labels, colors=colors_i,
                                   autopct='%1.0f%%', startangle=90,
                                   textprops={'fontsize': 12})
for at in autotexts:
    at.set_fontweight('bold')
    at.set_fontsize(14)
ax.set_title("Niveau d'intérêt pour E-cantine (n=100 · 100% intéressés)",
             fontweight='bold', pad=15)
plt.tight_layout()
save("fig6_interet.png")

# ── Figure 7 — Transport livreurs
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Moto personnelle", "Autre"]
vals = [95.7, 4.3]
bars = ax.bar(labels, vals, color=[BLUE, "#90caf9"], width=0.4)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val}%", ha='center', fontweight='bold', fontsize=13)
ax.set_ylabel("% des livreurs interrogés")
ax.set_title("Moyen de transport — Livreurs (n=23)", fontweight='bold')
ax.set_ylim(0, 110)
plt.tight_layout()
save("fig7_transport.png")

# ── Figure 8 — Zones livreurs
fig, ax = plt.subplots(figsize=(8, 5))
zones = ["Médina", "Sacré-Cœur", "Plateau", "Almadies",
         "Grand Yoff", "Ouakam", "Pikine", "Point E"]
vals = [9, 8, 5, 5, 5, 4, 3, 3]
bars = ax.barh(zones, vals,
               color=[BLUE if v >= 8 else "#1976d2" if v >= 5 else "#90caf9" for v in vals])
for bar, val in zip(bars, vals):
    ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
            str(val), va='center', fontweight='bold')
ax.set_xlabel("Nombre de livreurs")
ax.set_title("Zones de résidence des livreurs interrogés (n=23)", fontweight='bold')
plt.tight_layout()
save("fig8_zones_livreurs.png")

# ── Figure 9 — Sources entretiens livreurs
fig, ax = plt.subplots(figsize=(7, 5))
sources = ["Indépendants\ncolis", "Moaye", "Swice Palace", "Bazof", "Yum Yum"]
vals = [6, 5, 4, 4, 4]
bars = ax.bar(sources, vals, color=[BLUE, "#1565c0", "#1976d2", "#42a5f5", "#90caf9"])
for bar, val in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
            str(val), ha='center', fontweight='bold', fontsize=12)
ax.set_ylabel("Nombre d'entretiens")
ax.set_title("Sources des entretiens livreurs (n=23)", fontweight='bold')
ax.set_ylim(0, 8)
plt.tight_layout()
save("fig9_sources_livreurs.png")

# ── Figure 10 — Préférence rémunération livreurs
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Base fixe + bonus\n(modèle hybride)", "Paiement à la\ncourse uniquement"]
vals = [69.6, 30.4]
bars = ax.bar(labels, vals, color=[GREEN, "#90caf9"], width=0.4)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val}%", ha='center', fontweight='bold', fontsize=13)
ax.set_ylabel("% des livreurs")
ax.set_title("Préférence de rémunération — Livreurs (n=23)", fontweight='bold')
ax.set_ylim(0, 85)
plt.tight_layout()
save("fig10_remuneration.png")

# ── Figure 11 — Wave livreurs
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Compte Wave actif", "Peuvent créer\nun compte"]
vals = [87, 13]
bars = ax.bar(labels, vals, color=[GREEN, "#66bb6a"], width=0.4)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val}%", ha='center', fontweight='bold', fontsize=13)
ax.set_ylabel("% des livreurs")
ax.set_title("Compte Wave actif — Livreurs (n=23)", fontweight='bold')
ax.set_ylim(0, 105)
ax.text(0.5, 0.97, "→ 100% compatibles avec le paiement Wave E-cantine",
        ha='center', fontsize=9, fontstyle='italic', color='gray',
        transform=ax.transAxes)
plt.tight_layout()
save("fig11_wave_livreurs.png")

# ── Figure 12 — Gestion restaurants
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["WhatsApp + Téléphone", "Outil numérique"]
vals = [100, 0]
bars = ax.bar(labels, vals, color=[BLUE, "#90caf9"], width=0.4)
ax.text(bars[0].get_x()+bars[0].get_width()/2, vals[0]+1,
        "100%", ha='center', fontweight='bold', fontsize=16, color=BLUE)
ax.text(bars[1].get_x()+bars[1].get_width()/2, 3,
        "0%", ha='center', fontweight='bold', fontsize=16, color='gray')
ax.set_ylabel("% des restaurants")
ax.set_title("Mode de gestion des commandes — Restaurants (n=8)", fontweight='bold')
ax.set_ylim(0, 115)
plt.tight_layout()
save("fig12_gestion_restaurants.png")

# ── Figure 13 — Livreurs propres restaurants
fig, ax = plt.subplots(figsize=(7, 5))
labels = ["Ont leurs propres\nlivreurs", "N'ont pas de\nlivreurs propres"]
vals = [37.5, 62.5]
wedges, texts, autotexts = ax.pie(vals, labels=labels, colors=[BLUE, "#90caf9"],
                                   autopct='%1.1f%%', startangle=90,
                                   textprops={'fontsize': 11})
for at in autotexts:
    at.set_fontweight('bold')
ax.set_title("Présence de livreurs propres — Restaurants (n=8)",
             fontweight='bold', pad=15)
plt.tight_layout()
save("fig13_livreurs_propres.png")

# ── Figure 14 — Intérêt Starter gratuit
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Intéressés par le\nStarter gratuit", "Non intéressés"]
vals = [100, 0]
bars = ax.bar(labels, vals, color=[GREEN, "#90caf9"], width=0.4)
ax.text(bars[0].get_x()+bars[0].get_width()/2, vals[0]+1,
        "100%", ha='center', fontweight='bold', fontsize=16, color=GREEN)
ax.text(bars[1].get_x()+bars[1].get_width()/2, 3,
        "0%", ha='center', fontweight='bold', fontsize=16, color='gray')
ax.set_ylabel("% des restaurants")
ax.set_title("Intérêt pour le Starter gratuit 3 mois — Restaurants (n=8)",
             fontweight='bold')
ax.set_ylim(0, 115)
plt.tight_layout()
save("fig14_starter.png")

print(f"\n✅ 14 figures exportées → {OUT}")
print("   Insérer dans Word/PDF : fig1 à fig14.png")
