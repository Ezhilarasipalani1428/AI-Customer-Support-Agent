import re


SENSITIVE_KEYWORDS = [
    "password",
    "otp",
    "one time password",
    "card number",
    "credit card number",
    "debit card number",
    "bank account",
    "upi pin",
    "transaction dispute",
]


def detect_intent(query):
    """Detect the customer's main support intent."""

    query_lower = query.lower()

    if any(word in query_lower for word in ["return", "refund"]):
        return "return_refund"

    if any(word in query_lower for word in ["shipping", "delivery", "delivered"]):
        return "shipping"

    if any(word in query_lower for word in ["warranty", "repair", "defect"]):
        return "warranty"

    if any(word in query_lower for word in ["payment", "paid", "charged"]):
        return "payment"

    if any(word in query_lower for word in ["login", "password", "account"]):
        return "account"

    if any(word in query_lower for word in ["order", "track", "tracking"]):
        return "order_status"

    if any(word in query_lower for word in ["product", "price", "laptop", "phone", "earbuds"]):
        return "product_information"

    return "general"


def is_sensitive(query):
    """Check whether the query contains sensitive information topics."""

    query_lower = query.lower()

    return any(
        keyword in query_lower
        for keyword in SENSITIVE_KEYWORDS
    )


def calculate_confidence(query, retrieved_documents):
    """Estimate confidence based on retrieved knowledge."""

    if not retrieved_documents:
        return 0.0

    query_words = set(
        re.findall(r"\b\w+\b", query.lower())
    )

    document_text = " ".join(retrieved_documents).lower()

    matching_words = sum(
        1 for word in query_words
        if word in document_text
    )

    if not query_words:
        return 0.0

    confidence = matching_words / len(query_words)

    return min(confidence, 1.0)


def should_escalate(query, confidence):
    """Determine whether the case should be escalated to a human."""

    if is_sensitive(query):
        return True

    if confidence < 0.45:
        return True

    return False


if __name__ == "__main__":
    test_query = "What is the return policy?"

    intent = detect_intent(test_query)
    sensitive = is_sensitive(test_query)
    confidence = calculate_confidence(
        test_query,
        [
            "Products can be returned within 7 days of delivery "
            "if they are unused and in their original condition."
        ],
    )
    escalation = should_escalate(test_query, confidence)

    print("Support Logic Test")
    print("------------------")
    print("Query:", test_query)
    print("Intent:", intent)
    print("Sensitive:", sensitive)
    print("Confidence:", round(confidence, 2))
    print("Escalate:", escalation)