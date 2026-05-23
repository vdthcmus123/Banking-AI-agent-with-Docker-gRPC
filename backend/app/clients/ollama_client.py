"""Async HTTP client for Ollama response generation."""

import json
import logging
from typing import Dict, Any, Optional

import httpx

from app.clients.base import BaseClient

logger = logging.getLogger(__name__)


class OllamaClient(BaseClient):
    """Async client to call Ollama API for response generation."""

    def __init__(self, base_url: str, model_name: str, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )

    async def connect(self):
        """No-op: httpx client is ready on init."""
        pass

    async def generate_response(
        self,
        message: str,
        intent: str,
        priority: str,
        policy_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a banking response using the Ollama model.

        Args:
            message: Original customer message.
            intent: Classified intent.
            priority: Priority level (low/medium/high/critical).
            policy_content: Relevant banking policy text.

        Returns:
            Dict with draft_response, missing_info, and next_action.
        """
        policy_text = policy_content or "No specific policy found for this intent."

        system_prompt = f"""You are a professional banking customer service assistant.
You must generate a helpful response based on the following context:

- Customer Intent: {intent}
- Priority Level: {priority}
- Applicable Policy: {policy_text}

Your response must be in JSON format with these fields:
- "draft_response": A professional, helpful reply to the customer (2-4 sentences)
- "missing_info": Any additional information needed from the customer, or null if none
- "next_action": The recommended next step (e.g., "escalate_to_agent", "resolve_directly", "request_verification", "provide_information")

Respond ONLY with the JSON object."""

        try:
            response = await self.client.post(
                "/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0.3},
                },
            )
            response.raise_for_status()
            data = response.json()

            content = data.get("message", {}).get("content", "{}")
            result = json.loads(content)

            return {
                "draft_response": result.get(
                    "draft_response", "I apologize, I could not generate a response."
                ),
                "missing_info": result.get("missing_info"),
                "next_action": result.get("next_action", "provide_information"),
            }

        except json.JSONDecodeError as e:
            logger.error("Failed to parse Ollama response: %s", e)
            return {
                "draft_response": "I apologize for the inconvenience. Let me connect you with a specialist who can assist you better.",
                "missing_info": None,
                "next_action": "escalate_to_agent",
            }
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return {
                "draft_response": "I'm experiencing a temporary delay. Please try again in a moment.",
                "missing_info": None,
                "next_action": "retry",
            }
        except Exception as e:
            logger.error("Ollama response generation failed: %s", e)
            return {
                "draft_response": "I apologize for the technical difficulty. Please try again or contact support.",
                "missing_info": None,
                "next_action": "escalate_to_agent",
            }

    async def close(self):
        """Close the httpx client."""
        await self.client.aclose()
        logger.info("Ollama client closed")
