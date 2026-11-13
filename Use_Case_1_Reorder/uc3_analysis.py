
import pandas as pd
from pathlib import Path

BASE = Path("data/integrated_dataset/final_dataset")

# Scenario settings
DELAY_DAYS = 7

# Load datasets
inbound = pd.read_csv(BASE / "inbound_integrated.csv")
outbound = pd.read_csv(BASE / "outbound_integrated.csv")
performance = pd.read_csv("supplier_performance.csv")

# Select supplier with the highest average lead time
supplier = performance.sort_values(
    "average_lead_time", ascending=False
).iloc[0]

SUPPLIER_ID = supplier["supplier_id"]
SUPPLIER_NAME = supplier["supplier_name"]

print("\n========== UC3 DISRUPTION SIMULATION ==========")
print("Disrupted supplier:", SUPPLIER_NAME)
print("Additional delay:", DELAY_DAYS, "days")

# Convert dates
date_columns = [
    "order_date",
    "expected_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:
    inbound[col] = pd.to_datetime(inbound[col], errors="coerce")

outbound["order_date"] = pd.to_datetime(
    outbound["order_date"], errors="coerce"
)

# Select purchase orders from disrupted supplier
affected_po = inbound[
    (inbound["supplier_id"] == SUPPLIER_ID)
    & inbound["expected_delivery_date"].notna()
].copy()

# Simulate delayed arrival
affected_po["original_expected_date"] = (
    affected_po["expected_delivery_date"]
)

affected_po["simulated_delivery_date"] = (
    affected_po["expected_delivery_date"]
    + pd.Timedelta(days=DELAY_DAYS)
)

# Find customer orders for the same product and warehouse
# placed during the simulated disruption window
affected_orders = outbound.merge(
    affected_po[
        [
            "po_id",
            "product_id",
            "warehouse_id",
            "original_expected_date",
            "simulated_delivery_date"
        ]
    ],
    on=["product_id", "warehouse_id"],
    how="inner"
)

affected_orders = affected_orders[
    (affected_orders["order_date"] >=
     affected_orders["original_expected_date"])
    & (affected_orders["order_date"] <
       affected_orders["simulated_delivery_date"])
].copy()

# Remove duplicate customer orders
affected_orders = affected_orders.drop_duplicates(
    subset=["order_id"]
)

# Estimate order value where unit price is available
if "unit_price" in affected_orders.columns:
    affected_orders["estimated_order_value"] = (
        affected_orders["quantity"]
        * affected_orders["unit_price"]
    )
else:
    affected_orders["estimated_order_value"] = 0

# Save results
affected_po.to_csv("disrupted_purchase_orders.csv", index=False)
affected_orders.to_csv("potentially_affected_customer_orders.csv", index=False)

# Summary
summary = pd.DataFrame({
    "Metric": [
        "Disrupted supplier",
        "Additional delay in days",
        "Affected purchase orders",
        "Potentially affected customer orders",
        "Estimated customer order value at risk"
    ],
    "Value": [
        SUPPLIER_NAME,
        DELAY_DAYS,
        len(affected_po),
        len(affected_orders),
        round(affected_orders["estimated_order_value"].sum(), 2)
    ]
})

summary.to_csv("disruption_summary.csv", index=False)

print("\nDISRUPTION IMPACT:")
print(summary.to_string(index=False))

print("\nFiles created:")
print("1. disrupted_purchase_orders.csv")
print("2. potentially_affected_customer_orders.csv")
print("3. disruption_summary.csv")

print("\nUC3 SIMULATION COMPLETED")
