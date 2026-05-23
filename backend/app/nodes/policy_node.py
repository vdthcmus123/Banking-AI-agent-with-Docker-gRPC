"""Policy retrieval node — looks up applicable banking policy."""

import logging
from app.data.policies import BANKING_POLICIES

logger = logging.getLogger(__name__)


async def run(state: dict) -> dict:
    """Retrieve the applicable banking policy for the detected intent.

    Args:
        state: Workflow state with intent field.

    Returns:
        Updated state with policy field (dict or None).
    """
    intent = state.get("intent", "")
    policy = BANKING_POLICIES.get(intent)

    if policy:
        state["policy"] = policy
        logger.info("Policy Node: found policy '%s'", policy["policy_id"])
    else:
        state["policy"] = None
        logger.info("Policy Node: no specific policy for intent '%s'", intent)

    return state
