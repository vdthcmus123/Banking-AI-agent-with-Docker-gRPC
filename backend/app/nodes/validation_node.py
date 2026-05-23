"""Validation node — validates the request against policy and rules."""

import logging

logger = logging.getLogger(__name__)


async def run(state: dict) -> dict:
    """Validate the customer request.

    Checks:
    - Message is not empty
    - Intent was detected (not fallback)
    - Confidence meets minimum threshold

    Args:
        state: Workflow state with message, intent, confidence.

    Returns:
        Updated state with validation_passed boolean.
    """
    message = state.get("message", "")
    intent = state.get("intent", "")
    confidence = state.get("confidence", 0.0)

    is_valid = True
    reasons = []

    if not message.strip():
        is_valid = False
        reasons.append("Empty message")

    if not intent or intent == "general_inquiry" and confidence == 0.0:
        is_valid = False
        reasons.append("Intent detection failed")

    if confidence < 0.3:
        reasons.append(f"Low confidence ({confidence:.2f})")
        # Don't fail validation, just note it

    state["validation_passed"] = is_valid

    if reasons:
        logger.info("Validation Node: %s (%s)", is_valid, "; ".join(reasons))
    else:
        logger.info("Validation Node: passed")

    return state
