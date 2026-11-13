
from pathlib import Path
import html

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=" ",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "integrated_dataset" / "final_dataset"

 
# ============================================================
# 2. CUSTOM THEME
# ============================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(180deg, #F8FBFF 0%, #F1F5FB 100%);
    color: #1E293B;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 100%);
    border-right: 1px solid #DBEAFE;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Headings */
h1, h2, h3 {
    color: #172554;
    font-weight: 650;
}

.main-title {
    font-size: 32px;
    font-weight: 750;
    color: #172554;
    margin-bottom: 7px;
    letter-spacing: -0.6px;
}

.subtitle {
    color: #64748B;
    font-size: 15px;
    margin-bottom: 26px;
}

/* Section headings */
[data-testid="stSubheader"] {
    color: #172554;
    font-weight: 650;
}

h2, h3 {
    color: #1E3A8A;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #F0F7FF);
    border: 1px solid #DBEAFE;
    border-top: 4px solid #3B82F6;
    padding: 18px 20px;
    border-radius: 13px;
    box-shadow: 0 3px 10px rgba(30, 64, 175, 0.06);
    transition: 0.2s ease;
}

div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-size: 13px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #1D4ED8;
    font-size: 27px;
    font-weight: 750;
}

/* KPI card accent colours */
div[data-testid="stHorizontalBlock"] > div:nth-child(2)
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #ECFDF5);
    border-color: #D1FAE5;
    border-top-color: #10B981;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2)
