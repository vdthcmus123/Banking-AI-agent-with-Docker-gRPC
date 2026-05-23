"""Ollama client for intent classification via LLM."""

import json
import logging
from typing import Optional

from app.clients.base import BaseHTTPClient
from app.core.schemas import IntentResult
from app.data.policies import BANKING77_INTENTS

logger = logging.getLogger(__name__)


class OllamaClient(BaseHTTPClient):
    """Client to call Ollama API for intent classification."""

    def __init__(self, base_url: str, model_name: str, timeout: float = 120.0):
        super().__init__(base_url, timeout)
        self.model_name = model_name

    def classify_intent(self, message: str) -> IntentResult:
        """Classify a customer message into a banking intent using Ollama."""
        intent_list = ", ".join(BANKING77_INTENTS)

        prompt = f"""You are a banking intent classifier. Your task is to classify the customer message into exactly one of the following banking intents:

{intent_list}

Customer message: "{message}"

You must respond with a valid JSON object containing these fields:
- "intent": the classified intent (must be exactly one from the list above)
- "confidence": a float between 0.0 and 1.0 indicating your confidence
- "reason": a brief explanation of why this intent was chosen

Respond ONLY with the JSON object, no other text."""

        try:
            response = self.post(
                "/api/chat",
                {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0},
                },
            )

            content = response.get("message", {}).get("content", "{}")
            result = json.loads(content)

            # Validate intent is in the known list
            predicted_intent = result.get("intent", "general_inquiry")
            if predicted_intent not in BANKING77_INTENTS:
                logger.warning(
                    "Unknown intent '%s', falling back to general_inquiry",
                    predicted_intent,
                )
                predicted_intent = "general_inquiry"

            return IntentResult(
                intent=predicted_intent,
                confidence=float(result.get("confidence", 0.0)),
                reason=result.get("reason", ""),
            )

        except json.JSONDecodeError as e:
            logger.error("Failed to parse Ollama response as JSON: %s", e)
            return IntentResult(
                intent="general_inquiry",
                confidence=0.0,
                reason=f"JSON parse error: {str(e)}",
            )
        except Exception as e:
            logger.error("Ollama classification failed: %s", e)
            return IntentResult(
                intent="general_inquiry",
                confidence=0.0,
                reason=f"Classification error: {str(e)}",
            )
