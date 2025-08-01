def _get_suppliers_from_database(part_name: str) -> list:
    """Helper: Gets suppliers from the database."""
    return [
        {"name": "Supplier A", "risk": 0.1, "quality": 98, "price": 510, "source": "database"},
        {"name": "Supplier B", "risk": 0.3, "quality": 95, "price": 490, "source": "database"},
    ]

def _get_suppliers_from_website_one(part_name: str) -> list:
    """Helper: Gets suppliers from website one."""
    return [
        {"name": "Supplier C", "risk": 0.05, "quality": 99, "price": 525, "source": "website_one"},
        {"name": "Supplier D", "risk": 0.2, "quality": 92, "price": 480, "source": "website_one"},
    ]

def _get_suppliers_from_website_two(part_name: str) -> list:
    """Helper: Gets suppliers from website two."""
    return [
        {"name": "Supplier E", "risk": 0.5, "quality": 96, "price": 500, "source": "website_two"},
    ]

def _get_all_suppliers(part_name: str) -> list:
    """Helper function to aggregate suppliers from all sources."""
    print(f"Gathering supplier data for {part_name} from all sources...")
    all_suppliers = (
        _get_suppliers_from_database(part_name)
        + _get_suppliers_from_website_one(part_name)
        + _get_suppliers_from_website_two(part_name)
    )
    return all_suppliers

def get_best_supplier(part_name: str) -> dict:
    """Finds the most reliable supplier for a given part based on the lowest risk."""
    all_suppliers = _get_all_suppliers(part_name)
    best_supplier = min(all_suppliers, key=lambda x: x['risk'])
    return best_supplier

def get_best_price(part_name: str) -> dict:
    """Finds the lowest price for a given part across multiple suppliers."""
    all_suppliers = _get_all_suppliers(part_name)
    best_price_supplier = min(all_suppliers, key=lambda x: x['price'])
    return best_price_supplier

def get_report(part_name: str) -> str:
    """Generates a report analyzing all potential suppliers and explaining why the one with the lowest risk was chosen."""
    all_suppliers = _get_all_suppliers(part_name)
    best_supplier = min(all_suppliers, key=lambda x: x['risk'])

    report = f"Analysis for {part_name}:\n\n"
    report += f"A total of {len(all_suppliers)} suppliers were considered, sourced from our database and two external websites.\n"
    report += f"The chosen supplier is '{best_supplier['name']}' (from {best_supplier['source']}) primarily due to its outstandingly low risk profile of {best_supplier['risk']}.\n\n"
    report += "Comparison with other suppliers:\n"
    for s in all_suppliers:
        if s['name'] != best_supplier['name']:
            report += f"- '{s['name']}' (from {s['source']}) had a risk of {s['risk']}.\n"
    
    report += "\nConclusion: While other suppliers might offer slightly different prices, the significantly lower risk associated with '"
    report += f"{best_supplier['name']}' makes it the most reliable choice for this part."
    
    return report
