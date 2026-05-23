"""Intent classification node using Ollama."""

import logging

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult
from app.core.settings import get_settings

logger = logging.getLogger(__name__)


def classify(message: str) -> IntentResult:
    """Classify a customer message into a banking intent.

    Args:
        message: The customer's message to classify.

    Returns:
        IntentResult with predicted intent, confidence, and reason.
    """
    settings = get_settings()
    client = OllamaClient(
        base_url=settings.OLLAMA_BASE_URL,
        model_name=settings.INTENT_MODEL_NAME,
    )

    try:
        result = client.classify_intent(message)
        logger.info(
            "Classified intent: %s (confidence: %.2f)",
            result.intent,
            result.confidence,
        )
        return result
    except Exception as e:
        logger.error("Intent classification failed: %s", e)
        return IntentResult(
            intent="general_inquiry",
            confidence=0.0,
            reason=f"Classification failed: {str(e)}",
        )
    finally:
        client.close()
