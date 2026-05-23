"""Draft generation node — generates response using Ollama."""

import logging

logger = logging.getLogger(__name__)


async def run(state: dict, ollama_client) -> dict:
    """Generate a draft response for the customer using Ollama.

    Args:
        state: Workflow state with message, intent, priority, policy.
        ollama_client: OllamaClient instance.

    Returns:
        Updated state with draft_response, missing_info, next_action.
    """
    message = state["message"]
    intent = state.get("intent", "general_inquiry")
    priority = state.get("priority", "medium")
    policy = state.get("policy")

    policy_content = policy["content"] if policy else None

    logger.info("Draft Node: generating response for intent '%s'...", intent)

    result = await ollama_client.generate_response(
        message=message,
        intent=intent,
        priority=priority,
        policy_content=policy_content,
    )

    state["draft_response"] = result["draft_response"]
    state["missing_info"] = result.get("missing_info")
    state["next_action"] = result.get("next_action", "provide_information")

    logger.info("Draft Node: response generated, next_action=%s", state["next_action"])
    return state
