"""
E-CANTINE — NOTE METHODOLOGIQUE OFFICIELLE
Integree dans predict.py et le BP.
"""

METHODOLOGIE = {
    "clients": {
        "n_repondants":   100,
        "objectif_cible": 1_000,
        "type_collecte":  "Réseau de connaissance — bouche-à-oreille",
        "profil": (
            "Personnes de l'entourage direct et élargi du fondateur, "
            "sélectionnées sur un critère unique : commander régulièrement "
            "des repas à l'extérieur ou via des applications à Dakar."
        ),
        "zone":    "Dakar — plusieurs quartiers (réseau élargi)",
        "periode": "2024",
        "methode_cible": (
            "Formulaire intégré in-app E-cantine — proposé à chaque nouveau "
            "client lors de sa 1ère commande. Objectif atteint avant fin An 1 "
            "commercial (déc. 2027)."
        ),
        "statistique_cible": "Intervalle de confiance 95% — marge d'erreur 3,1%",
        "formulation_bp": (
            "100 personnes ont été interrogées dans le réseau de connaissance "
            "du fondateur et de son entourage élargi à Dakar — toutes sélectionnées "
            "sur un critère simple : commander régulièrement des repas à l'extérieur "
            "ou via des applications. Ces entretiens constituent une base primaire "
            "exploratoire conduite avant le lancement du modèle de prédiction IA. "
            "Les résultats sont traités comme des indicateurs directionnels et non "
            "comme un échantillon statistiquement représentatif. "
            "L'objectif est d'atteindre 1 000 répondants avant la fin de l'Année 1 "
            "commerciale (décembre 2027) via le formulaire intégré à l'application "
            "E-cantine, garantissant un intervalle de confiance de 95% avec une "
            "marge d'erreur de 3,1%."
        ),
    },
    "livreurs": {
        "n_entretiens": 23,
        "type_collecte": "Entretiens semi-directifs terrain",
        "sources": [
            "Moaye (5 livreurs)",
            "Swice Palace (4 livreurs)",
            "Bazof (4 livreurs)",
            "Yum Yum (4 livreurs)",
            "Livreurs de colis indépendants (6)",
        ],
        "zone":    "Dakar — plusieurs quartiers",
        "periode": "2024",
        "formulation_bp": (
            "23 entretiens semi-directifs ont été conduits directement sur le terrain "
            "à Dakar auprès de livreurs actifs issus de restaurants reconnus : "
            "Moaye (5), Swice Palace (4), Bazof (4), Yum Yum (4) "
            "et des livreurs de colis indépendants (6). "
            "Ces échanges qualitatifs documentent les habitudes, revenus, "
            "contraintes et attentes de cette population."
        ),
    },
    "restaurants": {
        "n_discussions": 8,
        "type_collecte": "Discussions directes avec responsables / gérants",
        "etablissements": [
            "4 restaurants à cuisine internationale (anonymisés)",
            "Swice Palace",
            "Trophet",
            "Chez Mervi",
            "Chez Maman Gaga",
        ],
        "zone":    "Dakar",
        "periode": "2024",
        "formulation_bp": (
            "8 établissements ont été approchés via des discussions directes "
            "avec leurs responsables ou gérants : 4 restaurants à cuisine "
            "internationale et 4 restaurants sénégalais dont Swice Palace, "
            "Trophet, Chez Mervi et Chez Maman Gaga. "
            "100% gèrent leurs commandes via WhatsApp ou téléphone, et "
            "100% ont exprimé un intérêt immédiat pour la formule Starter gratuite."
        ),
    },
    "modele_prediction": {
        "methode":       "Courbe S logistique (modèle de diffusion de l'innovation)",
        "calibration":   "Chowdeck Nigeria × Facteur Dakar 0,238",
        "facteur_dakar": 0.238,
        "simulation":    "Monte Carlo 1 000 itérations",
        "parametres":    {"mau_L": 60_000, "mau_k": 0.07, "mau_t0": 44},
        "dashboard_url": "https://ecantine-dash.streamlit.app/",
        "github_url":    "https://github.com/magi22/ecantine-dashboard",
        "date_generation": "Avril 2026",
        "statut":        "Estimations académiques — à affiner avec données réelles",
        "formulation_bp": (
            "Face à la nature exploratoire de l'enquête terrain "
            "(100 entretiens réseau de connaissance, 23 entretiens livreurs, "
            "8 discussions restaurants), les projections financières ont été "
            "produites par un modèle de prédiction statistique en trois étapes : "
            "(1) Courbe S logistique calibrée sur Chowdeck Nigeria × Facteur Dakar 0,238 ; "
            "(2) Projection des 6 flux de revenus nets sur 60 mois ; "
            "(3) Simulation Monte Carlo sur 1 000 itérations. "
            "Dashboard interactif : https://ecantine-dash.streamlit.app/ — "
            "Code source : https://github.com/magi22/ecantine-dashboard."
        ),
    },
    "frais_bceao": {
        "taux":       0.01,
        "plafond":    5_000,
        "nature":     "Réglementaire BCEAO — zone UEMOA",
        "operateurs": ["Wave", "Orange Money", "Mix by Yass", "Autres EME"],
        "beneficiaire": "Opérateur concerné — PAS E-cantine",
        "affichage_app": (
            "Frais réglementaires BCEAO : 1% — reversés à votre opérateur "
            "(Wave / Orange Money / Mix by Yass)."
        ),
        "formulation_bp": (
            "Les frais de paiement électronique de 1% (maximum 5 000 FCFA par "
            "transaction) sont réglementaires — imposés par la BCEAO à tous les "
            "opérateurs de monnaie électronique actifs en zone UEMOA : Wave, "
            "Orange Money, Mix by Yass et tout autre EME. Ils sont affichés au "
            "client avant validation et reversés intégralement à l'opérateur "
            "concerné. Ils ne constituent pas un revenu E-cantine."
        ),
    },
    "concurrents": {
        "glovo":      "Jamais officiellement lancé au Sénégal (Wikipedia + glovoapp.com)",
        "jumia_food": "Fermé décembre 2023 — 7 pays dont Sénégal (TechCabal 14/12/2023)",
        "chowdeck":   "Benchmark calibration uniquement — Nigeria, hors Sénégal",
        "yassir":     "Concurrent le plus capitalisé : $150M levés Série B nov. 2022",
        "actifs_dakar": [
            "DFD", "Yassir", "Yango Food", "Ayda App",
            "Bring Me SN", "KonectFood", "Wajeez", "Togalma",
        ],
    },
    "preuve_concept_v0": {
        "commandes_totales":  34,
        "commandes_livrees":  25,
        "premier_livreur":    "Tito Gbedjeha",
        "premier_restaurant": "TCHOP MASTER (4 commandes)",
        "plats_valides":      ["Choukouya de Porc", "ALLOCO", "Attiéké"],
        "stack":              "PHP/Laravel admin + React.js client + iOS/Android",
    },
}


def get_note_methodologique():
    return {
        "clients":     METHODOLOGIE["clients"]["formulation_bp"],
        "livreurs":    METHODOLOGIE["livreurs"]["formulation_bp"],
        "restaurants": METHODOLOGIE["restaurants"]["formulation_bp"],
        "modele":      METHODOLOGIE["modele_prediction"]["formulation_bp"],
        "bceao":       METHODOLOGIE["frais_bceao"]["formulation_bp"],
        "dashboard":   METHODOLOGIE["modele_prediction"]["dashboard_url"],
        "github":      METHODOLOGIE["modele_prediction"]["github_url"],
    }
