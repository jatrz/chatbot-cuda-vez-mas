"""Carga la configuración desde el archivo .env, sin mostrar secretos."""

import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "").strip() or "gpt-6-luna"

if not OPENAI_API_KEY:
    raise RuntimeError(
        "Falta OPENAI_API_KEY. Crea un archivo .env a partir de .env.example "
        "y define ahí la clave. El valor no se muestra por seguridad."
    )
