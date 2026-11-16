import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from shared import *


def render_uc2(delivery_summary, outbound_analysis, warehouse_performance):

    page_header(
        "Outbound Delivery Analysis",
        "Track customer order fulfilment, evaluate warehouse performance "
        "and identify delivery delays."
    )

    if delivery_summary.empty or outbound_analysis.empty:
        st.error("UC2 output files are missing. Run uc2_analysis.py first.")
        st.stop()

    # 1. PREPARE DATA

    outbound_view = outbound_analysis.copy()
    warehouse_view = warehouse_performance.copy()

    for col in ["processing_status", "delivery_status"]:
        if col in outbound_view.columns:
            outbound_view[col] = (
                outbound_view[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .str.title()
            )

    if "warehouse_id" in outbound_view.columns:
        outbound_view["warehouse_id"] = (
            outbound_view["warehouse_id"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    if "average_total_days" in warehouse_view.columns:
        warehouse_view["average_total_days"] = pd.to_numeric(
            warehouse_view["average_total_days"], errors="coerce"
        )

    days_col = find_days_column(outbound_view)
    processing_col, shipping_col = find_stage_columns(outbound_view)

    # 2. SUMMARY

    section_heading("Delivery Performance Summary")
    summary_cards(delivery_summary, per_row=4)

    # 3. DELIVERY OUTCOMES

    section_heading(
        "Delivery Outcomes",
        "Overall on-time performance and the speed of each warehouse."
    )

    out_left, out_right = st.columns(2, gap="large")

    with out_left:
        with card(
            "Customer Delivery Status",
            "Share of orders delivered on time or late."
        ):
            if "delivery_status" in outbound_view.columns:
                donut_compact(
                    outbound_view["delivery_status"].value_counts(),
                    DELIVERY_COLOURS, "orders"
                )
            else:
                st.info("Delivery status information is unavailable.")

    with out_right:
        with card(
            "Average Total Delivery Time by Warehouse",
            "Slowest warehouse highlighted; dashed line is the simple "
            "average across warehouses."
        ):
            if {"warehouse_id", "average_total_days"}.issubset(
                warehouse_view.columns
            ):
                hbar_chart(
                    warehouse_view, "warehouse_id", "average_total_days",
                    "Average delivery time (days)", fmt="%.1f",
                    highlight_colour=WARN,
                    ref_line=warehouse_view["average_total_days"].mean(),
                    ref_label="Warehouse average"
                )
            else:
                st.info("Warehouse delivery-time information is unavailable.")

    # 4. DELAY HOTSPOTS

    section_heading(
        "Delay Hotspots",
        "Where delivery outcomes and processing status differ most."
    )

    hot_left, hot_right = st.columns(2, gap="large")

    delayed_share = pd.DataFrame()

    with hot_left:
        with card(
            "Delivery Outcome Mix by Warehouse",
            "Share of each warehouse's orders by delivery status; "
            "most delay-prone warehouses at the top."
        ):
            if {"warehouse_id", "delivery_status"}.issubset(outbound_view.columns):
                mix = pd.crosstab(
                    outbound_view["warehouse_id"],
                    outbound_view["delivery_status"]
                )
                delayed_share = mix.div(mix.sum(axis=1), axis=0) * 100

                preferred = [
                    c for c in ["On Time", "Delayed", "Unknown"]
                    if c in delayed_share.columns
                ]
                others = [c for c in delayed_share.columns if c not in preferred]
                delayed_share = delayed_share[preferred + others]

                sort_column = (
                    "Delayed" if "Delayed" in delayed_share.columns
                    else delayed_share.columns[0]
                )
                delayed_share = delayed_share.sort_values(sort_column, ascending=True)

                stacked_bar_chart(delayed_share, DELIVERY_COLOURS, percent=True)
            else:
                st.info("Warehouse delivery outcome data is unavailable.")

    with hot_right:
        with card(
            "Orders by Processing Status",
            "Where orders currently sit in the fulfilment pipeline."
        ):
            if "processing_status" in outbound_view.columns:
                processing_counts = (
                    outbound_view["processing_status"]
                    .value_counts()
                    .rename_axis("status")
                    .reset_index(name="orders")
                )
                hbar_chart(
                    processing_counts, "status", "orders",
                    "Number of orders", fmt="%d", top_n=8
                )
            else:
                st.info("Processing status information is unavailable.")

    # 5. DELIVERY TIME DISTRIBUTION (only when a total-days column exists)
    if days_col:

        section_heading(
            "Delivery Time Distribution",
            "Averages hide spread: these charts show how long individual "
            "orders actually take."
        )

        dist_left, dist_right = st.columns(2, gap="large")

        with dist_left:
            with card(
                "Distribution of Total Delivery Time",
                "Each bar counts orders in a delivery-time range."
            ):
                hist_chart(outbound_view[days_col], "Total delivery time (days)")

        with dist_right:
            with card(
                "Delivery Time Spread by Warehouse",
                "Box = middle 50% of orders; line = median. "
                "Slowest medians at the top."
            ):
                if "warehouse_id" in outbound_view.columns:
                    box_chart(
                        outbound_view, "warehouse_id", days_col,
                        "Total delivery time (days)"
                    )
                else:
                    st.info("Warehouse information is unavailable.")

    if processing_col and shipping_col and "warehouse_id" in outbound_view.columns:

        section_heading(
            "Where Delivery Time Is Spent",
            "Average days in order processing versus shipping."
        )

        stage_data = outbound_view[
            ["warehouse_id", processing_col, shipping_col]
        ].copy()
        stage_data[processing_col] = pd.to_numeric(stage_data[processing_col], errors="coerce")
        stage_data[shipping_col] = pd.to_numeric(stage_data[shipping_col], errors="coerce")

        stage_avg = stage_data.groupby("warehouse_id")[
            [processing_col, shipping_col]
        ].mean().dropna()

        if not stage_avg.empty:
            stage_avg.columns = ["Processing", "Shipping"]
            stage_avg["total"] = stage_avg.sum(axis=1)
            stage_avg = stage_avg.sort_values("total").drop(columns="total")

            stage_left, stage_right = st.columns([1.3, 1], gap="large")

            with stage_left:
                with card(
                    "Average Days by Stage and Warehouse",
                    "Processing and shipping time stacked per warehouse."
                ):
                    stacked_bar_chart(
                        stage_avg,
                        {"Processing": BLUE_MID, "Shipping": BLUE_DARK},
                        percent=False, xlabel="Average days"
                    )

            with stage_right:
                total_stage = stage_avg.sum().sum()
                lines = []
                if total_stage > 0:
                    proc_share = stage_avg["Processing"].sum() / total_stage * 100
                    lines.append(
                        f"Processing accounts for <b>{proc_share:.0f}%</b> and "
                        f"shipping <b>{100 - proc_share:.0f}%</b> of average "
                        "delivery time across warehouses."
                    )
                    slowest_stage_wh = stage_avg.sum(axis=1).idxmax()
                    lines.append(
                        f"Longest combined time: warehouse "
                        f"<b>{esc(slowest_stage_wh)}</b>."
                    )
                insight_panel("What this means", lines)

    # 6. KEY OBSERVATIONS

    section_heading("Key Observations")

    observations = []

    if {"warehouse_id", "average_total_days"}.issubset(warehouse_view.columns):
        ranked = warehouse_view.dropna(subset=["average_total_days"]).sort_values(
            "average_total_days"
        )
        if len(ranked) >= 2:
            fastest = ranked.iloc[0]
            slowest = ranked.iloc[-1]
            observations.append(
                f"**Warehouse speed:** {fastest['warehouse_id']} is fastest "
                f"({fastest['average_total_days']:.1f} days on average); "
                f"{slowest['warehouse_id']} is slowest "
                f"({slowest['average_total_days']:.1f} days)."
            )

    if "delivery_status" in outbound_view.columns and len(outbound_view):
        delayed_pct = (outbound_view["delivery_status"] == "Delayed").mean() * 100
        observations.append(
            f"**Delivery delays:** {delayed_pct:.1f}% of "
            f"{len(outbound_view):,} customer orders are delayed."
        )

    if not delayed_share.empty and "Delayed" in delayed_share.columns:
        observations.append(
            f"**Delay hotspot:** warehouse {delayed_share['Delayed'].idxmax()} "
            f"has the highest share of delayed orders "
            f"({delayed_share['Delayed'].max():.1f}%)."
        )

    if days_col:
        days_values = pd.to_numeric(outbound_view[days_col], errors="coerce").dropna()
        if not days_values.empty:
            observations.append(
                f"**Delivery spread:** median delivery takes "
                f"{days_values.median():.1f} days; the slowest 10% of orders "
                f"take {days_values.quantile(0.9):.1f} days or more."
            )

    if "processing_status" in outbound_view.columns and len(outbound_view):
        top_processing = outbound_view["processing_status"].value_counts()
        observations.append(
            f"**Processing:** {top_processing.index[0]} is the most common "
            f"processing status ({int(top_processing.iloc[0]):,} orders)."
        )

    observation_list(observations)

    st.caption(
        "Note: The dataset provides order, shipment and delivery dates. It "
        "does not contain separate transport checkpoints, so first-mile, "
        "middle-mile and last-mile delays cannot be measured individually."
    )

    # 7. DETAIL TABLES

    with st.expander("View Warehouse Performance Records", expanded=False):
        st.dataframe(
            warehouse_view, use_container_width=True,
            hide_index=True, height=300
        )

    with st.expander("View Customer Order Details", expanded=False):

        f1, f2, f3 = st.columns(3)

        with f1:
            warehouse_options = (
                ["All"] + sorted(
                    outbound_view["warehouse_id"].dropna().astype(str).unique().tolist()
                )
                if "warehouse_id" in outbound_view.columns else ["All"]
            )
            selected_warehouse = st.selectbox(
                "Warehouse", warehouse_options, key="uc2_warehouse_filter"
            )

        with f2:
            processing_options = (
                ["All"] + sorted(outbound_view["processing_status"].dropna().unique().tolist())
                if "processing_status" in outbound_view.columns else ["All"]
            )
            selected_processing = st.selectbox(
                "Processing status", processing_options, key="uc2_processing_filter"
            )

        with f3:
            delivery_options = (
                ["All"] + sorted(outbound_view["delivery_status"].dropna().unique().tolist())
                if "delivery_status" in outbound_view.columns else ["All"]
            )
            selected_delivery = st.selectbox(
                "Delivery status", delivery_options, key="uc2_delivery_filter"
            )

        filtered_outbound = outbound_view.copy()

        if selected_warehouse != "All" and "warehouse_id" in filtered_outbound.columns:
            filtered_outbound = filtered_outbound[
                filtered_outbound["warehouse_id"].astype(str) == selected_warehouse
            ]

        if selected_processing != "All" and "processing_status" in filtered_outbound.columns:
            filtered_outbound = filtered_outbound[
                filtered_outbound["processing_status"] == selected_processing
            ]

        if selected_delivery != "All" and "delivery_status" in filtered_outbound.columns:
            filtered_outbound = filtered_outbound[
                filtered_outbound["delivery_status"] == selected_delivery
            ]

        st.caption(
            f"Showing {len(filtered_outbound):,} of {len(outbound_view):,} customer orders."
        )
        st.dataframe(
            filtered_outbound, use_container_width=True,
            hide_index=True, height=350
        )
