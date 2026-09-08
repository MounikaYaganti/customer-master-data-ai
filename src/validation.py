def validate_customer(customer):
    errors = []

    # Mandatory field checks
    if not customer.get("customer_name"):
        errors.append("Customer name is mandatory.")

    if not customer.get("country"):
        errors.append("Country is mandatory.")

    if not customer.get("city"):
        errors.append("City is mandatory.")

    if not customer.get("postal_code"):
        errors.append("Postal code is mandatory.")

    if not customer.get("customer_type"):
        errors.append("Customer type is mandatory.")

    # Customer type validation
    allowed_customer_types = [
        "Distributor",
        "Retailer",
        "Wholesaler"
    ]

    if customer.get("customer_type") not in allowed_customer_types:
        errors.append(
            "Customer type must be Distributor, Retailer, or Wholesaler."
        )

    # Distributor business rule
    if customer.get("customer_type") == "Distributor":
        if not customer.get("sales_organization"):
            errors.append(
                "Sales organization is mandatory for Distributor customers."
            )

    # Final result
    if errors:
        return {
            "status": "FAILED",
            "errors": errors
        }

    return {
        "status": "PASSED",
        "errors": []
    }