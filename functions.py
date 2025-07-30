def get_best_supplier(part_name: str) -> dict:
    """Finds the most reliable supplier for a given part based on risk and quality."""
    return {"supplier": "ABC Corp", "risk": "Low"}


def get_best_price(part_name: str) -> dict:
    """Finds the lowest price for a given part across multiple suppliers."""
    return {"supplier": "XYZ Ltd", "price": 500}
