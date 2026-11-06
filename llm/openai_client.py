"""Cliente de la capa LLM. Habla con la API Responses de OpenAI."""

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    OpenAIError,
)


class LLMClientError(Exception):
    """Error de configuración o de comunicación con el modelo."""


def _load_openai_settings():
    """Lee la clave y el modelo desde config.settings, sin valores fijos."""
    try:
        from config import settings
    except ImportError as exc:
        raise LLMClientError(
            "No se pudo cargar config/settings.py. "
            "Esa capa debe definir OPENAI_API_KEY y OPENAI_MODEL."
        ) from exc

    api_key = getattr(settings, "OPENAI_API_KEY", None)
    model = getattr(settings, "OPENAI_MODEL", None)

    api_key = str(api_key).strip() if api_key else ""
    model = str(model).strip() if model else ""

    if not api_key:
        raise LLMClientError(
            "Falta OPENAI_API_KEY. Cópiala en el archivo .env; "
            "no la escribas en el código."
        )
    if not model:
        raise LLMClientError(
            "Falta OPENAI_MODEL. Define el modelo en el archivo .env."
        )

    return api_key, model


def generate_response(message, instructions):
    """Envía un mensaje a la API Responses y devuelve el texto generado.

    Args:
        message: Texto del usuario que se envía como input.
        instructions: Instrucciones del sistema para el modelo.

    Returns:
        Texto generado por el modelo.

    Raises:
        LLMClientError: Si falta configuración o falla la conexión con OpenAI.
    """
    if message is None or not str(message).strip():
        raise LLMClientError("El mensaje no puede estar vacío.")

    if instructions is None:
        instructions = ""

    api_key, model = _load_openai_settings()

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=str(instructions),
            input=str(message),
        )
    except (APIConnectionError, APITimeoutError) as exc:
        raise LLMClientError(
            "No se pudo conectar con la API de OpenAI. "
            "Comprueba la conexión e inténtalo de nuevo."
        ) from exc
    except AuthenticationError as exc:
        raise LLMClientError(
            "OpenAI ha rechazado la clave API. Revisa OPENAI_API_KEY en .env."
        ) from exc
    except OpenAIError as exc:
        raise LLMClientError(
            "OpenAI no pudo generar la respuesta. "
            "Revisa OPENAI_MODEL y la configuración del cliente."
        ) from exc

    text = getattr(response, "output_text", None)
    if text is None or not str(text).strip():
        raise LLMClientError(
            "El modelo respondió, pero no devolvió texto utilizable."
        )

    return str(text).strip()
