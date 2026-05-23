"""Orchestrator — chains workflow nodes to process customer requests."""

import logging
from typing import Any, Dict

from app.clients.grpc_intent_client import IntentGRPCClient
from app.clients.ollama_client import OllamaClient
from app.nodes import (
    intent_node,
    priority_node,
    policy_node,
    validation_node,
    router_node,
    draft_node,
)

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates the banking AI agent workflow pipeline.

    Pipeline: message → intent → priority → policy → validation → routing → draft
    """

    def __init__(self, intent_client: IntentGRPCClient, ollama_client: OllamaClient):
        self.intent_client = intent_client
        self.ollama_client = ollama_client

    async def run(self, message: str) -> Dict[str, Any]:
        """Execute the full agent workflow for a customer message.

        Args:
            message: Customer message to process.

        Returns:
            Dict containing the full workflow result.
        """
        logger.info("=" * 60)
        logger.info("Orchestrator: starting workflow for message: '%s'", message[:100])

        # Initialize workflow state
        state: Dict[str, Any] = {
            "message": message,
            "intent": None,
            "confidence": None,
            "intent_reason": None,
            "priority": None,
            "policy": None,
            "validation_passed": None,
            "routed_to": None,
            "draft_response": None,
            "missing_info": None,
            "next_action": None,
        }

        # Execute pipeline nodes sequentially
        state = await intent_node.run(state, self.intent_client)
        state = await priority_node.run(state)
        state = await policy_node.run(state)
        state = await validation_node.run(state)
        state = await router_node.run(state)
        state = await draft_node.run(state, self.ollama_client)

        logger.info("Orchestrator: workflow completed")
        logger.info("=" * 60)

        # Build response
        return self._build_response(state)

    def _build_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Convert workflow state to API response format."""
        return {
            "intent": {
                "intent": state["intent"],
                "confidence": state["confidence"],
                "reason": state["intent_reason"] or "",
            },
            "priority": state["priority"],
            "policy": state["policy"],
            "validation_passed": state["validation_passed"],
            "routed_to": state["routed_to"],
            "draft_response": state["draft_response"] or "",
            "missing_info": state["missing_info"],
            "next_action": state["next_action"] or "",
        }
