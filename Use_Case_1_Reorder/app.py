
from pathlib import Path
import html
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="Orbix",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

from shared import *
from uc1 import render_uc1
from uc2 import render_uc2
from uc3 import render_uc3
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "integrated_dataset" / "final_dataset"

# 2. CUSTOM THEME

st.markdown("""
<style>
    :root {
        --navy: #142B49;
        --navy-light: #203F65;
        --blue: #3976B9;
        --blue-mid: #6E9AC8;
        --blue-pale: #DCE8F5;
        --canvas: #F4F7FB;
        --white: #FFFFFF;
        --ink: #203047;
        --muted: #718096;
        --line: #E3EAF2;
    }
    /* Main page */
    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: var(--canvas);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background: var(--navy);
        border-right: 1px solid #294563;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.4rem 1rem;
    }

    [data-testid="stSidebar"] * {
        color: #EAF1F8;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #EAF1F8;
        font-size: 0.94rem;
        font-weight: 550;
        padding: 0.25rem 0;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        color: #FFFFFF;
    }

    [data-testid="stSidebar"] hr {
        border-color: #36516E;
    }

    /* Orbix brand */
    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 0.2rem 0 1.2rem 0;
    }

    .brand-mark {
        width: 39px;
        height: 39px;
        border: 1px solid #8FB4D9;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #203F65;
    }

    .brand-name {
        color: #FFFFFF;
        font-size: 1.42rem;
        font-weight: 750;
        letter-spacing: 0.3px;
    }

    .brand-caption {
        color: #AFC2D8;
        font-size: 0.72rem;
        margin-top: 2px;
    }

    /* Page headings */
    h1, h2, h3 {
        color: var(--navy);
        letter-spacing: -0.025em;
    }

    h2 {
        font-size: 1.32rem;
        font-weight: 700;
    }

    h3 {
        font-size: 1.03rem;
        font-weight: 650;
    }

    .main-title {
        font-size: 1.9rem;
        font-weight: 750;
        color: var(--navy);
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 0.94rem;
        color: var(--muted);
        margin-bottom: 1.5rem;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-left: 4px solid var(--blue);
        border-radius: 10px;
        padding: 15px 17px;
        min-height: 105px;
        box-shadow: 0 2px 7px rgba(20, 43, 73, 0.045);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: var(--navy);
        font-size: 1.65rem;
        font-weight: 750;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }

    /* Content panels */
    .section-panel {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 17px 19px;
        box-shadow: 0 2px 8px rgba(20, 43, 73, 0.035);
        margin-bottom: 14px;
    }

    /* Filters */
    div[data-baseweb="select"] > div {
        background: #FFFFFF;
        border: 1px solid #D6E0EB;
        border-radius: 8px;
    }

    /* Tables */
    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.83rem;
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 9px;
        overflow: hidden;
    }

    .data-table th {
        background: #EAF1F8;
        color: var(--navy);
        text-align: left;
        font-weight: 700;
        padding: 11px 12px;
        border-bottom: 1px solid #DCE5EF;
        white-space: nowrap;
    }

    .data-table td {
        color: #34445A;
        padding: 10px 12px;
        border-bottom: 1px solid #EDF1F6;
        white-space: nowrap;
    }

    .data-table tr:nth-child(even) {
        background: #F8FAFD;
    }

    .data-table tr:last-child td {
        border-bottom: none;
    }

    .table-container {
        width: 100%;
        overflow-x: auto;
        border-radius: 9px;
        margin: 8px 0 16px 0;
    }

    /* Buttons and separators */
    .stButton button {
        border-radius: 8px;
        border: 1px solid #C9D7E6;
        font-weight: 600;
    }

    hr {
        border-color: var(--line);
        margin: 1.3rem 0;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 3. LOAD DATA FILES

@st.cache_data
def load_csv(path):
    if path.exists():
        df = pd.read_csv(path, encoding="utf-8-sig")
        df.columns = df.columns.str.strip()
        return df

    return pd.DataFrame()

# UC1 outputs
supplier_performance = load_csv(
    BASE_DIR / "supplier_performance.csv"
)

reorder_alerts = load_csv(
    BASE_DIR / "reorder_alerts.csv"
)

product_inventory = load_csv(
    BASE_DIR / "product_inventory_summary.csv"
)

# UC2 outputs
outbound_analysis = load_csv(
    BASE_DIR / "outbound_delay_analysis.csv"
)

warehouse_performance = load_csv(
    BASE_DIR / "warehouse_performance.csv"
)

delivery_summary = load_csv(
    BASE_DIR / "delivery_delay_summary.csv"
)


# UC3 outputs
disrupted_pos = load_csv(
    BASE_DIR / "disrupted_purchase_orders.csv"
)

affected_orders = load_csv(
    BASE_DIR / "potentially_affected_customer_orders.csv"
)

disruption_summary = load_csv(
    BASE_DIR / "disruption_summary.csv"
)


# Master datasets
products = load_csv(DATA_DIR / "products_final.csv")
suppliers = load_csv(DATA_DIR / "suppliers_final.csv")
inventory = load_csv(DATA_DIR / "inventory_final.csv")
outbound = load_csv(DATA_DIR / "sales_orders_final.csv")
purchase_orders = load_csv(DATA_DIR / "purchase_orders_final.csv")

# 6. SIDEBAR NAVIGATION  (V2 LAYOUT)

import matplotlib as mpl
from contextlib import contextmanager

EXTRA_CSS = """
<style>
    .kpi {
        background: #FFFFFF;
        border: 1px solid #E3EAF2;
        border-left: 4px solid #3976B9;
        border-radius: 10px;
        padding: 13px 16px;
        min-height: 94px;
        box-shadow: 0 2px 7px rgba(20, 43, 73, 0.045);
        margin-bottom: 10px;
    }
    .kpi-label {
        color: #718096;
        font-size: 0.72rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.045em;
    }
    .kpi-value {
        color: #142B49;
        font-size: 1.55rem;
        font-weight: 750;
        line-height: 1.25;
        margin-top: 3px;
    }
    .kpi-sub {
        color: #718096;
        font-size: 0.76rem;
        margin-top: 2px;
    }
    .section-title {
        color: #142B49;
        font-size: 1.12rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 0.6rem 0 0.05rem 0;
        padding-left: 10px;
        border-left: 4px solid #3976B9;
    }
    .section-sub {
        color: #718096;
        font-size: 0.82rem;
        margin: 0 0 0.7rem 14px;
    }
    .card-title {
        color: #142B49;
        font-size: 0.95rem;
        font-weight: 700;
    }
    .card-caption {
        color: #718096;
        font-size: 0.76rem;
        margin-bottom: 4px;
    }
    .callout {
        background: #EEF4FA;
        border-left: 4px solid #3976B9;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 0.86rem;
        color: #34445A;
        margin: 6px 0 10px 0;
    }
    .callout-warn {
        background: #FDF3E7;
        border-left-color: #D9822B;
    }
    .obs-item {
        background: #FFFFFF;
        border: 1px solid #E3EAF2;
        border-radius: 8px;
        padding: 9px 14px;
        margin-bottom: 7px;
        font-size: 0.87rem;
        color: #34445A;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E3EAF2;
        border-radius: 10px;
    }
</style>
"""

st.markdown(EXTRA_CSS, unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="brand">
    <div class="brand-mark">
        <svg width="25" height="25" viewBox="0 0 24 24"
             fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3.5 7.5L12 3L20.5 7.5L12 12L3.5 7.5Z"
                  stroke="#DCE8F5" stroke-width="1.6"
                  stroke-linejoin="round"/>
            <path d="M3.5 7.5V16.5L12 21L20.5 16.5V7.5"
                  stroke="#DCE8F5" stroke-width="1.6"
                  stroke-linejoin="round"/>
            <path d="M12 12V21"
                  stroke="#8FB4D9" stroke-width="1.6"/>
        </svg>
    </div>
    <div>
        <div class="brand-name">Orbix</div>
        <div class="brand-caption">Supply Chain Analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "UC1 - Inbound Reorder",
        "UC2 - Outbound Deliveries",
        "UC3 - Supplier Control Tower"
    ]
)

# 7. OVERVIEW

if page == "Overview":

    page_header(
        "Dashboard",
        "A consolidated view of inventory, supplier performance, "
        "customer deliveries and disruption risk."
    )
    
    # 1. FIGURES
    
    total_pos = len(purchase_orders)
    total_suppliers = len(suppliers)
    total_products = len(products)
    total_customer_orders = len(outbound)
    total_reorder_alerts = len(reorder_alerts)

    delayed_delivery = on_time_delivery = unknown_delivery = 0

    if (
        not outbound_analysis.empty
        and "delivery_status" in outbound_analysis.columns
    ):
        status_clean = (
            outbound_analysis["delivery_status"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )
        status_counts = status_clean.value_counts()

        delayed_delivery = int(status_counts.get("Delayed", 0))
        on_time_delivery = int(status_counts.get("On Time", 0))
        unknown_delivery = int(status_counts.get("Unknown", 0))

    analysed_orders = delayed_delivery + on_time_delivery + unknown_delivery
    known_orders = delayed_delivery + on_time_delivery

    delay_pct = (
        delayed_delivery / analysed_orders * 100 if analysed_orders else 0
    )
    on_time_rate = (
        on_time_delivery / known_orders * 100 if known_orders else None
    )

    average_total_days = lookup_metric(
        delivery_summary, "Average total delivery days"
    )
    estimated_risk = lookup_metric(
        disruption_summary, "Estimated customer order value at risk"
    )

    disrupted_po_count = len(disrupted_pos)
    affected_customer_count = len(affected_orders)

    # 2. KPI CARDS

    kpi_cards([
        ("Purchase Orders", f"{total_pos:,}"),
        ("Suppliers", f"{total_suppliers:,}"),
        ("Products", f"{total_products:,}"),
        ("Customer Orders", f"{total_customer_orders:,}"),
        (
            "Reorder Alerts", f"{total_reorder_alerts:,}",
            "Inventory records flagged", "amber"
        ),
    ], per_row=5)

    kpi_cards([
        (
            "On-Time Delivery Rate",
            f"{on_time_rate:.1f}%" if on_time_rate is not None else "N/A",
            f"{on_time_delivery:,} of {known_orders:,} orders with a known status",
            "green"
        ),
        (
            "Delayed Deliveries", f"{delayed_delivery:,}",
            f"{delay_pct:.1f}% of {analysed_orders:,} analysed orders",
            "amber"
        ),
        (
            "Avg Total Delivery Time",
            f"{average_total_days:.2f} days"
            if average_total_days is not None else "N/A",
            "Order placed to delivered"
        ),
        (
            "Orders at Risk (Scenario)", f"{affected_customer_count:,}",
            f"{inr(estimated_risk)} estimated value" if estimated_risk else None,
            "red"
        ),
    ], per_row=4)

    # 3. INVENTORY AND DELIVERY HEALTH

    section_heading(
        "Inventory and Delivery Health",
        "Current stock position and customer delivery outcomes."
    )

    health_left, health_right = st.columns(2, gap="large")

    with health_left:
        with card(
            "Inventory Health",
            "Latest stock per product and warehouse against safety stock "
            "and reorder point."
        ):
            health = prepare_inventory_health(inventory)

            if not health.empty:
                donut_compact(
                    health["inventory_status"].value_counts(),
                    HEALTH_COLOURS,
                    "stock positions"
                )
                critical = int((health["inventory_status"] == "Critical").sum())
                if critical:
                    st.caption(
                        f"{critical:,} stock positions are at or below "
                        "safety stock."
                    )
            else:
                st.info("Inventory health data is unavailable.")

    with health_right:
        with card(
            "Customer Delivery Status",
            "Share of analysed orders delivered on time or late."
        ):
            if analysed_orders > 0:
                donut_compact(
                    pd.Series({
                        "On Time": on_time_delivery,
                        "Delayed": delayed_delivery,
                        "Unknown": unknown_delivery,
                    }),
                    DELIVERY_COLOURS,
                    "orders"
                )
            else:
                st.info("Delivery status data is unavailable.")

    # 4. SUPPLIER RELIABILITY
    
    section_heading(
        "Supplier Reliability",
        "How often suppliers deliver on time and how far actual lead "
        "times drift from expectations."
    )

    supplier_left, supplier_right = st.columns(2, gap="large")

    supplier_chart_data = supplier_performance.copy()

    for col in [
        "average_lead_time", "average_expected_lead_time",
        "late_orders", "total_orders"
    ]:
        if col in supplier_chart_data.columns:
            supplier_chart_data[col] = pd.to_numeric(
                supplier_chart_data[col], errors="coerce"
            )

    with supplier_left:
        with card(
            "On-Time Delivery Rate by Supplier",
            "Purchase orders not delivered late, as a percentage of total."
        ):
            if {"supplier_name", "late_orders", "total_orders"}.issubset(
                supplier_chart_data.columns
            ):
                rate_data = supplier_chart_data[
                    supplier_chart_data["total_orders"] > 0
                ].copy()
                rate_data["on_time_rate"] = (
                    1 - rate_data["late_orders"] / rate_data["total_orders"]
                ) * 100

                hbar_chart(
                    rate_data, "supplier_name", "on_time_rate",
                    "On-time rate (%)", fmt="%.1f%%",
                    highlight=False, colour=BLUE
                )
            else:
                st.info("Supplier order counts are unavailable.")

    with supplier_right:
        with card(
            "Lead-Time Variance by Supplier",
            "Positive values mean deliveries arrive later than expected."
        ):
            variance_chart(
                supplier_chart_data, "supplier_name",
                "average_lead_time", "average_expected_lead_time"
            )

    # 5. WAREHOUSES AND DISRUPTION

    section_heading(
        "Warehouses and Disruption Scenario",
        "Fulfilment speed by warehouse and the modelled supplier "
        "disruption exposure."
    )

    wh_left, wh_right = st.columns([1.3, 1], gap="large")

    with wh_left:
        with card(
            "Average Total Delivery Time by Warehouse",
            "Slowest warehouse highlighted; dashed line is the simple "
            "average across warehouses."
        ):
            wh_data = warehouse_performance.copy()

            if "average_total_days" in wh_data.columns:
                wh_data["average_total_days"] = pd.to_numeric(
                    wh_data["average_total_days"], errors="coerce"
                )
                hbar_chart(
                    wh_data, "warehouse_id", "average_total_days",
                    "Average delivery time (days)", fmt="%.2f",
                    highlight_colour=WARN,
                    ref_line=wh_data["average_total_days"].mean(),
                    ref_label="Warehouse average"
                )
            else:
                st.info("Warehouse performance data is unavailable.")

    with wh_right:
        with card(
            "Supplier Disruption Impact",
            "Scenario-based estimate, not a confirmed financial loss."
        ):
            kpi_cards([
                ("Disrupted POs", f"{disrupted_po_count:,}", None, "amber"),
                (
                    "Affected Orders", f"{affected_customer_count:,}",
                    None, "red"
                ),
            ], per_row=2)

            kpi_cards([
                (
                    "Estimated Value at Risk", inr(estimated_risk),
                    "Customer order value in scenario", "red"
                ),
            ], per_row=1)

            if not disruption_summary.empty:
                assumptions = []
                for _, row in disruption_summary.iterrows():
                    name = str(row["Metric"]).strip()
                    if name in ["Disrupted supplier", "Additional delay in days"]:
                        assumptions.append(
                            f"<b>{esc(name)}:</b> {esc(str(row['Value']).strip())}"
                        )
                if assumptions:
                    callout("<br>".join(assumptions))

    # 6. OPERATIONAL TABLES

    section_heading("Operational Highlights")

    tab1, tab2 = st.tabs(
        ["Suppliers with Most Late Orders", "Warehouse Performance"]
    )

    with tab1:
        if (
            not supplier_performance.empty
            and "late_orders" in supplier_performance.columns
        ):
            late_view = supplier_performance.copy()
            late_view["late_orders"] = pd.to_numeric(
                late_view["late_orders"], errors="coerce"
            )
            st.dataframe(
                late_view.sort_values("late_orders", ascending=False).head(10),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Supplier late-order information is unavailable.")

    with tab2:
        if warehouse_performance.empty:
            st.info("Warehouse performance data is unavailable.")
        else:
            st.dataframe(
                warehouse_performance.head(10),
                use_container_width=True, hide_index=True
            )

    st.caption(
        "Operational figures are based on the supplied analysis outputs. "
        "Supplier disruption figures are scenario-based estimates."
    )

# 8. UC1 - INBOUND REORDER

elif page == "UC1 - Inbound Reorder":
    render_uc1(reorder_alerts, supplier_performance, product_inventory)

# 9. UC2 - OUTBOUND DELIVERIES

elif page == "UC2 - Outbound Deliveries":
    render_uc2(delivery_summary, outbound_analysis, warehouse_performance)

# 10. UC3 - SUPPLIER CONTROL TOWER

elif page == "UC3 - Supplier Control Tower":
    render_uc3(disrupted_pos, affected_orders, disruption_summary)
