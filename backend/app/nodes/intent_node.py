"""Intent detection node — calls Intent Service via gRPC."""

import logging

logger = logging.getLogger(__name__)


async def run(state: dict, intent_client) -> dict:
    """Classify the customer message intent via gRPC.

    Args:
        state: Workflow state containing the customer message.
        intent_client: IntentGRPCClient instance.

    Returns:
        Updated state with intent, confidence, and intent_reason.
    """
    message = state["message"]
    logger.info("Intent Node: classifying message...")

    result = await intent_client.classify(message)

    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    state["intent_reason"] = result["reason"]

    logger.info(
        "Intent Node: detected '%s' (confidence: %.2f)",
        state["intent"],
        state["confidence"],
    )
    return state
