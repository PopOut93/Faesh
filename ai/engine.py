# ai/engine.py
# ============================================
# FÆSH ENGINE — FASHION / SENSEI / PRIVATE
# ============================================

import re
from difflib import get_close_matches

# --------------------------------------------
# SESSION STATE (simple, safe, per-runtime)
# --------------------------------------------
SESSION = {
    "mode": "fashion",          # fashion | sensei
    "private_unlocked": False,
    "legacy_unlocked": False,
    "jailin_verified": False
}

# --------------------------------------------
# TRIGGERS
# --------------------------------------------
SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 
