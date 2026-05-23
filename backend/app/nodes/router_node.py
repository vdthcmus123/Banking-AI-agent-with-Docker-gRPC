"""Router node — routes the request to the appropriate department."""

import logging

logger = logging.getLogger(__name__)

# Intent-to-department routing map
CARD_INTENTS = {
    "activate_my_card", "card_about_to_expire", "card_acceptance",
    "card_arrival", "card_delivery_estimate", "card_linking",
    "card_not_working", "card_swallowed", "change_pin",
    "compromised_card", "contactless_not_working", "declined_card_payment",
    "get_physical_card", "getting_spare_card", "getting_virtual_card",
    "lost_or_stolen_card", "order_physical_card", "pin_blocked",
    "virtual_card_not_working", "visa_or_mastercard",
}

TRANSACTION_INTENTS = {
    "cancel_transfer", "card_payment_fee_charged",
    "card_payment_not_recognised", "card_payment_wrong_exchange_rate",
    "cash_withdrawal_charge", "cash_withdrawal_not_recognised",
    "declined_cash_withdrawal", "declined_transfer",
    "direct_debit_payment_not_recognised", "extra_charge_on_statement",
    "failed_transfer", "pending_card_payment", "pending_cash_withdrawal",
    "pending_transfer", "receiving_money", "refund_not_showing_up",
    "request_refund", "reverted_card_payment", "transaction_charged_twice",
    "transfer_fee_charged", "transfer_into_account",
    "transfer_not_received_by_recipient", "transfer_timing",
    "wrong_amount_of_cash_received", "wrong_exchange_rate_for_cash_withdrawal",
}

ACCOUNT_INTENTS = {
    "beneficiary_not_allowed", "edit_personal_details",
    "passcode_forgotten", "terminate_account",
    "balance_not_updated_after_bank_transfer",
    "balance_not_updated_after_cheque_or_cash_deposit",
    "lost_or_stolen_phone",
}

TOPUP_INTENTS = {
    "automatic_top_up", "pending_top_up", "top_up_by_bank_transfer_charge",
    "top_up_by_card_charge", "top_up_by_cash_or_cheque", "top_up_failed",
    "top_up_limits", "top_up_reverted", "topping_up_by_card",
}

VERIFICATION_INTENTS = {
    "unable_to_verify_identity", "verify_my_identity",
    "verify_source_of_funds", "verify_top_up", "why_verify_identity",
}

INFO_INTENTS = {
    "age_limit", "apple_pay_or_google_pay", "atm_support",
    "country_support", "disposable_card_limits", "exchange_rate",
    "exchange_via_app", "fiat_currency_support",
    "supported_cards_and_currencies",
}


async def run(state: dict) -> dict:
    """Route the request to the appropriate department.

    Args:
        state: Workflow state with intent field.

    Returns:
        Updated state with routed_to field.
    """
    intent = state.get("intent", "")

    if intent in CARD_INTENTS:
        department = "card_services"
    elif intent in TRANSACTION_INTENTS:
        department = "transaction_services"
    elif intent in ACCOUNT_INTENTS:
        department = "account_services"
    elif intent in TOPUP_INTENTS:
        department = "topup_services"
    elif intent in VERIFICATION_INTENTS:
        department = "verification_services"
    elif intent in INFO_INTENTS:
        department = "information_services"
    else:
        department = "general_support"

    state["routed_to"] = department
    logger.info("Router Node: routed to '%s' (intent=%s)", department, intent)
    return state
