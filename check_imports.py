"""Verifica que todos los módulos carguen correctamente."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

errors = []

checks = [
    ("constants", "from services.constants import RARITY_LABELS"),
    ("game_logic", "from services.game_logic import get_progress, progress_stats"),
    ("inventory", "from services.inventory import remove_sticker_from_user, user_owns_sticker"),
    ("exchange", "from services.exchange import cancel_my_offer, accept_exchange"),
    ("share", "from services.share import get_share_content"),
    ("auth", "from services.auth import register_user"),
    ("progress_utils", "from services.progress_utils import progress_user_id"),
    ("app", "import app"),
]

for name, stmt in checks:
    try:
        exec(stmt, {"__name__": "__check__"})
        print(f"  OK  {name}")
    except Exception as exc:
        print(f"  FAIL {name}: {exc}")
        errors.append(name)

if errors:
    print(f"\n{len(errors)} error(es). Revisá los módulos anteriores.")
    sys.exit(1)
else:
    print("\nTodo correcto. Ejecutá: python -m streamlit run app.py")
