import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from shared import *


def render_uc3(disrupted_pos, affected_orders, disruption_summary):

    page_header(
        "Supplier Disruption Control Tower",
        "Monitor supplier disruptions, analyse purchase order delays, "
        "and assess their potential impact on customer orders."
    )

    if disrupted_pos.empty and affected_orders.empty:
        st.error(
            "UC3 output files are missing or empty. Run uc3_analysis.py first."
        )
        st.stop()

    # 1. PREPARE DATA

    po_view = disrupted_pos.copy()
    customer_view = affected_orders.copy()

    for frame, columns in [
        (po_view, ["supplier_name", "country", "status"]),
        (customer_view, ["status"])
    ]:
        for col in columns:
            if col in frame.columns:
                frame[col] = (
                    frame[col]
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                    .replace("", "Unknown")
                )

    if "order_id" in customer_view.columns:
        customer_view = customer_view.drop_duplicates(subset=["order_id"])

    total_pos = (
        po_view["po_id"].nunique() if "po_id" in po_view.columns else len(po_view)
    )
    total_customers = (
        customer_view["order_id"].nunique()
        if "order_id" in customer_view.columns else len(customer_view)
    )

    supplier_col = (
        "supplier_name" if "supplier_name" in po_view.columns
        else "supplier_id" if "supplier_id" in po_view.columns
        else None
    )

    supplier_count = (
        po_view[supplier_col].nunique()
        if supplier_col and not po_view.empty else 0
    )

    estimated_risk = lookup_metric(
        disruption_summary, "Estimated customer order value at risk"
    )

    value_series = pd.Series(dtype=float)
    if "estimated_order_value" in customer_view.columns:
        value_series = pd.to_numeric(
            customer_view["estimated_order_value"], errors="coerce"
        )

    # 2. KPI CARDS

    section_heading("Disruption Overview")

    kpi_cards([
        ("Disrupted Purchase Orders", f"{total_pos:,}", None, "amber"),
        ("Suppliers Affected", f"{supplier_count:,}"),
        ("Potentially Affected Orders", f"{total_customers:,}", None, "red"),
        (
            "Estimated Value at Risk", inr(estimated_risk),
            "Scenario estimate, not a confirmed loss", "red"
        ),
    ], per_row=4)

    # 3. SUPPLIER DISRUPTION PROFILE

    section_heading(
        "Supplier Disruption Profile",
        "Which supplier is driving the disruption and the state of its "
        "purchase orders."
    )

    profile_col, status_col = st.columns([1, 1.2], gap="large")

    with profile_col:
        with card("Supplier Concentration"):
            if supplier_col and not po_view.empty:
                supplier_counts = po_view[supplier_col].value_counts()
                primary_supplier = supplier_counts.index[0]
                primary_count = int(supplier_counts.iloc[0])
                supplier_share = primary_count / len(po_view) * 100

                country = "Not available"
                if "country" in po_view.columns:
                    country_values = (
                        po_view.loc[po_view[supplier_col] == primary_supplier, "country"]
                        .dropna().astype(str).unique()
                    )
                    if len(country_values) > 0:
                        country = country_values[0]

                st.markdown(
                    '<div style="background:#EEF4FA;border-left:4px solid #3976B9;'
                    'border-radius:6px;padding:16px;margin-top:4px;">'
                    '<div style="font-size:13px;color:#52657A;">'
                    'Primary Disrupted Supplier</div>'
                    '<div style="font-size:19px;font-weight:600;color:#203F65;'
                    f'margin-top:5px;">{esc(primary_supplier)}</div>'
                    '<div style="font-size:13px;color:#52657A;margin-top:8px;">'
                    f'Country: {esc(country)}</div>'
                    '<div style="font-size:24px;font-weight:600;color:#3976B9;'
                    f'margin-top:10px;">{primary_count:,} Purchase Orders</div>'
                    '<div style="font-size:13px;color:#52657A;">'
                    f'{supplier_share:.1f}% of disrupted PO records</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if supplier_count == 1:
                    st.caption(
                        "Only one supplier is represented in the current "
                        "disruption scenario, so a supplier comparison chart "
                        "would be misleading."
                    )
            else:
                st.info("Supplier information is not available.")

    with status_col:
        with card(
            "Purchase Order Status",
            "Status of the disrupted purchase orders."
        ):
            if "status" in po_view.columns and not po_view.empty:
                donut_compact(
                    po_view["status"].value_counts(),
                    centre_label="PO records"
                )
            else:
                st.info("Purchase order status data is unavailable.")

    # 4. CUSTOMER ORDER IMPACT

    section_heading(
        "Customer Order Impact",
        "Potentially affected customer orders by status and value."
    )

    imp_left, imp_right = st.columns(2, gap="large")

    with imp_left:
        with card(
            "Affected Orders by Status",
            "Number of potentially affected orders in each status."
        ):
            if "status" in customer_view.columns and not customer_view.empty:
                status_df = (
                    customer_view["status"].value_counts()
                    .rename_axis("status").reset_index(name="orders")
                )
                hbar_chart(
                    status_df, "status", "orders",
                    "Customer orders", fmt="%d"
                )
            else:
                st.info("Customer order status information is unavailable.")

    with imp_right:
        with card(
            "Estimated Value at Risk by Status",
            "Sum of estimated order value for each order status."
        ):
            if (
                "status" in customer_view.columns
                and value_series.notna().any()
            ):
                value_by_status = (
                    customer_view.assign(_value=value_series)
                    .groupby("status")["_value"].sum()
                    .reset_index()
                )
                hbar_chart(
                    value_by_status, "status", "_value",
                    "Estimated order value", fmt="%.0f",
                    colour=BLUE_MID
                )
            else:
                st.info("Order value information is unavailable.")

    top_left, top_right = st.columns([1.3, 1], gap="large")

    with top_left:
        with card(
            "Top 10 Affected Orders by Value",
            "Largest potentially affected orders."
        ):
            if (
                "order_id" in customer_view.columns
                and value_series.notna().any()
            ):
                top_orders = customer_view.assign(_value=value_series)[
                    ["order_id", "_value"]
                ].dropna()
                hbar_chart(
                    top_orders, "order_id", "_value",
                    "Estimated order value", fmt="%.0f",
                    highlight_colour=BAD
                )
            else:
                st.info("Order value or order ID information is unavailable.")

    with top_right:
        valid_values = value_series.dropna()
        lines = []

        if not valid_values.empty and valid_values.sum() > 0:
            top10_sum = valid_values.nlargest(10).sum()
            lines.append(
                f"Top 10 orders hold <b>{top10_sum / valid_values.sum() * 100:.1f}%</b> "
                "of the estimated value in listed orders."
            )
            lines.append(
                f"Average estimated order value: <b>{inr(valid_values.mean())}</b>."
            )
            lines.append(
                f"Largest single order: <b>{inr(valid_values.max())}</b>."
            )
        lines.append(
            "Values are scenario estimates; they do not confirm that every "
            "order will be delayed or lost."
        )
        insight_panel("Value concentration", lines)

    # 5. KEY OBSERVATIONS

    section_heading("Key Observations")

    observations = []

    if supplier_col and not po_view.empty:
        counts = po_view[supplier_col].value_counts()
        observations.append(
            f"**Supplier concentration:** {counts.index[0]} has the highest "
            f"number of disrupted purchase orders ({int(counts.iloc[0]):,}), "
            f"representing {int(counts.iloc[0]) / len(po_view) * 100:.1f}% "
            "of disrupted PO records."
        )

    if "status" in po_view.columns and not po_view.empty:
        po_status = po_view["status"].value_counts()
        observations.append(
            f"**Purchase order status:** {po_status.index[0]} is the most "
            f"common status, accounting for {int(po_status.iloc[0]):,} "
            "disrupted purchase orders."
        )

    observations.append(
        f"**Customer exposure:** {total_customers:,} customer orders are "
        "identified as potentially affected in this disruption scenario."
    )

    if "status" in customer_view.columns and not customer_view.empty:
        customer_status = customer_view["status"].value_counts()
        observations.append(
            f"**Customer order status:** {customer_status.index[0]} is the "
            "most frequent status among potentially affected orders "
            f"({int(customer_status.iloc[0]):,} records)."
        )

    observation_list(observations)

    st.caption(
        "This analysis identifies potential disruption exposure using the "
        "available dataset. It does not confirm that every affected customer "
        "order will be delayed or result in a financial loss."
    )

    # 6. DETAIL TABLES

    with st.expander("View Disrupted Purchase Order Details", expanded=False):

        po_filtered = po_view.copy()
        fc1, fc2 = st.columns(2)

        with fc1:
            if supplier_col:
                supplier_options = sorted(
                    po_filtered[supplier_col].dropna().astype(str).unique().tolist()
                )
                selected_supplier = st.selectbox(
                    "Filter by Supplier",
                    ["All Suppliers"] + supplier_options,
                    key="uc3_supplier_filter"
                )
                if selected_supplier != "All Suppliers":
                    po_filtered = po_filtered[
                        po_filtered[supplier_col].astype(str) == selected_supplier
                    ]

        with fc2:
            if "status" in po_filtered.columns:
                status_options = sorted(
                    po_filtered["status"].dropna().astype(str).unique().tolist()
                )
                selected_po_status = st.selectbox(
                    "Filter by PO Status",
                    ["All Statuses"] + status_options,
                    key="uc3_po_status_filter"
                )
                if selected_po_status != "All Statuses":
                    po_filtered = po_filtered[
                        po_filtered["status"].astype(str) == selected_po_status
                    ]

        st.caption(f"Showing {len(po_filtered):,} purchase order records.")
        st.dataframe(
            po_filtered, use_container_width=True,
            hide_index=True, height=350
        )

    with st.expander("View Potentially Affected Customer Orders", expanded=False):

        customer_filtered = customer_view.copy()

        if "status" in customer_filtered.columns:
            customer_status_options = sorted(
                customer_filtered["status"].dropna().astype(str).unique().tolist()
            )
            selected_customer_status = st.selectbox(
                "Filter by Customer Order Status",
                ["All Statuses"] + customer_status_options,
                key="uc3_customer_status_filter"
            )
            if selected_customer_status != "All Statuses":
                customer_filtered = customer_filtered[
                    customer_filtered["status"].astype(str) == selected_customer_status
                ]

        st.caption(f"Showing {len(customer_filtered):,} customer order records.")
        st.dataframe(
            customer_filtered, use_container_width=True,
            hide_index=True, height=350
        )

    if not disruption_summary.empty:
        with st.expander("View Disruption Summary Data", expanded=False):
            st.dataframe(
                disruption_summary, use_container_width=True, hide_index=True
            )
