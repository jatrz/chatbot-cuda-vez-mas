"""Rutas HTTP del chatbot. Esta capa no usa el SDK de OpenAI."""

from flask import Blueprint, jsonify, request

from llm.openai_client import LLMClientError
from services.chatbot_service import process_message

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _error(message, status):
    return jsonify({"error": message}), status


@api_bp.post("/chat")
def chat():
    """Recibe un mensaje y devuelve la respuesta del asistente."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error("El cuerpo de la petición debe ser un JSON.", 400)

    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        return _error("El campo message es obligatorio y no puede estar vacío.", 400)

    try:
        reply = process_message(message)
    except LLMClientError as exc:
        return _error(str(exc), 502)
    except RuntimeError as exc:
        return _error(str(exc), 500)
    except Exception:
        return _error("No se pudo procesar el mensaje.", 500)

    return jsonify({"response": reply})
