import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from shared import *


def render_uc1(reorder_alerts, supplier_performance, product_inventory):

    page_header(
        "Inbound Reorder Analysis",
        "Monitor stock availability, identify replenishment requirements "
        "and evaluate supplier reliability."
    )

    if reorder_alerts.empty or supplier_performance.empty:
        st.error("UC1 output files are missing. Run uc1_analysis.py first.")
        st.stop()

    # 1. CLEAN DATA
    
    reorder_view = reorder_alerts.copy()
    supplier_view = supplier_performance.copy()
    inventory_view = product_inventory.copy()

    for col in ["reorder_status", "category", "warehouse_name"]:
        if col in reorder_view.columns:
            reorder_view[col] = (
                reorder_view[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .str.title()
            )

    for col in [
        "stock_on_hand", "reorder_point", "safety_stock",
        "unit_cost", "unit_price"
    ]:
        if col in reorder_view.columns:
            reorder_view[col] = pd.to_numeric(reorder_view[col], errors="coerce")

    for col in [
        "average_lead_time", "average_expected_lead_time",
        "late_orders", "total_orders"
    ]:
        if col in supplier_view.columns:
            supplier_view[col] = pd.to_numeric(supplier_view[col], errors="coerce")

    # Latest record per product (and warehouse) for stock-position analysis
    snapshot = alert_snapshot(reorder_view)

    # 2. KPI CARDS

    total_alert_records = len(reorder_view)

    unique_products = (
        reorder_view["product_id"].nunique()
        if "product_id" in reorder_view.columns else 0
    )

    supplier_count = (
        supplier_view["supplier_id"].nunique()
        if "supplier_id" in supplier_view.columns
        else len(supplier_view)
    )

    total_late_orders = (
        supplier_view["late_orders"].sum()
        if "late_orders" in supplier_view.columns else 0
    )
    total_supplier_orders = (
        supplier_view["total_orders"].sum()
        if "total_orders" in supplier_view.columns else 0
    )
    late_rate = (
        total_late_orders / total_supplier_orders * 100
        if total_supplier_orders else None
    )

    below_safety = None
    if {"stock_on_hand", "safety_stock"}.issubset(snapshot.columns):
        valid = snapshot[["stock_on_hand", "safety_stock"]].dropna()
        below_safety = int((valid["stock_on_hand"] <= valid["safety_stock"]).sum())

    kpi_cards([
        (
            "Reorder Alert Records", f"{total_alert_records:,}",
            "Inventory records flagged", "amber"
        ),
        (
            "Products with Alerts", f"{unique_products:,}",
            f"Across {supplier_count:,} suppliers analysed"
        ),
        (
            "Below Safety Stock",
            f"{below_safety:,}" if below_safety is not None else "N/A",
            "Latest stock positions at or under safety stock", "red"
        ),
        (
            "Late Purchase Orders", f"{total_late_orders:,.0f}",
            f"of {total_supplier_orders:,.0f} supplier orders"
            if total_supplier_orders else None,
            "amber"
        ),
        (
            "Late-Order Rate",
            f"{late_rate:.1f}%" if late_rate is not None else "N/A",
            "Late orders as a share of all supplier orders"
        ),
    ], per_row=5)

    # 3. REORDER EXPOSURE

    section_heading(
        "Reorder Exposure",
        "How alerts split by status, product category and warehouse."
    )

    exp_status, exp_category, exp_warehouse = st.columns(3, gap="medium")

    category_counts = pd.DataFrame()

    with exp_status:
        with card("Alert Status", "Share of alert records."):
            if "reorder_status" in reorder_view.columns:
                donut_compact(
                    reorder_view["reorder_status"].value_counts(),
                    centre_label="alert records"
                )
            else:
                st.info("Reorder status information is unavailable.")

    with exp_category:
        with card("By Product Category", "Unique products with alerts."):
            if {"category", "product_id"}.issubset(reorder_view.columns):
                category_counts = (
                    reorder_view.groupby("category")["product_id"]
                    .nunique()
                    .reset_index(name="products")
                )
                hbar_chart(
                    category_counts, "category", "products",
                    "Unique products", fmt="%d"
                )
            else:
                st.info("Product category information is unavailable.")

    with exp_warehouse:
        with card("By Warehouse", "Unique products with alerts."):
            if {"warehouse_name", "product_id"}.issubset(reorder_view.columns):
                warehouse_counts = (
                    reorder_view.groupby("warehouse_name")["product_id"]
                    .nunique()
                    .reset_index(name="products")
                )
                hbar_chart(
                    warehouse_counts, "warehouse_name", "products",
                    "Unique products", fmt="%d", colour=BLUE_MID
                )
            else:
                st.info("Warehouse information is unavailable.")

    # 4. PRODUCTS REQUIRING ATTENTION

    section_heading(
        "Products Requiring Attention",
        "Largest shortfalls between stock on hand and the reorder point, "
        "using the latest record for each product and warehouse."
    )

    shortage = pd.DataFrame()

    if {"product_id", "stock_on_hand", "reorder_point"}.issubset(
        snapshot.columns
    ):
        shortage = snapshot.copy()

        base_label = (
            shortage["product_name"].astype(str)
            if "product_name" in shortage.columns
            else shortage["product_id"].astype(str)
        )

        if "warehouse_name" in shortage.columns:
            shortage["position"] = base_label + " · " + shortage["warehouse_name"].astype(str)
        elif "warehouse_id" in shortage.columns:
            shortage["position"] = base_label + " · " + shortage["warehouse_id"].astype(str)
        else:
            shortage["position"] = base_label

        shortage["stock_gap"] = shortage["reorder_point"] - shortage["stock_on_hand"]
        shortage = shortage.dropna(subset=["stock_gap"])

    if not shortage.empty:

        attn_left, attn_right = st.columns([1.7, 1], gap="large")

        with attn_left:
            with card(
                "Stock on Hand vs Reorder Point",
                "10 stock positions with the largest shortfall."
            ):
                grouped_hbar_chart(
                    shortage, "position",
                    [
                        ("reorder_point", "Reorder point", BLUE_LIGHT),
                        ("stock_on_hand", "Stock on hand", BLUE),
                    ],
                    "Units", sort_col="stock_gap", top_n=10
                )

        with attn_right:
            short = shortage[shortage["stock_gap"] > 0]

            lines = [
                f"<b>{len(short):,}</b> of {len(shortage):,} stock "
                "positions are below their reorder point."
            ]

            if not short.empty:
                worst = short.sort_values("stock_gap", ascending=False).iloc[0]
                lines.append(
                    f"Largest shortfall: <b>{esc(worst['position'])}</b> "
                    f"at {worst['stock_gap']:,.0f} units."
                )
                lines.append(
                    f"Total units short of reorder point: "
                    f"<b>{short['stock_gap'].sum():,.0f}</b>."
                )

                if "unit_cost" in short.columns:
                    cost = (short["stock_gap"] * short["unit_cost"]).sum()
                    if pd.notna(cost) and cost > 0:
                        lines.append(
                            "Approximate cost to restore reorder point: "
                            f"<b>{inr(cost)}</b> (units short × unit cost)."
                        )

            insight_panel("What this means", lines)

    else:
        st.info("Stock and reorder-point fields are unavailable.")

    # 5. SUPPLIER DELIVERY PERFORMANCE

    section_heading(
        "Supplier Delivery Performance",
        "Lead times against expectations and where late orders concentrate."
    )

    s1, s2 = st.columns(2, gap="large")

    with s1:
        with card(
            "Actual vs Expected Lead Time",
            "Average days from order to receipt."
        ):
            grouped_hbar_chart(
                supplier_view, "supplier_name",
                [
                    ("average_expected_lead_time", "Expected", BLUE_LIGHT),
                    ("average_lead_time", "Actual", BLUE),
                ],
                "Lead time (days)", sort_col="average_lead_time"
            )

    with s2:
        with card(
            "Lead-Time Variance",
            "Positive = slower than expected."
        ):
            variance_chart(
                supplier_view, "supplier_name",
                "average_lead_time", "average_expected_lead_time"
            )

    s3, s4 = st.columns(2, gap="large")

    with s3:
        with card("Late Purchase Orders", "Count of late orders by supplier."):
            hbar_chart(
                supplier_view, "supplier_name", "late_orders",
                "Late orders", fmt="%.0f",
                highlight_colour=WARN
            )

    with s4:
        with card(
            "Late-Order Rate",
            "Late orders as a share of each supplier's total orders."
        ):
            if {"supplier_name", "late_orders", "total_orders"}.issubset(
                supplier_view.columns
            ):
                rate_data = supplier_view[supplier_view["total_orders"] > 0].copy()
                rate_data["late_rate"] = (
                    rate_data["late_orders"] / rate_data["total_orders"] * 100
                )
                hbar_chart(
                    rate_data, "supplier_name", "late_rate",
                    "Late rate (%)", fmt="%.1f%%",
                    colour=BLUE_MID, highlight_colour=WARN
                )
            else:
                st.info("Supplier order counts are unavailable.")

    # 6. KEY OBSERVATIONS

    section_heading("Key Observations")

    observations = []

    if not category_counts.empty:
        top_category = category_counts.sort_values("products", ascending=False).iloc[0]
        observations.append(
            f"**Category exposure:** {top_category['category']} has the "
            f"most products with reorder alerts "
            f"({int(top_category['products']):,})."
        )

    if "reorder_status" in reorder_view.columns and total_alert_records:
        status_counts = reorder_view["reorder_status"].value_counts()
        observations.append(
            f"**Alert status:** {status_counts.index[0]} is the most common "
            f"status ({int(status_counts.iloc[0]):,} of "
            f"{total_alert_records:,} records)."
        )

    if below_safety:
        observations.append(
            f"**Safety stock:** {below_safety:,} stock positions are at or "
            "below safety stock and need priority replenishment."
        )

    if {"supplier_name", "late_orders"}.issubset(supplier_view.columns):
        ranked = supplier_view.dropna(subset=["late_orders"])
        if not ranked.empty:
            worst_supplier = ranked.sort_values("late_orders", ascending=False).iloc[0]
            observations.append(
                f"**Late deliveries:** {worst_supplier['supplier_name']} has "
                f"the most late purchase orders ({worst_supplier['late_orders']:,.0f})."
            )

    if {
        "supplier_name", "average_lead_time", "average_expected_lead_time"
    }.issubset(supplier_view.columns):
        gap_data = supplier_view.dropna(
            subset=["average_lead_time", "average_expected_lead_time"]
        ).copy()
        if not gap_data.empty:
            gap_data["overrun"] = (
                gap_data["average_lead_time"] - gap_data["average_expected_lead_time"]
            )
            largest = gap_data.sort_values("overrun", ascending=False).iloc[0]
            observations.append(
                f"**Lead-time overrun:** {largest['supplier_name']} averages "
                f"{largest['overrun']:+.1f} days against its expected lead time."
            )

    if late_rate is not None:
        observations.append(
            f"**Overall reliability:** {late_rate:.1f}% of supplier purchase "
            "orders were delivered late."
        )

    observation_list(observations)

    st.caption(
        "Reorder alert records are inventory observations, not necessarily "
        "unique purchase orders. Stock-position figures use the latest "
        "record for each product and warehouse where a date is available."
    )

    # 7. DETAIL TABLES

    with st.expander("View Reorder Alert Details", expanded=False):

        f1, f2, f3 = st.columns(3)

        with f1:
            status_options = (
                ["All"] + sorted(reorder_view["reorder_status"].dropna().unique().tolist())
                if "reorder_status" in reorder_view.columns else ["All"]
            )
            selected_status = st.selectbox(
                "Reorder status", status_options, key="uc1_status_filter"
            )

        with f2:
            category_options = (
                ["All"] + sorted(reorder_view["category"].dropna().unique().tolist())
                if "category" in reorder_view.columns else ["All"]
            )
            selected_category = st.selectbox(
                "Product category", category_options, key="uc1_category_filter"
            )

        with f3:
            warehouse_options = (
                ["All"] + sorted(reorder_view["warehouse_name"].dropna().unique().tolist())
                if "warehouse_name" in reorder_view.columns else ["All"]
            )
            selected_warehouse = st.selectbox(
                "Warehouse", warehouse_options, key="uc1_warehouse_filter"
            )

        filtered_reorders = reorder_view.copy()

        if selected_status != "All" and "reorder_status" in filtered_reorders.columns:
            filtered_reorders = filtered_reorders[
                filtered_reorders["reorder_status"] == selected_status
            ]

        if selected_category != "All" and "category" in filtered_reorders.columns:
            filtered_reorders = filtered_reorders[
                filtered_reorders["category"] == selected_category
            ]

        if selected_warehouse != "All" and "warehouse_name" in filtered_reorders.columns:
            filtered_reorders = filtered_reorders[
                filtered_reorders["warehouse_name"] == selected_warehouse
            ]

        st.caption(
            f"Showing {len(filtered_reorders):,} of {len(reorder_view):,} alert records."
        )
        st.dataframe(
            filtered_reorders, use_container_width=True,
            hide_index=True, height=350
        )

    with st.expander("View Supplier Performance Details", expanded=False):
        st.dataframe(
            supplier_view, use_container_width=True,
            hide_index=True, height=300
        )

    with st.expander("View Product Inventory Summary", expanded=False):
        st.dataframe(
            inventory_view, use_container_width=True,
            hide_index=True, height=350
        )
