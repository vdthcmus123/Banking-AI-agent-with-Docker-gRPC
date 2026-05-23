"""Priority assessment node — determines urgency based on intent."""

import logging

logger = logging.getLogger(__name__)

# Intent categories grouped by priority level
CRITICAL_INTENTS = {
    "compromised_card",
    "lost_or_stolen_card",
    "lost_or_stolen_phone",
    "pin_blocked",
}

HIGH_INTENTS = {
    "failed_transfer",
    "declined_card_payment",
    "declined_cash_withdrawal",
    "declined_transfer",
    "card_swallowed",
    "transaction_charged_twice",
    "card_payment_not_recognised",
    "cash_withdrawal_not_recognised",
    "direct_debit_payment_not_recognised",
    "wrong_amount_of_cash_received",
}

LOW_INTENTS = {
    "exchange_rate",
    "country_support",
    "supported_cards_and_currencies",
    "fiat_currency_support",
    "visa_or_mastercard",
    "card_delivery_estimate",
    "card_acceptance",
    "age_limit",
    "apple_pay_or_google_pay",
    "atm_support",
    "card_about_to_expire",
    "why_verify_identity",
    "disposable_card_limits",
    "top_up_limits",
}


async def run(state: dict) -> dict:
    """Determine the priority level of the customer request.

    Args:
        state: Workflow state with intent and confidence.

    Returns:
        Updated state with priority field.
    """
    intent = state.get("intent", "")
    confidence = state.get("confidence", 0.0)

    if intent in CRITICAL_INTENTS:
        priority = "critical"
    elif intent in HIGH_INTENTS or confidence < 0.3:
        priority = "high"
    elif intent in LOW_INTENTS:
        priority = "low"
    else:
        priority = "medium"

    state["priority"] = priority
    logger.info("Priority Node: %s (intent=%s)", priority, intent)
    return state