[data-testid="stMetricValue"] {
    color: #047857;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(3)
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #F5F3FF);
    border-color: #EDE9FE;
    border-top-color: #8B5CF6;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(3)
[data-testid="stMetricValue"] {
    color: #6D28D9;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(4)
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #FFF7ED);
    border-color: #FFEDD5;
    border-top-color: #F59E0B;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(4)
[data-testid="stMetricValue"] {
    color: #C2410C;
}

/* Tables */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    background-color: #FFFFFF;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(30, 64, 175, 0.04);
}

.data-table th {
    background-color: #EAF1FB;
    color: #1E3A8A;
    text-align: left;
    padding: 12px;
    border: 1px solid #DCE5F0;
    white-space: nowrap;
    font-weight: 650;
}

.data-table td {
    color: #334155;
    padding: 11px;
    border: 1px solid #E2E8F0;
    white-space: nowrap;
}

.data-table tr:nth-child(even) {
    background-color: #F8FAFC;
}

.table-container {
    width: 100%;
    overflow-x: auto;
    border-radius: 10px;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-radius: 8px;
    border-color: #CBD5E1;
}

/* Buttons */
.stButton button {
    border-radius: 8px;
}

/* Dividers */
hr {
    border-color: #DCE7F5;
    margin-top: 24px;
    margin-bottom: 24px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. LOAD DATA FILES
# ============================================================

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


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def show_table(df, max_rows=30):

    if df is None or df.empty:
        st.info("No records available.")
        return

    display = df.head(max_rows).copy()

    headers = "".join(
        f"<th>{html.escape(str(col))}</th>"
        for col in display.columns
    )

    rows = []

    for _, row in display.iterrows():

        cells = []

        for value in row:

            if pd.isna(value):
                value = "-"

            elif isinstance(value, float):
                value = round(value, 2)

            cells.append(
                f"<td>{html.escape(str(value))}</td>"
            )

        rows.append(
            "<tr>" + "".join(cells) + "</tr>"
        )

    st.markdown(
        '<div class="table-container"><table class="data-table">'
        f"<thead><tr>{headers}</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table></div>",
        unsafe_allow_html=True
    )


def metric_number(df):
    return 0 if df.empty else len(df)


def make_chart():

    fig, ax = plt.subplots(figsize=(9, 4.5))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#E2E8F0")
    ax.spines["bottom"].set_color("#E2E8F0")

    ax.tick_params(colors="#475569", labelsize=9)

    ax.grid(
        axis="y",
        color="#E2E8F0",
        linestyle="--",
        linewidth=0.7,
        alpha=0.8
    )

    ax.set_axisbelow(True)

    return fig, ax


def show_bar_chart(
    df,
    label_col,
    value_col,
    title,
    xlabel
):

    if (
        df.empty
        or label_col not in df.columns
        or value_col not in df.columns
    ):
        st.info("Chart data is not available.")
        return

    chart_data = df[[label_col, value_col]].copy()

    chart_data[value_col] = pd.to_numeric(
        chart_data[value_col],
        errors="coerce"
    )

    chart_data = chart_data.dropna()

    chart_data = chart_data.sort_values(
        value_col,
        ascending=False
    )

    if chart_data.empty:
        st.info("No numeric data available for this chart.")
        return

    fig, ax = make_chart()

    palette = [
        "#3B82F6",
        "#14B8A6",
        "#8B5CF6",
        "#F59E0B",
        "#EC4899",
        "#06B6D4",
        "#6366F1",
        "#84CC16"
    ]

    colors = [
        palette[i % len(palette)]
        for i in range(len(chart_data))
    ]

    bars = ax.bar(
        chart_data[label_col].astype(str),
        chart_data[value_col],
        color=colors,
        width=0.65,
        edgecolor="white",
        linewidth=0.8
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color="#172554",
        pad=18
    )

    ax.set_xlabel(
        xlabel,
        color="#64748B",
        fontsize=10
    )

    ax.set_ylabel(
        "Value",
        color="#64748B",
        fontsize=10
    )

    ax.tick_params(axis="x", rotation=30)

    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    ax.bar_label(
        bars,
        fmt="%.1f",
        padding=4,
        fontsize=8,
        color="#334155"
    )

    ax.margins(y=0.15)
    fig.tight_layout()

    st.pyplot(fig, width="stretch")
    plt.close(fig)


def show_donut_chart(df, category_col, title):

    if df.empty or category_col not in df.columns:
        st.info("Chart data is not available.")
        return

    counts = (
        df[category_col]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )

    if counts.empty:
        st.info("No category data available.")
        return

    palette = [
        "#3B82F6",
        "#14B8A6",
        "#8B5CF6",
        "#F59E0B",
        "#EC4899",
        "#06B6D4",
        "#6366F1",
        "#84CC16"
    ]

    fig, ax = make_chart()

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        colors=palette[:len(counts)],
        wedgeprops={
            "width": 0.42,
            "edgecolor": "white",
            "linewidth": 2
        },
        textprops={
            "color": "#334155",
            "fontsize": 9
        }
    )

    for text_item in autotexts:
        text_item.set_fontsize(9)
        text_item.set_fontweight("bold")
        text_item.set_color("#FFFFFF")

    ax.text(
        0,
        0,
        f"{counts.sum():,}",
        ha="center",
        va="center",
        fontsize=19,
        fontweight="bold",
        color="#172554"
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color="#172554",
        pad=18
    )

    ax.axis("equal")
    fig.tight_layout()

    st.pyplot(fig, width="stretch")
    plt.close(fig)


def show_summary_metrics(df):

    if (
        df.empty
        or "Metric" not in df.columns
        or "Value" not in df.columns
    ):
        st.info("Summary metrics are unavailable.")
        return

    for start in range(0, len(df), 3):

        cols = st.columns(3)

        for col, (_, row) in zip(
            cols,
            df.iloc[start:start + 3].iterrows()
        ):

            value = row["Value"]

            with col:
                st.metric(
                    str(row["Metric"]),
                    str(value)
                )


# ============================================================
# 5. INVENTORY HEALTH PREPARATION
# ============================================================

def prepare_inventory_health(df):

    required_columns = [
        "product_id",
        "warehouse_id",
        "date",
        "stock_on_hand",
        "reorder_point",
        "safety_stock"
    ]

    if (
        df.empty
        or not all(col in df.columns for col in required_columns)
    ):
        return pd.DataFrame()

    data = df[required_columns].copy()

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    for col in [
        "stock_on_hand",
        "reorder_point",
        "safety_stock"
    ]:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

    # Keep the latest record for each product and warehouse
    if data["date"].notna().any():
        data = data.dropna(subset=["date"])
        data = data.sort_values("date")

    data = data.drop_duplicates(
        subset=["product_id", "warehouse_id"],
        keep="last"
    )

    data["inventory_status"] = "Unknown"

    valid = (
        data["stock_on_hand"].notna()
        & data["reorder_point"].notna()
        & data["safety_stock"].notna()
    )

    critical = valid & (
        data["stock_on_hand"] <= data["safety_stock"]
    )

    low = valid & (
        (data["stock_on_hand"] > data["safety_stock"])
        & (data["stock_on_hand"] <= data["reorder_point"])
    )

    healthy = valid & (
        data["stock_on_hand"] > data["reorder_point"]
    )

    data.loc[critical, "inventory_status"] = "Critical"
    data.loc[low, "inventory_status"] = "Low"
    data.loc[healthy, "inventory_status"] = "Healthy"

    return data


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "UC1 - Inbound Reorder",
        "UC2 - Outbound Deliveries",
        "UC3 - Supplier Control Tower"
    ]
)


