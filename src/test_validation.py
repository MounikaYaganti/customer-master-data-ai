from validation import validate_customer
from duplicate import find_similar_customers


# New customer
customer = {
    "customer_name": "ABC Distribution LLC",
    "country": "USA",
    "city": "Chicago",
    "postal_code": "60601",
    "customer_type": "Distributor",
    "sales_organization": "US01"
}


# Validate customer
result = validate_customer(customer)

print("Validation Result:")
print(result)


# Existing customers
existing_customers = [
    {
        "customer_name": "ABC Distributors",
        "city": "Chicago",
        "country": "USA"
    },
    {
        "customer_name": "Global Foods Inc",
        "city": "Dallas",
        "country": "USA"
    },
    {
        "customer_name": "XYZ Retail",
        "city": "New York",
        "country": "USA"
    }
]


# Find potential duplicates
similar_customers = find_similar_customers(
    customer,
    existing_customers
)

print("\nPotential Duplicate Customers:")

if similar_customers:
    for match in similar_customers:
        print(
            f"- {match['customer_name']} "
            f"({match['similarity']}% similar)"
        )
else:
    print("No potential duplicates found.")