import os
import re

from dotenv import load_dotenv
from groq import Groq

from src.retriever import search_knowledge
from src.support import (
    detect_intent,
    is_sensitive,
    calculate_confidence,
    should_escalate,
)
from src.tools import (
    check_order_status,
    create_support_ticket,
)


# Load environment variables
load_dotenv()


MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)


_client = None


def get_client():
    """Create and reuse the Groq client."""

    global _client

    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        _client = Groq(api_key=api_key)

    return _client


def generate_response(prompt):
    """Generate a response using the Groq model."""

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful customer support AI agent "
                    "for NovaTech Store. "
                    "Answer only using the provided knowledge. "
                    "Never invent policies, prices, order information, "
                    "or guarantees. "
                    "Never request passwords, OTPs, or complete "
                    "payment card details."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def extract_order_id(query):
    """Extract an order ID such as ORD1001 from a user query."""

    match = re.search(
        r"\bORD\d+\b",
        query.upper(),
    )

    if match:
        return match.group(0)

    return None


def handle_customer_query(query):
    """
    Process a customer query using retrieval,
    support logic, tools, and the LLM.
    """

    if not query or not query.strip():
        return {
            "response": "Please enter your support question.",
            "intent": "unknown",
            "confidence": 0.0,
            "escalated": False,
            "action": None,
        }

    query = query.strip()

    # Step 1: Retrieve relevant knowledge
    documents = search_knowledge(
        query,
        top_k=3,
    )

    # Step 2: Understand the query
    intent = detect_intent(query)

    # Step 3: Calculate confidence
    confidence = calculate_confidence(
        query,
        documents,
    )

    # Step 4: Check sensitive information
    sensitive = is_sensitive(query)

    # Step 5: Escalation decision
    escalate = should_escalate(
        query,
        confidence,
    )

    action = None

    # Sensitive requests are escalated
    if sensitive:
        ticket = create_support_ticket(query)

        action = {
            "type": "support_ticket",
            "result": ticket,
        }

        return {
            "response": (
                "This request involves sensitive information, "
                "so it has been escalated to a human support agent. "
                "Please do not share passwords, OTPs, or complete "
                "payment card details."
            ),
            "intent": intent,
            "confidence": confidence,
            "escalated": True,
            "action": action,
        }

    # Order-status requests use the mock order tool
    if intent == "order_status":
        order_id = extract_order_id(query)

        if order_id:
            order_result = check_order_status(
                order_id
            )

            action = {
                "type": "order_status",
                "result": order_result,
            }

            if order_result["success"]:
                response = (
                    f"Your order {order_id} is currently "
                    f"{order_result['status']}. "
                    f"Product: {order_result['product']}. "
                    f"Estimated delivery: "
                    f"{order_result['estimated_delivery']}."
                )

                return {
                    "response": response,
                    "intent": intent,
                    "confidence": confidence,
                    "escalated": False,
                    "action": action,
                }

    # Low-confidence requests are escalated
    if escalate:
        ticket = create_support_ticket(query)

        action = {
            "type": "support_ticket",
            "result": ticket,
        }

        return {
            "response": (
                "I don't have enough reliable information "
                "to safely answer this request. "
                "Your issue has been escalated to a human "
                "support agent."
            ),
            "intent": intent,
            "confidence": confidence,
            "escalated": True,
            "action": action,
        }

    # Step 6: Generate grounded response using retrieved knowledge
    context = "\n\n".join(documents)

    prompt = f"""
Customer Question:
{query}

Detected Intent:
{intent}

Knowledge Base:
{context}

Instructions:
- Answer the customer's question clearly.
- Use only the supplied knowledge base.
- Do not invent information.
- If the knowledge does not answer the question, say so.
- Keep the response concise and helpful.
"""

    response = generate_response(prompt)

    return {
        "response": response,
        "intent": intent,
        "confidence": confidence,
        "escalated": False,
        "action": action,
    }


if __name__ == "__main__":
    print("AI Customer Support Agent Test")
    print("--------------------------------")

    query = input(
        "Enter customer question: "
    )

    result = handle_customer_query(query)

    print("\nAI Response:")
    print(result["response"])

    print("\nIntent:")
    print(result["intent"])

    print("\nConfidence:")
    print(round(result["confidence"], 2))

    print("\nEscalated:")
    print(result["escalated"])

    print("\nAction:")
    print(result["action"])