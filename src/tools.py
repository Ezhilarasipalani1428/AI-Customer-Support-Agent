MOCK_ORDERS = {
    "ORD1001": {
        "status": "Shipped",
        "product": "NovaBook Pro 14",
        "estimated_delivery": "2 days",
    },
    "ORD1002": {
        "status": "Processing",
        "product": "NovaPhone X",
        "estimated_delivery": "3 to 5 days",
    },
    "ORD1003": {
        "status": "Delivered",
        "product": "NovaBuds Air",
        "estimated_delivery": "Delivered",
    },
}


def check_order_status(order_id):
    """Check the status of a mock customer order."""

    if not order_id:
        return {
            "success": False,
            "message": "Order ID is required.",
        }

    order_id = order_id.strip().upper()

    order = MOCK_ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "message": f"No order found for {order_id}.",
        }

    return {
        "success": True,
        "order_id": order_id,
        **order,
    }


def create_support_ticket(issue):
    """Create a mock support ticket."""

    if not issue or not issue.strip():
        return {
            "success": False,
            "message": "Issue description is required.",
        }

    ticket_id = "TKT1001"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "Created",
        "issue": issue.strip(),
        "message": (
            f"Support ticket {ticket_id} has been created "
            "and will be reviewed by a human support agent."
        ),
    }


if __name__ == "__main__":
    print("Agentic Tools Test")
    print("------------------")

    print("\nOrder Status:")
    print(check_order_status("ORD1001"))

    print("\nSupport Ticket:")
    print(create_support_ticket("Customer needs help with a refund decision."))