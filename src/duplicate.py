from difflib import SequenceMatcher


def normalize(value):
    """Convert a value to lowercase text and remove extra spaces."""
    if value is None:
        return ""

    return str(value).lower().strip()


def name_similarity(name1, name2):
    """Calculate similarity between two customer names."""
    return SequenceMatcher(
        None,
        normalize(name1),
        normalize(name2)
    ).ratio()


def find_similar_customers(new_customer, existing_customers):
    matches = []

    for existing in existing_customers:

        # -------------------------------------------------
        # 1. Customer Name
        # -------------------------------------------------
        name_score = name_similarity(
            new_customer.get("customer_name"),
            existing.get("customer_name")
        )

        # -------------------------------------------------
        # 2. Location / Master Data Attributes
        # -------------------------------------------------
        city_match = (
            normalize(new_customer.get("city"))
            == normalize(existing.get("city"))
        )

        country_match = (
            normalize(new_customer.get("country"))
            == normalize(existing.get("country"))
        )

        postal_match = (
            normalize(new_customer.get("postal_code"))
            == normalize(existing.get("postal_code"))
        )

        customer_type_match = (
            normalize(new_customer.get("customer_type"))
            == normalize(existing.get("customer_type"))
        )

        sales_org_match = (
            normalize(new_customer.get("sales_organization"))
            == normalize(existing.get("sales_organization"))
        )

        # -------------------------------------------------
        # 3. Weighted Duplicate Score
        # -------------------------------------------------

        score = (
            name_score * 0.50
            + (0.15 if city_match else 0)
            + (0.10 if country_match else 0)
            + (0.10 if postal_match else 0)
            + (0.05 if customer_type_match else 0)
            + (0.10 if sales_org_match else 0)
        )

        # Convert to percentage
        similarity = round(score * 100, 2)

        # -------------------------------------------------
        # 4. Risk Classification
        # -------------------------------------------------
        if similarity >= 90:
            risk = "HIGH"

        elif similarity >= 75:
            risk = "MEDIUM"

        else:
            risk = "LOW"
        

        # -------------------------------------------------
        # 5. Keep potential duplicates
        # -------------------------------------------------

        if similarity >= 70:
            confidence = similarity
            matches.append({
                "customer_name": existing.get("customer_name"),
                "city": existing.get("city"),
                "country": existing.get("country"),
                "postal_code": existing.get("postal_code"),
                "customer_type": existing.get("customer_type"),
                "sales_organization": existing.get(
                    "sales_organization"
                ),
                "name_similarity": round(name_score * 100, 2),
                "city_match": city_match,
                "country_match": country_match,
                "postal_match": postal_match,
                "customer_type_match": customer_type_match,
                "sales_org_match": sales_org_match,
                "similarity": similarity,
                "risk": risk,
                "confidence": confidence 
            })

    # Highest similarity first
    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return matches