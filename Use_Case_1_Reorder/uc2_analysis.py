
import pandas as pd

# Load outbound integrated dataset
df = pd.read_csv(
    "data/integrated_dataset/final_dataset/outbound_integrated.csv"
)

# Convert dates
date_columns = ["order_date", "ship_date", "delivery_date"]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Calculate delays
df["processing_days"] = (
    df["ship_date"] - df["order_date"]
).dt.days

df["delivery_days"] = (
    df["delivery_date"] - df["ship_date"]
).dt.days

df["total_delivery_days"] = (
    df["delivery_date"] - df["order_date"]
).dt.days

# Keep valid non-negative durations
df.loc[df["processing_days"] < 0, "processing_days"] = pd.NA
df.loc[df["delivery_days"] < 0, "delivery_days"] = pd.NA
df.loc[df["total_delivery_days"] < 0, "total_delivery_days"] = pd.NA

# Identify delayed stages
df["processing_status"] = df["processing_days"].apply(
    lambda x: "Delayed" if pd.notna(x) and x > 1 else
    ("On Time" if pd.notna(x) else "Unknown")
)

df["delivery_status"] = df["delivery_days"].apply(
    lambda x: "Delayed" if pd.notna(x) and x > 3 else
    ("On Time" if pd.notna(x) else "Unknown")
)

# Warehouse performance
warehouse_performance = df.groupby("warehouse_id").agg(
    total_orders=("order_id", "count"),
    average_processing_days=("processing_days", "mean"),
    average_delivery_days=("delivery_days", "mean"),
    average_total_days=("total_delivery_days", "mean")
).reset_index()

# Round averages
average_columns = [
    "average_processing_days",
    "average_delivery_days",
    "average_total_days"
]

warehouse_performance[average_columns] = (
    warehouse_performance[average_columns].round(2)
)

# Delay summary
delay_summary = pd.DataFrame({
    "Metric": [
        "Total orders",
        "Processing delayed orders",
        "Delivery delayed orders",
        "Average processing days",
        "Average delivery days",
        "Average total delivery days"
    ],
    "Value": [
        len(df),
        (df["processing_status"] == "Delayed").sum(),
        (df["delivery_status"] == "Delayed").sum(),
        round(df["processing_days"].mean(), 2),
        round(df["delivery_days"].mean(), 2),
        round(df["total_delivery_days"].mean(), 2)
    ]
})

# Save results
df.to_csv("outbound_delay_analysis.csv", index=False)
warehouse_performance.to_csv(
    "warehouse_performance.csv", index=False
)
delay_summary.to_csv("delivery_delay_summary.csv", index=False)

print("\n========== UC2 ANALYSIS COMPLETED ==========")
print(delay_summary.to_string(index=False))
print("\nWarehouse performance:")
print(warehouse_performance.to_string(index=False))

print("\nFiles created:")
print("1. outbound_delay_analysis.csv")
print("2. warehouse_performance.csv")
print("3. delivery_delay_summary.csv")
