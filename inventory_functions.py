def handle_inventory_query(message):
    if not message:
        return None

    message = message.lower()

    if "stock" in message:
        return "The current stock is 15 units."

    if "order" in message:
        return "You can place an order by providing the SKU."

    # If no known keyword matched
    return None
