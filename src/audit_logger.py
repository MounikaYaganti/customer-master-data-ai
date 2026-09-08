import csv
import os
from datetime import datetime


def save_review_decision(
    customer,
    match,
    decision
):

    file_path = "data/review_decisions.csv"

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(file_path)

    with open(
        file_path,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Create header only for a new file
        if not file_exists:
            writer.writerow([
                "timestamp",
                "customer_name",
                "potential_duplicate",
                "similarity",
                "risk",
                "city",
                "country",
                "postal_code",
                "customer_type",
                "sales_organization",
                "review_decision"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            customer.get("customer_name"),
            match.get("customer_name"),
            match.get("similarity"),
            match.get("risk"),
            customer.get("city"),
            customer.get("country"),
            customer.get("postal_code"),
            customer.get("customer_type"),
            customer.get("sales_organization"),
            decision
        ])