import csv
from pathlib import Path


def load_customer_master():
    file_path = Path(__file__).parent.parent / "data" / "customer_master.csv"

    customers = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customers.append(row)

    return customers