# ============================================================
# 7. OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="main-title">Supply Chain Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Unified view of inbound inventory, '
        'outbound deliveries and supplier disruptions.</div>',
        unsafe_allow_html=True
    )

    st.subheader("Overall Supply Chain Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Purchase Orders",
        f"{len(purchase_orders):,}"
    )

    c2.metric(
        "Suppliers",
        f"{metric_number(suppliers):,}"
    )

    c3.metric(
        "Products",
        f"{metric_number(products):,}"
    )

    c4.metric(
        "Customer Orders",
        f"{metric_number(outbound):,}"
    )

    st.markdown("---")
    st.subheader("Use Case Highlights")

    a, b, c = st.columns(3)

    with a:

        st.markdown("### 1. Inbound Reorder")

        st.metric(
            "Reorder Alerts",
            f"{metric_number(reorder_alerts):,}"
        )

        st.metric(
            "Suppliers Analyzed",
            f"{metric_number(supplier_performance):,}"
        )

        st.caption(
            "Supplier performance and inventory replenishment."
        )

    with b:

        st.markdown("### 2. Outbound Deliveries")

        if (
            not delivery_summary.empty
            and "Metric" in delivery_summary.columns
        ):

            delayed = delivery_summary.loc[
                delivery_summary["Metric"]
                == "Delivery delayed orders",
                "Value"
            ]

            st.metric(
                "Delivery Delays",
                (
                    f"{int(float(delayed.iloc[0])):,}"
                    if not delayed.empty
                    else "N/A"
                )
            )

        else:
            st.metric("Delivery Delays", "N/A")

        st.metric(
            "Warehouses Analyzed",
            f"{metric_number(warehouse_performance):,}"
        )

        st.caption(
            "Order processing and delivery performance."
        )

    with c:

        st.markdown("### 3. Supplier Control Tower")

        st.metric(
            "Affected Purchase Orders",
            f"{metric_number(disrupted_pos):,}"
        )

        st.metric(
            "Potentially Affected Customer Orders",
            f"{metric_number(affected_orders):,}"
        )

        st.caption(
            "Supplier disruption impact simulation."
        )

    st.markdown("---")
    st.subheader("Supply Chain Status Overview")

    chart1, chart2 = st.columns(2)

    with chart1:

        show_donut_chart(
            reorder_alerts,
            "reorder_status",
            "Inventory Reorder Status"
        )

    with chart2:

        show_donut_chart(
            outbound_analysis,
            "delivery_status",
            "Customer Delivery Status"
        )


# ============================================================
# 8. UC1 - INBOUND REORDER
# ============================================================

