"""Banking policies data for policy retrieval node."""

BANKING_POLICIES = {
    "lost_or_stolen_card": {
        "policy_id": "POL-001",
        "title": "Lost/Stolen Card Policy",
        "content": "If a card is lost or stolen, immediately freeze the card via the app or call our 24/7 hotline at 1800-XXX-XXXX. A replacement card will be issued within 5-7 business days. Any unauthorized transactions reported within 48 hours will be fully refunded.",
        "applicable": True,
    },
    "compromised_card": {
        "policy_id": "POL-002",
        "title": "Compromised Card Security Policy",
        "content": "If card details have been compromised, the card will be blocked immediately. A new card with a new number will be issued. All recent transactions will be reviewed for fraud. Temporary virtual card can be issued within 24 hours.",
        "applicable": True,
    },
    "card_not_working": {
        "policy_id": "POL-003",
        "title": "Card Troubleshooting Policy",
        "content": "If the card is not working, first check if it is activated and not expired. Try cleaning the chip or using contactless payment. If the issue persists, contact support for a replacement card. Replacement fee may apply for damaged cards.",
        "applicable": True,
    },
    "activate_my_card": {
        "policy_id": "POL-004",
        "title": "Card Activation Policy",
        "content": "New cards can be activated via the mobile app, website, or by calling customer service. Activation requires identity verification. Cards not activated within 30 days will be automatically cancelled for security.",
        "applicable": True,
    },
    "change_pin": {
        "policy_id": "POL-005",
        "title": "PIN Change Policy",
        "content": "PIN can be changed at any ATM, via the mobile app, or by calling customer service. For security, PIN change requires current PIN or identity verification. After 3 incorrect PIN attempts, the card will be temporarily locked.",
        "applicable": True,
    },
    "declined_card_payment": {
        "policy_id": "POL-006",
        "title": "Declined Payment Policy",
        "content": "Payments may be declined due to insufficient funds, exceeded daily limits, merchant restrictions, or fraud detection. Check your balance and daily limits in the app. If the decline seems incorrect, contact support to review the transaction.",
        "applicable": True,
    },
    "failed_transfer": {
        "policy_id": "POL-007",
        "title": "Failed Transfer Policy",
        "content": "Failed transfers are usually reversed within 1-3 business days. Common causes include incorrect recipient details, network issues, or exceeded limits. If funds are not returned within 5 business days, file a dispute with customer service.",
        "applicable": True,
    },
    "request_refund": {
        "policy_id": "POL-008",
        "title": "Refund Request Policy",
        "content": "Refund requests must be submitted within 60 days of the transaction. Refunds are processed within 5-10 business days. For disputed charges, a temporary credit may be issued while the investigation is ongoing. Provide transaction details and reason for the refund.",
        "applicable": True,
    },
    "terminate_account": {
        "policy_id": "POL-009",
        "title": "Account Termination Policy",
        "content": "Account closure requires zero balance and no pending transactions. Outstanding loans must be settled first. Any remaining rewards points will be forfeited. Account closure is processed within 30 days and a confirmation letter will be sent.",
        "applicable": True,
    },
    "verify_my_identity": {
        "policy_id": "POL-010",
        "title": "Identity Verification Policy",
        "content": "Identity verification requires a valid government-issued ID and proof of address. Verification can be done online via video call or at a branch. Processing takes 1-3 business days. Account features may be limited until verification is complete.",
        "applicable": True,
    },
    "balance_not_updated_after_bank_transfer": {
        "policy_id": "POL-011",
        "title": "Balance Update Policy",
        "content": "Bank transfers may take 1-3 business days to reflect in your balance. Same-bank transfers are usually instant. If the balance is not updated after 3 business days, contact support with the transaction reference number for investigation.",
        "applicable": True,
    },
    "top_up_failed": {
        "policy_id": "POL-012",
        "title": "Top-Up Failure Policy",
        "content": "Failed top-ups are reversed to the source account within 1-2 business days. Common causes include card expiry, insufficient funds, or daily limit exceeded. Try again with a different payment method or contact support.",
        "applicable": True,
    },
    "pending_transfer": {
        "policy_id": "POL-013",
        "title": "Pending Transfer Policy",
        "content": "Transfers may remain pending due to security checks, weekend/holiday processing, or recipient bank processing times. International transfers may take 3-5 business days. Contact support if the transfer has been pending for more than the expected processing time.",
        "applicable": True,
    },
    "card_payment_not_recognised": {
        "policy_id": "POL-014",
        "title": "Unrecognized Transaction Policy",
        "content": "If you don't recognize a transaction, check if it might be a subscription or recurring payment. Merchant names may differ from store names. If the charge is unauthorized, report it immediately for fraud investigation. Temporary card freeze is recommended.",
        "applicable": True,
    },
    "transaction_charged_twice": {
        "policy_id": "POL-015",
        "title": "Double Charge Policy",
        "content": "Duplicate charges are often due to payment processing errors. Wait 24-48 hours as one charge may be a temporary authorization hold. If both charges are confirmed, contact support with both transaction IDs for an automatic refund.",
        "applicable": True,
    },
    "pin_blocked": {
        "policy_id": "POL-016",
        "title": "PIN Blocked Policy",
        "content": "PIN is blocked after 3 consecutive incorrect attempts. You can unblock your PIN via the mobile app or by visiting a branch with valid ID. A new PIN can be set after identity verification.",
        "applicable": True,
    },
    "transfer_not_received_by_recipient": {
        "policy_id": "POL-017",
        "title": "Transfer Not Received Policy",
        "content": "If the recipient has not received the transfer, verify the recipient details are correct. Domestic transfers take 1-2 business days, international transfers take 3-5 business days. Contact support with the transaction reference for a trace request.",
        "applicable": True,
    },
    "card_swallowed": {
        "policy_id": "POL-018",
        "title": "Card Swallowed by ATM Policy",
        "content": "If your card is retained by an ATM, note the ATM location and time. Contact us within 24 hours. If it was our ATM, the card can be retrieved within 5 business days. Otherwise, a replacement card will be issued.",
        "applicable": True,
    },
}
