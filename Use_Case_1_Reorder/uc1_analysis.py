
import pandas as pd
from pathlib import Path

BASE = Path("data/integrated_dataset/final_dataset")

# Load integrated datasets
inbound = pd.read_csv(BASE / "inbound_integrated.csv")
inventory = pd.read_csv(BASE / "inventory_integrated.csv")
outbound = pd.read_csv(BASE / "outbound_integrated.csv")

# Convert dates
for col in ["order_date", "expected_delivery_date", "actual_delivery_date"]:
    inbound[col] = pd.to_datetime(inbound[col], errors="coerce")

# Calculate supplier delivery performance
inbound["actual_lead_time"] = (
    inbound["actual_delivery_date"] - inbound["order_date"]
).dt.days

inbound["expected_lead_time"] = (
    inbound["expected_delivery_date"] - inbound["order_date"]
).dt.days

valid = inbound[
    inbound["actual_lead_time"].notna()
    & (inbound["actual_lead_time"] >= 0)
]

supplier_performance = valid.groupby(
    ["supplier_id", "supplier_name"]
).agg(
    total_orders=("po_id", "count"),
    average_lead_time=("actual_lead_time", "mean"),
    average_expected_lead_time=("expected_lead_time", "mean"),
    late_orders=("actual_lead_time", lambda x: (
        x > valid.loc[x.index, "expected_lead_time"]
    ).sum())
).reset_index()

supplier_performance["average_lead_time"] = (
    supplier_performance["average_lead_time"].round(2)
)

supplier_performance.to_csv("supplier_performance.csv", index=False)

# Identify products needing reorder
inventory["reorder_status"] = inventory.apply(
    lambda row: "REORDER"
    if row["stock_on_hand"] <= row["reorder_point"]
    else "SUFFICIENT",
    axis=1
)

reorder_alerts = inventory[
    inventory["reorder_status"] == "REORDER"
].copy()

reorder_alerts.to_csv("reorder_alerts.csv", index=False)

# Product-level inventory summary
latest_inventory = (
    inventory.sort_values("date")
    .groupby(["product_id", "warehouse_id"])
    .tail(1)
)

product_summary = latest_inventory.groupby("product_id").agg(
    total_stock=("stock_on_hand", "sum"),
    total_reorder_point=("reorder_point", "sum"),
    total_safety_stock=("safety_stock", "sum")
).reset_index()

product_summary.to_csv("product_inventory_summary.csv", index=False)

print("\n========== UC1 ANALYSIS COMPLETED ==========")
print("Supplier performance records:", len(supplier_performance))
print("Reorder alerts:", len(reorder_alerts))
print("Products analyzed:", len(product_summary))
print("\nFiles created:")
print("1. supplier_performance.csv")
print("2. reorder_alerts.csv")
print("3. product_inventory_summary.csv")