elif page == "UC1 - Inbound Reorder":

    st.markdown(
        '<div class="main-title">Inbound Reorder Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Supplier delivery performance, '
        'inventory status and reorder alerts.</div>',
        unsafe_allow_html=True
    )

    if supplier_performance.empty or reorder_alerts.empty:
        st.error(
            "UC1 output files are missing. "
            "Run uc1_analysis.py first."
        )
        st.stop()

    st.subheader("Inbound Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Suppliers Analyzed",
        f"{len(supplier_performance):,}"
    )

    c2.metric(
        "Reorder Alerts",
        f"{len(reorder_alerts):,}"
    )

    c3.metric(
        "Products Analyzed",
        f"{len(product_inventory):,}"
    )

    if "average_lead_time" in supplier_performance.columns:

        avg_lead = pd.to_numeric(
            supplier_performance["average_lead_time"],
            errors="coerce"
        ).mean()

        c4.metric(
            "Average Actual Lead Time",
            f"{avg_lead:.2f} days"
            if pd.notna(avg_lead)
            else "N/A"
        )

    else:
        c4.metric("Average Actual Lead Time", "N/A")

    # Supplier performance
    st.markdown("---")
    st.subheader("Supplier Performance")

    chart1, chart2 = st.columns(2)

    with chart1:

        show_donut_chart(
            reorder_alerts,
            "reorder_status",
            "Reorder Alert Distribution"
        )

    with chart2:

        show_bar_chart(
            supplier_performance,
            "supplier_name",
            "average_lead_time",
            "Average Supplier Lead Time",
            "Supplier"
        )

    show_table(supplier_performance, 30)

    # Late orders
    st.markdown("---")
    st.subheader("Supplier Late Orders")

    show_bar_chart(
        supplier_performance,
        "supplier_name",
        "late_orders",
        "Late Purchase Orders by Supplier",
        "Supplier"
    )

    # Reorder alerts
    st.markdown("---")
    st.subheader("Reorder Alerts")

    if "reorder_status" in reorder_alerts.columns:

        status_options = ["All"] + sorted(
            reorder_alerts["reorder_status"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_status = st.selectbox(
            "Filter by reorder status",
            status_options
        )

        if selected_status != "All":

            reorder_view = reorder_alerts[
                reorder_alerts["reorder_status"].astype(str)
                == selected_status
            ]

        else:
            reorder_view = reorder_alerts

    else:
        reorder_view = reorder_alerts

    show_table(reorder_view, 100)

    # Inventory health
    st.markdown("---")
    st.subheader("Inventory Health Analysis")

    inventory_health = prepare_inventory_health(inventory)

    if inventory_health.empty:

        st.info(
            "Inventory health cannot be calculated. "
            "Please check the inventory dataset columns."
        )

    else:

        status_counts = (
            inventory_health["inventory_status"]
            .value_counts()
            .reindex(
                ["Healthy", "Low", "Critical", "Unknown"],
                fill_value=0
            )
            .reset_index()
        )

        status_counts.columns = ["Status", "Products"]

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Healthy Stock",
            f"{int(status_counts.loc[status_counts['Status'] == 'Healthy', 'Products'].iloc[0]):,}"
        )

        m2.metric(
            "Low Stock",
            f"{int(status_counts.loc[status_counts['Status'] == 'Low', 'Products'].iloc[0]):,}"
        )

        m3.metric(
            "Critical Stock",
            f"{int(status_counts.loc[status_counts['Status'] == 'Critical', 'Products'].iloc[0]):,}"
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            show_donut_chart(
                inventory_health,
                "inventory_status",
                "Inventory Health Distribution"
            )

        with chart2:

            show_bar_chart(
                status_counts,
                "Status",
                "Products",
                "Products by Inventory Status",
                "Inventory Status"
            )

        st.markdown("### Inventory Health Details")

        show_table(
            inventory_health.sort_values(
                "stock_on_hand",
                ascending=True,
                na_position="first"
            ),
            100
        )

    # Product inventory summary
    st.markdown("---")
    st.subheader("Product Inventory Summary")

    show_table(product_inventory, 100)


# ============================================================
# 9. UC2 - OUTBOUND DELIVERIES
# ============================================================

elif page == "UC2 - Outbound Deliveries":

    st.markdown(
        '<div class="main-title">Outbound Delivery Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Identify delays during order processing '
        'and customer delivery.</div>',
        unsafe_allow_html=True
    )

    if delivery_summary.empty or outbound_analysis.empty:

        st.error(
            "UC2 output files are missing. "
            "Run uc2_analysis.py first."
        )
        st.stop()

    st.subheader("Delivery Performance Summary")

    show_summary_metrics(delivery_summary)

    # Warehouse performance
    st.markdown("---")
    st.subheader("Warehouse Performance")

    show_bar_chart(
        warehouse_performance,
        "warehouse_id",
        "average_total_days",
        "Average Total Delivery Time by Warehouse",
        "Warehouse"
    )

    show_table(warehouse_performance, 20)

    # Order delay analysis
    st.markdown("---")
    st.subheader("Order Delay Analysis")

    status_col1, status_col2 = st.columns(2)

    with status_col1:

        show_donut_chart(
            outbound_analysis,
            "processing_status",
            "Order Processing Status"
        )

    with status_col2:

        show_donut_chart(
            outbound_analysis,
            "delivery_status",
            "Delivery Status"
        )

    # Customer order details
    st.markdown("---")
    st.subheader("Customer Order Details")

    if "warehouse_id" in outbound_analysis.columns:

        warehouse_options = ["All"] + sorted(
            outbound_analysis["warehouse_id"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_warehouse = st.selectbox(
            "Filter by warehouse",
            warehouse_options
        )

        if selected_warehouse != "All":

            outbound_view = outbound_analysis[
                outbound_analysis["warehouse_id"].astype(str)
                == selected_warehouse
            ]

        else:
            outbound_view = outbound_analysis

    else:
        outbound_view = outbound_analysis

    show_table(outbound_view, 100)

    st.caption(
        "Note: The current dataset provides order, shipment and delivery "
        "dates. It does not contain separate transport checkpoints, so "
        "first-mile, middle-mile and last-mile delays cannot be measured "
        "individually from these records."
    )


# ============================================================
# 10. UC3 - SUPPLIER CONTROL TOWER
# ============================================================

elif page == "UC3 - Supplier Control Tower":

    st.markdown(
        '<div class="main-title">Supplier Disruption Control Tower</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Impact of a supplier delay on purchase '
        'orders and customer orders.</div>',
        unsafe_allow_html=True
    )

    if disruption_summary.empty:

        st.error(
            "UC3 output files are missing. "
            "Run uc3_analysis.py first."
        )
        st.stop()

    st.subheader("Disruption Simulation Summary")

    show_summary_metrics(disruption_summary)

    # Disrupted purchase orders
    st.markdown("---")
    st.subheader("Disrupted Purchase Orders")

    supplier_col = next(
        (
            col for col in [
                "supplier_name",
                "supplier_id",
                "supplier",
                "disrupted_supplier"
            ]
            if col in disrupted_pos.columns
        ),
        None
    )

    if supplier_col is not None and not disrupted_pos.empty:

        supplier_counts = (
            disrupted_pos[supplier_col]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        supplier_counts.columns = [
            "supplier",
            "disrupted_orders"
        ]

        show_bar_chart(
            supplier_counts,
            "supplier",
            "disrupted_orders",
            "Disrupted Purchase Orders by Supplier",
            "Supplier"
        )

    else:

        st.info(
            "Supplier-wise disruption chart is unavailable "
            "because supplier information is not present."
        )

    st.write(
        f"Total affected purchase orders: **{len(disrupted_pos):,}**"
    )

    show_table(disrupted_pos, 100)

    # Affected customer orders
    st.markdown("---")
    st.subheader("Potentially Affected Customer Orders")

    st.write(
        f"Total potentially affected customer orders: "
        f"**{len(affected_orders):,}**"
    )

    show_table(affected_orders, 100)

    # Simulation explanation
    st.markdown("---")
    st.subheader("Simulation Explanation")

    st.write(
        "The simulation applies an additional supplier delivery delay. "
        "It identifies purchase orders linked to the disrupted supplier "
        "and customer orders that may be affected by the disruption."
    )

    st.caption(
        "This is a scenario-based estimate using the available dataset. "
        "Potentially affected orders and value at risk are not confirmed "
        "actual losses."
    )
