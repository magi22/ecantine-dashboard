#!/usr/bin/env bash
# Script de sauvegarde rapide du contexte — E-Cantine

# 1. Archiver traces locales
tar -czf .memory_snapshot_$(date +%Y%m%d_%H%M%S).tar.gz \
  claude.md primer.md hindsight.md obsidian.md token_optimization.md \
  2>/dev/null || true

# 2. Vérifier état git
echo "=== Status git ==="
git status --short

echo "=== Remote URL ==="
git remote -v

echo "=== Derniers commits ==="
git log --oneline --max-count=5

# 3. Tester le modèle
echo "=== Test predict.py ==="
python predict.py 2>&1 | tail -10

# 4. Rappel des consignes critiques
cat <<'EOF'

=== CONSIGNES CRITIQUES E-CANTINE ===
- NE JAMAIS : font=dict(weight=N) dans Plotly → crash Streamlit Cloud
- NE JAMAIS : **PLOTLY sur go.Pie → utiliser PLOTLY_PIE
- NE JAMAIS : HTML <span> dans annotations Plotly
- TOUJOURS  : python predict.py avant commit
- TOUJOURS  : git push origin main après fix
- DEPLOIEMENT : share.streamlit.io → repo magi22/ecantine-dashboard → app.py
EOF
