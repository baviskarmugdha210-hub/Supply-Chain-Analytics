
from pathlib import Path
import html

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Orbix",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "integrated_dataset" / "final_dataset"

 
# ============================================================
# 2. CUSTOM THEME
# ============================================================


# ============================================================
# 2. CUSTOM THEME
# ============================================================

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



def show_bar_chart(df, label_col, value_col, title, xlabel):

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
        ascending=True
    )

    if chart_data.empty:
        st.info("No numeric data available for this chart.")
        return

    # Keep charts readable when there are many categories
    chart_data = chart_data.tail(15)

    fig, ax = plt.subplots(
        figsize=(9, max(3.5, len(chart_data) * 0.38))
    )

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    bars = ax.barh(
        chart_data[label_col].astype(str),
        chart_data[value_col],
        color="#2F6BBA",
        height=0.62
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color="#17365D",
        pad=16
    )

    ax.set_xlabel(
        xlabel,
        fontsize=10,
        color="#64748B"
    )

    ax.set_ylabel("")

    ax.tick_params(
        axis="both",
        labelsize=9,
        colors="#475569"
    )

    ax.grid(
        axis="x",
        color="#DCE8F5",
        linestyle="--",
        linewidth=0.7
    )

    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#DCE8F5")

    ax.bar_label(
        bars,
        fmt="%.1f",
        padding=5,
        fontsize=8,
        color="#17365D"
    )

    ax.margins(x=0.15)

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

    # Monochromatic blue shades
    blue_palette = [
        "#17365D",
        "#2F6BBA",
        "#6F98CC",
        "#A9C2E0",
        "#DCE8F5"
    ]

    colors = [
        blue_palette[i % len(blue_palette)]
        for i in range(len(counts))
    ]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        colors=colors,
        wedgeprops={
            "width": 0.38,
            "edgecolor": "#FFFFFF",
            "linewidth": 2
        },
        textprops={
            "color": "#475569",
            "fontsize": 9
        }
    )

    for item in autotexts:
        item.set_fontsize(8)
        item.set_fontweight("bold")
        item.set_color("#FFFFFF")

    ax.text(
        0,
        0,
        f"{counts.sum():,}",
        ha="center",
        va="center",
        fontsize=19,
        fontweight="bold",
        color="#17365D"
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color="#17365D",
        pad=16
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


# ============================================================
# 7. OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="main-title">Dashboard</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">A consolidated view of inventory, '
        'supplier performance, customer deliveries and disruption risk.</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # 1. PREPARE DASHBOARD FIGURES
    # --------------------------------------------------------

    total_pos = len(purchase_orders)
    total_suppliers = len(suppliers)
    total_products = len(products)
    total_customer_orders = len(outbound)
    total_reorder_alerts = len(reorder_alerts)

    delayed_delivery = 0
    on_time_delivery = 0
    unknown_delivery = 0

    if not outbound_analysis.empty and "delivery_status" in outbound_analysis.columns:
        delivery_status_clean = (
            outbound_analysis["delivery_status"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

        delivery_counts = delivery_status_clean.value_counts()

        delayed_delivery = int(delivery_counts.get("Delayed", 0))
        on_time_delivery = int(delivery_counts.get("On Time", 0))
        unknown_delivery = int(delivery_counts.get("Unknown", 0))

    delivery_delay_pct = (
        delayed_delivery / total_customer_orders * 100
        if total_customer_orders else 0
    )

    average_total_days = None

    if (
        not delivery_summary.empty
        and "Metric" in delivery_summary.columns
        and "Value" in delivery_summary.columns
    ):
        avg_row = delivery_summary[
            delivery_summary["Metric"].astype(str).str.strip()
            == "Average total delivery days"
        ]

        if not avg_row.empty:
            average_total_days = pd.to_numeric(
                avg_row["Value"], errors="coerce"
            ).iloc[0]

    estimated_risk = None

    if (
        not disruption_summary.empty
        and "Metric" in disruption_summary.columns
        and "Value" in disruption_summary.columns
    ):
        risk_row = disruption_summary[
            disruption_summary["Metric"].astype(str).str.strip()
            == "Estimated customer order value at risk"
        ]

        if not risk_row.empty:
            estimated_risk = pd.to_numeric(
                risk_row["Value"], errors="coerce"
            ).iloc[0]

    disrupted_po_count = len(disrupted_pos)
    affected_customer_count = len(affected_orders)

    # --------------------------------------------------------
    # 2. TOP KPI CARDS
    # --------------------------------------------------------

    st.subheader("Supply Chain at a Glance")

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Purchase Orders", f"{total_pos:,}")
    k2.metric("Suppliers", f"{total_suppliers:,}")
    k3.metric("Products", f"{total_products:,}")
    k4.metric("Customer Orders", f"{total_customer_orders:,}")
    k5.metric("Reorder Alerts", f"{total_reorder_alerts:,}")

    st.markdown("")

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Delayed Deliveries",
        f"{delayed_delivery:,}",
        f"{delivery_delay_pct:.1f}% of customer orders"
    )

    d2.metric(
        "Average Total Delivery Time",
        f"{average_total_days:.2f} days"
        if pd.notna(average_total_days)
        else "N/A"
    )

    d3.metric(
        "Potentially Affected Orders",
        f"{affected_customer_count:,}",
        "Supplier disruption scenario"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # 3. CHART COLOUR PALETTE
    # --------------------------------------------------------

    chart_colours = [
        "#17365D",
        "#2F6BBA",
        "#6F98CC",
        "#A9C2E0",
        "#DCE8F5"
    ]

    # --------------------------------------------------------
    # 4. SUPPLIER PERFORMANCE
    # --------------------------------------------------------

    st.subheader("Supplier Performance")

    left, right = st.columns([1.4, 1])

    with left:

        if (
            not supplier_performance.empty
            and "supplier_name" in supplier_performance.columns
            and "average_lead_time" in supplier_performance.columns
        ):

            supplier_chart = supplier_performance[
                ["supplier_name", "average_lead_time"]
            ].copy()

            supplier_chart["average_lead_time"] = pd.to_numeric(
                supplier_chart["average_lead_time"],
                errors="coerce"
            )

            supplier_chart = supplier_chart.dropna()
            supplier_chart = supplier_chart.sort_values(
                "average_lead_time"
            )

            if not supplier_chart.empty:

                fig, ax = plt.subplots(
                    figsize=(8, 4.5)
                )

                fig.patch.set_facecolor("#FFFFFF")
                ax.set_facecolor("#FFFFFF")

                bars = ax.barh(
                    supplier_chart["supplier_name"].astype(str),
                    supplier_chart["average_lead_time"],
                    color="#3976B9",
                    height=0.62
                )

                ax.set_title(
                    "Average Actual Lead Time by Supplier",
                    fontsize=12,
                    fontweight="bold",
                    color="#17365D",
                    pad=13
                )

                ax.set_xlabel(
                    "Average lead time (days)",
                    fontsize=9,
                    color="#64748B"
                )

                ax.tick_params(
                    axis="both",
                    labelsize=8,
                    colors="#475569"
                )

                ax.grid(
                    axis="x",
                    color="#DCE8F5",
                    linestyle="--",
                    linewidth=0.7
                )

                ax.set_axisbelow(True)

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["bottom"].set_color("#DCE8F5")

                ax.bar_label(
                    bars,
                    fmt="%.1f",
                    padding=4,
                    fontsize=8,
                    color="#17365D"
                )

                ax.margins(x=0.16)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            else:
                st.info("Supplier lead-time data is unavailable.")

        else:
            st.info("Supplier performance data is unavailable.")

    # --------------------------------------------------------
    # 5. DELIVERY STATUS
    # --------------------------------------------------------

    with right:

        st.markdown("**Customer Delivery Status**")

        if delayed_delivery + on_time_delivery + unknown_delivery > 0:

            status_labels = []
            status_values = []
            status_colours = []

            if on_time_delivery:
                status_labels.append("On Time")
                status_values.append(on_time_delivery)
                status_colours.append("#2F6BBA")

            if delayed_delivery:
                status_labels.append("Delayed")
                status_values.append(delayed_delivery)
                status_colours.append("#6F98CC")

            if unknown_delivery:
                status_labels.append("Unknown")
                status_values.append(unknown_delivery)
                status_colours.append("#DCE8F5")

            fig, ax = plt.subplots(figsize=(6, 4.5))

            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            wedges, texts, autotexts = ax.pie(
                status_values,
                labels=status_labels,
                colors=status_colours,
                startangle=90,
                autopct="%1.1f%%",
                pctdistance=0.78,
                wedgeprops={
                    "width": 0.38,
                    "edgecolor": "#FFFFFF",
                    "linewidth": 2
                },
                textprops={
                    "fontsize": 9,
                    "color": "#475569"
                }
            )

            for item in autotexts:
                item.set_fontsize(8)
                item.set_fontweight("bold")
                item.set_color("#17365D")

            ax.text(
                0,
                0,
                f"{sum(status_values):,}",
                ha="center",
                va="center",
                fontsize=18,
                fontweight="bold",
                color="#17365D"
            )

            ax.set_title(
                "Delivery Status Distribution",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=13
            )

            ax.axis("equal")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info("Delivery status data is unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 6. WAREHOUSE PERFORMANCE
    # --------------------------------------------------------

    st.subheader("Warehouse Delivery Performance")

    if (
        not warehouse_performance.empty
        and "warehouse_id" in warehouse_performance.columns
        and "average_total_days" in warehouse_performance.columns
    ):

        warehouse_chart = warehouse_performance[
            ["warehouse_id", "average_total_days"]
        ].copy()

        warehouse_chart["average_total_days"] = pd.to_numeric(
            warehouse_chart["average_total_days"],
            errors="coerce"
        )

        warehouse_chart = warehouse_chart.dropna()
        warehouse_chart = warehouse_chart.sort_values(
            "average_total_days"
        )

        if not warehouse_chart.empty:

            fig, ax = plt.subplots(figsize=(10, 3.5))

            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.bar(
                warehouse_chart["warehouse_id"].astype(str),
                warehouse_chart["average_total_days"],
                color="#6F98CC",
                width=0.55
            )

            ax.set_title(
                "Average Total Delivery Days by Warehouse",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=13
            )

            ax.set_ylabel(
                "Average days",
                fontsize=9,
                color="#64748B"
            )

            ax.tick_params(
                axis="both",
                labelsize=9,
                colors="#475569"
            )

            ax.grid(
                axis="y",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )

            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%.2f",
                padding=4,
                fontsize=9,
                color="#17365D"
            )

            ax.margins(y=0.18)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info("Warehouse performance data is unavailable.")

    else:
        st.info("Warehouse performance data is unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 7. SUPPLIER DISRUPTION IMPACT
    # --------------------------------------------------------

    st.subheader("Supplier Disruption Impact")

    impact_left, impact_right = st.columns([1.2, 1])

    with impact_left:

        impact_labels = [
            "Disrupted Purchase Orders",
            "Potentially Affected Customer Orders"
        ]

        impact_values = [
            disrupted_po_count,
            affected_customer_count
        ]

        fig, ax = plt.subplots(figsize=(7, 3.2))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.barh(
            impact_labels[::-1],
            impact_values[::-1],
            color=["#6F98CC", "#2F6BBA"],
            height=0.5
        )

        ax.set_title(
            "Orders Identified in Disruption Scenario",
            fontsize=12,
            fontweight="bold",
            color="#17365D",
            pad=13
        )

        ax.set_xlabel(
            "Number of orders",
            fontsize=9,
            color="#64748B"
        )

        ax.tick_params(
            axis="both",
            labelsize=8,
            colors="#475569"
        )

        ax.grid(
            axis="x",
            color="#DCE8F5",
            linestyle="--",
            linewidth=0.7
        )

        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#DCE8F5")

        ax.bar_label(
            bars,
            fmt="%d",
            padding=5,
            fontsize=9,
            color="#17365D"
        )

        ax.margins(x=0.2)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with impact_right:

        st.markdown("**Estimated Customer Order Value at Risk**")

        if pd.notna(estimated_risk):
            st.metric(
                "Scenario estimate",
                f"₹{estimated_risk:,.2f}"
            )
        else:
            st.metric("Scenario estimate", "N/A")

        st.caption(
            "This value is a scenario-based estimate from the supplier "
            "disruption analysis. It is not a confirmed financial loss."
        )

        st.markdown("**Scenario assumptions**")

        if not disruption_summary.empty:
            for _, row in disruption_summary.iterrows():

                metric_name = str(row["Metric"]).strip()
                metric_value = str(row["Value"]).strip()

                if metric_name in [
                    "Disrupted supplier",
                    "Additional delay in days"
                ]:
                    st.write(f"**{metric_name}:** {metric_value}")

    st.markdown("---")

    # --------------------------------------------------------
    # 8. QUICK OPERATIONAL TABLES
    # --------------------------------------------------------

    st.subheader("Operational Highlights")

    tab1, tab2 = st.tabs([
        "Suppliers with Most Late Orders",
        "Warehouse Performance"
    ])

    with tab1:

        if (
            not supplier_performance.empty
            and "late_orders" in supplier_performance.columns
        ):

            supplier_late_view = supplier_performance.copy()

            supplier_late_view["late_orders"] = pd.to_numeric(
                supplier_late_view["late_orders"],
                errors="coerce"
            )

            supplier_late_view = supplier_late_view.sort_values(
                "late_orders",
                ascending=False
            )

            show_table(supplier_late_view, 10)

        else:
            st.info("Supplier late-order information is unavailable.")

    with tab2:

        show_table(warehouse_performance, 10)

    st.caption(
        "Operational figures are based on the supplied analysis outputs. "
        "Supplier disruption figures are scenario-based estimates."
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
        '<div class="subtitle">Monitor stock availability, identify '
        'replenishment requirements and evaluate supplier reliability.</div>',
        unsafe_allow_html=True
    )

    if reorder_alerts.empty or supplier_performance.empty:
        st.error("UC1 output files are missing. Run uc1_analysis.py first.")
        st.stop()

    # --------------------------------------------------------
    # 1. CLEAN DATA FOR DISPLAY
    # --------------------------------------------------------

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
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "unit_cost",
        "unit_price"
    ]:
        if col in reorder_view.columns:
            reorder_view[col] = pd.to_numeric(
                reorder_view[col], errors="coerce"
            )

    for col in [
        "average_lead_time",
        "average_expected_lead_time",
        "late_orders",
        "total_orders"
    ]:
        if col in supplier_view.columns:
            supplier_view[col] = pd.to_numeric(
                supplier_view[col], errors="coerce"
            )

    # --------------------------------------------------------
    # 2. KEY PERFORMANCE INDICATORS
    # --------------------------------------------------------

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

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Reorder Alert Records", f"{total_alert_records:,}")
    m2.metric("Products with Alerts", f"{unique_products:,}")
    m3.metric("Suppliers Analysed", f"{supplier_count:,}")
    m4.metric("Late Purchase Orders", f"{total_late_orders:,.0f}")

    st.markdown("---")

    # --------------------------------------------------------
    # 3. REORDER EXPOSURE BY PRODUCT CATEGORY
    # --------------------------------------------------------

    st.subheader("Reorder Exposure by Product Category")

    if (
        "category" in reorder_view.columns
        and "product_id" in reorder_view.columns
    ):

        category_counts = (
            reorder_view.groupby("category")["product_id"]
            .nunique()
            .sort_values(ascending=True)
        )

        if not category_counts.empty:

            fig, ax = plt.subplots(figsize=(9, 4))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                category_counts.index.astype(str),
                category_counts.values,
                color="#3976B9",
                height=0.58
            )

            ax.set_title(
                "Products with Reorder Alerts by Category",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=12
            )

            ax.set_xlabel("Number of unique products", fontsize=9)
            ax.tick_params(axis="both", labelsize=8)
            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%d",
                padding=4,
                fontsize=8,
                color="#17365D"
            )

            ax.margins(x=0.15)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    else:
        st.info("Product category information is unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 4. STOCK AGAINST REORDER POINT
    # --------------------------------------------------------

    st.subheader("Products Requiring Attention")

    if (
        {"product_id", "stock_on_hand", "reorder_point"}.issubset(
            reorder_view.columns
        )
    ):

        product_stock = (
            reorder_view.groupby("product_id", as_index=False)
            .agg(
                stock_on_hand=("stock_on_hand", "mean"),
                reorder_point=("reorder_point", "mean")
            )
        )

        product_stock["stock_gap"] = (
            product_stock["reorder_point"]
            - product_stock["stock_on_hand"]
        )

        product_stock = (
            product_stock.sort_values("stock_gap", ascending=False)
            .head(12)
            .sort_values("stock_gap", ascending=True)
        )

        if not product_stock.empty:

            fig, ax = plt.subplots(figsize=(10, 4.5))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            positions = range(len(product_stock))
            bar_height = 0.34

            ax.barh(
                [p + bar_height / 2 for p in positions],
                product_stock["reorder_point"],
                height=bar_height,
                color="#A9C2E0",
                label="Reorder point"
            )

            ax.barh(
                [p - bar_height / 2 for p in positions],
                product_stock["stock_on_hand"],
                height=bar_height,
                color="#2F6BBA",
                label="Stock on hand"
            )

            ax.set_yticks(list(positions))
            ax.set_yticklabels(product_stock["product_id"].astype(str))

            ax.set_title(
                "Stock on Hand Compared with Reorder Point",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=12
            )

            ax.set_xlabel("Stock quantity", fontsize=9)
            ax.tick_params(axis="both", labelsize=8)
            ax.legend(loc="lower right", frameon=False, fontsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            st.caption(
                "The chart compares average stock on hand with average "
                "reorder point for the 12 products with the largest "
                "positive stock gaps in the alert records."
            )

    else:
        st.info("Stock and reorder-point fields are unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 5. SUPPLIER LEAD-TIME COMPARISON
    # --------------------------------------------------------

    st.subheader("Supplier Delivery Performance")

    required_supplier_cols = {
        "supplier_name",
        "average_lead_time",
        "average_expected_lead_time"
    }

    if required_supplier_cols.issubset(supplier_view.columns):

        lead_chart = supplier_view[
            [
                "supplier_name",
                "average_lead_time",
                "average_expected_lead_time"
            ]
        ].dropna().copy()

        lead_chart = lead_chart.sort_values(
            "average_lead_time", ascending=True
        )

        if not lead_chart.empty:

            fig, ax = plt.subplots(figsize=(10, 4.6))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            positions = range(len(lead_chart))
            bar_height = 0.34

            ax.barh(
                [p + bar_height / 2 for p in positions],
                lead_chart["average_expected_lead_time"],
                height=bar_height,
                color="#A9C2E0",
                label="Expected lead time"
            )

            ax.barh(
                [p - bar_height / 2 for p in positions],
                lead_chart["average_lead_time"],
                height=bar_height,
                color="#2F6BBA",
                label="Actual lead time"
            )

            ax.set_yticks(list(positions))
            ax.set_yticklabels(lead_chart["supplier_name"].astype(str))

            ax.set_title(
                "Actual vs Expected Average Supplier Lead Time",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=12
            )

            ax.set_xlabel("Lead time (days)", fontsize=9)
            ax.tick_params(axis="both", labelsize=8)
            ax.legend(loc="lower right", frameon=False, fontsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    else:
        st.info("Supplier lead-time comparison fields are unavailable.")

    # --------------------------------------------------------
    # 6. SUPPLIERS WITH MOST LATE ORDERS
    # --------------------------------------------------------

    st.subheader("Supplier Late-Order Analysis")

    if {"supplier_name", "late_orders"}.issubset(supplier_view.columns):

        late_chart = supplier_view[
            ["supplier_name", "late_orders"]
        ].dropna().copy()

        late_chart = late_chart.sort_values(
            "late_orders", ascending=True
        )

        if not late_chart.empty:

            fig, ax = plt.subplots(figsize=(10, 4.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                late_chart["supplier_name"].astype(str),
                late_chart["late_orders"],
                color="#3976B9",
                height=0.58
            )

            ax.set_title(
                "Late Purchase Orders by Supplier",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=12
            )

            ax.set_xlabel("Number of late orders", fontsize=9)
            ax.tick_params(axis="both", labelsize=8)
            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%.0f",
                padding=4,
                fontsize=8,
                color="#17365D"
            )

            ax.margins(x=0.15)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    else:
        st.info("Late-order supplier information is unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 7. FILTERABLE REORDER RECORDS
    # --------------------------------------------------------

    st.subheader("Reorder Alert Details")

    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        status_options = (
            ["All"] + sorted(
                reorder_view["reorder_status"].dropna().unique().tolist()
            )
            if "reorder_status" in reorder_view.columns else ["All"]
        )

        selected_status = st.selectbox(
            "Reorder status",
            status_options,
            key="uc1_status_filter"
        )

    with filter2:
        category_options = (
            ["All"] + sorted(
                reorder_view["category"].dropna().unique().tolist()
            )
            if "category" in reorder_view.columns else ["All"]
        )

        selected_category = st.selectbox(
            "Product category",
            category_options,
            key="uc1_category_filter"
        )

    with filter3:
        warehouse_options = (
            ["All"] + sorted(
                reorder_view["warehouse_name"].dropna().unique().tolist()
            )
            if "warehouse_name" in reorder_view.columns else ["All"]
        )

        selected_warehouse = st.selectbox(
            "Warehouse",
            warehouse_options,
            key="uc1_warehouse_filter"
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
        f"Showing {len(filtered_reorders):,} of "
        f"{len(reorder_view):,} alert records."
    )

    show_table(filtered_reorders, 100)

    # --------------------------------------------------------
    # 8. SUPPLIER PERFORMANCE TABLE
    # --------------------------------------------------------

    st.subheader("Supplier Performance Details")
    show_table(supplier_view, 20)

    # --------------------------------------------------------
    # 9. PRODUCT INVENTORY SUMMARY
    # --------------------------------------------------------

    st.subheader("Product Inventory Summary")
    show_table(inventory_view, 100)

    st.caption(
        "Note: Reorder alert records are inventory observations, not "
        "necessarily unique purchase orders. Product-level stock values "
        "in the comparison chart are averaged across the available alert "
        "records for each product."
    )


# ============================================================
# 9. UC2 - OUTBOUND DELIVERIES
# ============================================================


elif page == "UC2 - Outbound Deliveries":

    st.markdown(
        '<div class="main-title">Outbound Delivery Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Track customer order fulfilment, '
        'evaluate warehouse performance and identify delivery delays.</div>',
        unsafe_allow_html=True
    )

    if delivery_summary.empty or outbound_analysis.empty:
        st.error(
            "UC2 output files are missing. "
            "Run uc2_analysis.py first."
        )
        st.stop()

    # --------------------------------------------------------
    # 1. PREPARE DATA
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 2. DELIVERY PERFORMANCE SUMMARY
    # --------------------------------------------------------

    st.subheader("Delivery Performance Summary")

    show_summary_metrics(delivery_summary)

    st.markdown("---")

    # --------------------------------------------------------
    # 3. WAREHOUSE PERFORMANCE
    # --------------------------------------------------------

    st.subheader("Warehouse Performance")

    if (
        {"warehouse_id", "average_total_days"}.issubset(
            warehouse_view.columns
        )
    ):

        warehouse_chart = warehouse_view[
            ["warehouse_id", "average_total_days"]
        ].copy()

        warehouse_chart["average_total_days"] = pd.to_numeric(
            warehouse_chart["average_total_days"],
            errors="coerce"
        )

        warehouse_chart = (
            warehouse_chart.dropna()
            .sort_values("average_total_days", ascending=True)
        )

        if not warehouse_chart.empty:

            fig, ax = plt.subplots(figsize=(9, 4))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                warehouse_chart["warehouse_id"].astype(str),
                warehouse_chart["average_total_days"],
                color="#3976B9",
                height=0.58
            )

            ax.set_title(
                "Average Total Delivery Time by Warehouse",
                fontsize=12,
                fontweight="bold",
                color="#17365D",
                pad=12
            )

            ax.set_xlabel("Average delivery time (days)", fontsize=9)
            ax.tick_params(axis="both", labelsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%.1f",
                padding=4,
                fontsize=8,
                color="#17365D"
            )

            ax.margins(x=0.15)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            st.caption(
                "Compares the average total delivery time across "
                "warehouses. Lower values indicate faster average "
                "order fulfilment."
            )

    else:
        st.info("Warehouse delivery-time information is unavailable.")

    with st.expander("View warehouse performance records"):
        show_table(warehouse_view, 20)

    st.markdown("---")

    # --------------------------------------------------------
    # 4. ORDER PROCESSING AND DELIVERY STATUS
    # --------------------------------------------------------

    st.subheader("Order Fulfilment Status")

    status_left, status_right = st.columns(2)

    with status_left:
        if "processing_status" in outbound_view.columns:
            show_donut_chart(
                outbound_view,
                "processing_status",
                "Order Processing Status"
            )
        else:
            st.info("Processing status information is unavailable.")

    with status_right:
        if "delivery_status" in outbound_view.columns:
            show_donut_chart(
                outbound_view,
                "delivery_status",
                "Customer Delivery Status"
            )
        else:
            st.info("Delivery status information is unavailable.")

    st.markdown("---")

    # --------------------------------------------------------
    # 5. FILTERABLE CUSTOMER ORDER DETAILS
    # --------------------------------------------------------

    st.subheader("Customer Order Details")

    filter1, filter2, filter3 = st.columns(3)

    # Warehouse filter
    with filter1:

        if "warehouse_id" in outbound_view.columns:

            warehouse_options = (
                ["All"] +
                sorted(
                    outbound_view["warehouse_id"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

        else:
            warehouse_options = ["All"]

        selected_warehouse = st.selectbox(
            "Warehouse",
            warehouse_options,
            key="uc2_warehouse_filter"
        )

    # Processing status filter
    with filter2:

        if "processing_status" in outbound_view.columns:

            processing_options = (
                ["All"] +
                sorted(
                    outbound_view["processing_status"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

        else:
            processing_options = ["All"]

        selected_processing = st.selectbox(
            "Processing status",
            processing_options,
            key="uc2_processing_filter"
        )

    # Delivery status filter
    with filter3:

        if "delivery_status" in outbound_view.columns:

            delivery_options = (
                ["All"] +
                sorted(
                    outbound_view["delivery_status"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

        else:
            delivery_options = ["All"]

        selected_delivery = st.selectbox(
            "Delivery status",
            delivery_options,
            key="uc2_delivery_filter"
        )

    # Apply selected filters
    filtered_outbound = outbound_view.copy()

    if (
        selected_warehouse != "All"
        and "warehouse_id" in filtered_outbound.columns
    ):
        filtered_outbound = filtered_outbound[
            filtered_outbound["warehouse_id"].astype(str)
            == selected_warehouse
        ]

    if (
        selected_processing != "All"
        and "processing_status" in filtered_outbound.columns
    ):
        filtered_outbound = filtered_outbound[
            filtered_outbound["processing_status"]
            == selected_processing
        ]

    if (
        selected_delivery != "All"
        and "delivery_status" in filtered_outbound.columns
    ):
        filtered_outbound = filtered_outbound[
            filtered_outbound["delivery_status"]
            == selected_delivery
        ]

    st.caption(
        f"Showing {len(filtered_outbound):,} of "
        f"{len(outbound_view):,} customer orders."
    )

    show_table(filtered_outbound, 100)

    st.markdown("---")

    # --------------------------------------------------------
    # 6. DELIVERY ANALYSIS SUMMARY
    # --------------------------------------------------------

    st.subheader("Delivery Analysis Summary")

    st.markdown(
        """
        Use the warehouse comparison to identify locations with longer
        average delivery times. The processing and delivery status charts
        help distinguish order-processing issues from delivery-stage
        outcomes.
        """
    )

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
        '<div class="subtitle">Analyse supplier disruptions, '
        'purchase order exposure and potential customer impact.</div>',
        unsafe_allow_html=True
    )

    if disruption_summary.empty:
        st.error(
            "UC3 output files are missing. "
            "Run uc3_analysis.py first."
        )
        st.stop()

    # --------------------------------------------------------
    # 1. PREPARE DATA
    # --------------------------------------------------------

    po_view = disrupted_pos.copy()
    customer_view = affected_orders.copy()

    def find_uc3_column(df, candidates):
        lookup = {
            str(col).lower().strip(): col
            for col in df.columns
        }

        for candidate in candidates:
            if candidate.lower().strip() in lookup:
                return lookup[candidate.lower().strip()]

        return None

    supplier_col = find_uc3_column(
        po_view,
        [
            "supplier_name",
            "supplier_id",
            "supplier",
            "disrupted_supplier"
        ]
    )

    po_status_col = find_uc3_column(
        po_view,
        [
            "status",
            "po_status",
            "disruption_status",
            "delivery_status"
        ]
    )

    customer_supplier_col = find_uc3_column(
        customer_view,
        [
            "supplier_name",
            "supplier_id",
            "supplier",
            "disrupted_supplier"
        ]
    )

    customer_order_col = find_uc3_column(
        customer_view,
        [
            "order_id",
            "sales_order_id",
            "customer_order_id",
            "sales_id"
        ]
    )

    customer_value_col = find_uc3_column(
        customer_view,
        [
            "order_value",
            "total_order_value",
            "sales_value",
            "order_amount",
            "total_amount",
            "order_total",
            "value_at_risk",
            "estimated_value_at_risk"
        ]
    )

    customer_status_col = find_uc3_column(
        customer_view,
        [
            "delivery_status",
            "order_status",
            "status"
        ]
    )

    # Clean text fields
    if supplier_col is not None:
        po_view[supplier_col] = (
            po_view[supplier_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    if po_status_col is not None:
        po_view[po_status_col] = (
            po_view[po_status_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    if customer_status_col is not None:
        customer_view[customer_status_col] = (
            customer_view[customer_status_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Keep one row per customer order for order-level estimates.
    if customer_order_col is not None:
        customer_view = customer_view.drop_duplicates(
            subset=[customer_order_col]
        )

    # Convert order value to numeric
    estimated_value = None

    if customer_value_col is not None:

        customer_view[customer_value_col] = pd.to_numeric(
            customer_view[customer_value_col],
            errors="coerce"
        )

        estimated_value = customer_view[
            customer_value_col
        ].sum(min_count=1)

    # --------------------------------------------------------
    # 2. KEY PERFORMANCE INDICATORS
    # --------------------------------------------------------

    total_disrupted_pos = len(po_view)
    total_affected_orders = len(customer_view)

    supplier_count = (
        po_view[supplier_col].nunique()
        if supplier_col is not None else None
    )

    st.subheader("Disruption Overview")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Disrupted Purchase Orders",
        f"{total_disrupted_pos:,}"
    )

    k2.metric(
        "Suppliers Affected",
        f"{supplier_count:,}"
        if supplier_count is not None else "N/A"
    )

    k3.metric(
        "Potentially Affected Orders",
        f"{total_affected_orders:,}"
    )

    k4.metric(
        "Estimated Order Value at Risk",
        f"₹{estimated_value:,.0f}"
        if estimated_value is not None
        and pd.notna(estimated_value)
        else "N/A"
    )

    st.caption(
        "Estimated order value at risk is a scenario-based exposure, "
        "not confirmed financial loss."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # 3. SUPPLIER DISRUPTION ANALYSIS
    # --------------------------------------------------------

    st.subheader("Supplier Disruption Analysis")

    chart_left, chart_right = st.columns(2, gap="medium")

    supplier_counts = None

    with chart_left:

        st.markdown("**Purchase Orders by Supplier**")

        if supplier_col is not None and not po_view.empty:

            supplier_counts = (
                po_view.groupby(supplier_col)
                .size()
                .reset_index(name="disrupted_orders")
                .sort_values("disrupted_orders", ascending=True)
            )

            fig, ax = plt.subplots(figsize=(5.5, 3.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                supplier_counts[supplier_col].astype(str),
                supplier_counts["disrupted_orders"],
                color="#3976B9",
                height=0.55
            )

            ax.set_xlabel("Disrupted purchase orders", fontsize=8)
            ax.tick_params(axis="both", labelsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.6
            )

            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%d",
                padding=3,
                fontsize=8,
                color="#17365D"
            )

            ax.margins(x=0.16)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            highest_supplier = supplier_counts.iloc[-1]

            st.caption(
                f"Highest disruption count: "
                f"**{highest_supplier[supplier_col]}** "
                f"({int(highest_supplier['disrupted_orders'])} "
                f"purchase orders)."
            )

        else:
            st.info("Supplier information is unavailable.")

    with chart_right:

        st.markdown("**Purchase Order Status Distribution**")

        if po_status_col is not None and not po_view.empty:

            status_counts = po_view[
                po_status_col
            ].value_counts()

            fig, ax = plt.subplots(figsize=(5.5, 3.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            wedges, texts, autotexts = ax.pie(
                status_counts.values,
                labels=status_counts.index.astype(str),
                autopct="%1.1f%%",
                startangle=90,
                pctdistance=0.78,
                wedgeprops={
                    "width": 0.42,
                    "edgecolor": "white",
                    "linewidth": 2
                },
                textprops={
                    "fontsize": 8,
                    "color": "#17365D"
                }
            )

            for autotext in autotexts:
                autotext.set_fontsize(8)
                autotext.set_color("#17365D")

            ax.set_aspect("equal")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            most_common_status = status_counts.index[0]

            st.caption(
                f"Most frequent purchase order status: "
                f"**{most_common_status}** "
                f"({int(status_counts.iloc[0])} records)."
            )

        else:
            st.info(
                "Purchase order status information is unavailable "
                "for this chart."
            )

    st.markdown("---")

    # --------------------------------------------------------
    # 4. CUSTOMER ORDER IMPACT
    # --------------------------------------------------------

    st.subheader("Potential Customer Impact")

    impact_left, impact_right = st.columns(2, gap="medium")

    with impact_left:

        st.markdown("**Customer Order Exposure**")

        st.metric(
            "Potentially Affected Customer Orders",
            f"{total_affected_orders:,}"
        )

        if (
            customer_value_col is not None
            and estimated_value is not None
            and pd.notna(estimated_value)
        ):

            st.metric(
                "Estimated Order Value",
                f"₹{estimated_value:,.2f}"
            )

            average_order_value = (
                estimated_value / total_affected_orders
                if total_affected_orders > 0 else 0
            )

            st.metric(
                "Average Value per Affected Order",
                f"₹{average_order_value:,.2f}"
            )

        else:
            st.info(
                "Order value information is unavailable. "
                "Financial exposure cannot be calculated."
            )

    with impact_right:

        st.markdown("**Customer Order Analysis**")

        if (
            customer_supplier_col is not None
            and not customer_view.empty
        ):

            customer_supplier_counts = (
                customer_view.groupby(customer_supplier_col)
                .size()
                .sort_values(ascending=True)
            )

            fig, ax = plt.subplots(figsize=(5.5, 3.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                customer_supplier_counts.index.astype(str),
                customer_supplier_counts.values,
                color="#6F98CC",
                height=0.55
            )

            ax.set_xlabel("Potentially affected orders", fontsize=8)
            ax.tick_params(axis="both", labelsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.6
            )

            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%d",
                padding=3,
                fontsize=8,
                color="#17365D"
            )

            ax.margins(x=0.16)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.caption(
                "Customer orders grouped by supplier, using the "
                "supplier field present in the affected-order records."
            )

        elif (
            customer_value_col is not None
            and not customer_view.empty
        ):

            top_orders = customer_view.nlargest(
                10, customer_value_col
            ).copy()

            if customer_order_col is not None:
                order_labels = top_orders[
                    customer_order_col
                ].astype(str)
            else:
                order_labels = top_orders.index.astype(str)

            fig, ax = plt.subplots(figsize=(5.5, 3.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                order_labels,
                top_orders[customer_value_col],
                color="#6F98CC",
                height=0.55
            )

            ax.set_xlabel("Order value (₹)", fontsize=8)
            ax.tick_params(axis="both", labelsize=7)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.6
            )

            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.xaxis.set_major_formatter(
                plt.FuncFormatter(
                    lambda x, _: f"₹{x:,.0f}"
                )
            )

            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.caption(
                "The 10 potentially affected customer orders "
                "with the highest recorded order values."
            )

        elif (
            customer_status_col is not None
            and not customer_view.empty
        ):

            customer_status_counts = (
                customer_view[customer_status_col]
                .value_counts()
                .sort_values(ascending=True)
            )

            fig, ax = plt.subplots(figsize=(5.5, 3.2))
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            bars = ax.barh(
                customer_status_counts.index.astype(str),
                customer_status_counts.values,
                color="#6F98CC",
                height=0.55
            )

            ax.set_xlabel("Customer orders", fontsize=8)
            ax.tick_params(axis="both", labelsize=8)

            ax.grid(
                axis="x",
                color="#DCE8F5",
                linestyle="--",
                linewidth=0.6
            )

            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#DCE8F5")

            ax.bar_label(
                bars,
                fmt="%d",
                padding=3,
                fontsize=8
            )

            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.caption(
                "Distribution of delivery or order statuses "
                "among potentially affected customer orders."
            )

        else:
            st.info(
                "There are not enough customer order fields "
                "to create a meaningful breakdown chart."
            )

    st.markdown("---")

    # --------------------------------------------------------
    # 5. DISRUPTION RECORD DETAILS
    # --------------------------------------------------------

    st.subheader("Disrupted Purchase Order Records")

    with st.expander(
        "View and filter disrupted purchase orders",
        expanded=False
    ):

        if supplier_col is not None:

            supplier_options = (
                ["All"] +
                sorted(
                    po_view[supplier_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            selected_supplier = st.selectbox(
                "Supplier",
                supplier_options,
                key="uc3_supplier_filter"
            )

        else:
            selected_supplier = "All"

        if po_status_col is not None:

            status_options = (
                ["All"] +
                sorted(
                    po_view[po_status_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            selected_status = st.selectbox(
                "Purchase order status",
                status_options,
                key="uc3_po_status_filter"
            )

        else:
            selected_status = "All"

        filtered_pos = po_view.copy()

        if selected_supplier != "All" and supplier_col is not None:
            filtered_pos = filtered_pos[
                filtered_pos[supplier_col].astype(str)
                == selected_supplier
            ]

        if selected_status != "All" and po_status_col is not None:
            filtered_pos = filtered_pos[
                filtered_pos[po_status_col].astype(str)
                == selected_status
            ]

        st.caption(
            f"Showing {len(filtered_pos):,} of "
            f"{len(po_view):,} purchase orders."
        )

        show_table(filtered_pos, 100)

    # --------------------------------------------------------
    # 6. CUSTOMER ORDER DETAILS
    # --------------------------------------------------------

    st.subheader("Affected Customer Order Records")

    with st.expander(
        "View potentially affected customer orders",
        expanded=False
    ):

        st.caption(
            f"Total potentially affected customer orders: "
            f"{len(customer_view):,}"
        )

        show_table(customer_view, 100)

    # --------------------------------------------------------
    # 7. DISRUPTION SUMMARY
    # --------------------------------------------------------

    st.subheader("Disruption Scenario Summary")

    with st.expander(
        "View scenario summary records",
        expanded=False
    ):
        show_table(disruption_summary, 20)

    # --------------------------------------------------------
    # 8. INTERPRETATION
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("Key Observations")

    if supplier_counts is not None and not supplier_counts.empty:

        top_supplier = supplier_counts.iloc[-1]
        top_supplier_share = (
            top_supplier["disrupted_orders"]
            / total_disrupted_pos * 100
            if total_disrupted_pos > 0 else 0
        )

        st.markdown(
            f"""
            - **Supplier concentration:** {top_supplier[supplier_col]}
              has the highest number of disrupted purchase orders
              ({int(top_supplier['disrupted_orders'])}), representing
              {top_supplier_share:.1f}% of the disrupted purchase order
              records.
            """
        )

    if po_status_col is not None and not po_view.empty:

        status_counts = po_view[po_status_col].value_counts()

        st.markdown(
            f"""
            - **Purchase order status:** {status_counts.index[0]}
              is the most common status, accounting for
              {int(status_counts.iloc[0])} disrupted purchase orders.
            """
        )

    if total_affected_orders > 0:

        st.markdown(
            f"""
            - **Customer exposure:** {total_affected_orders:,}
              customer orders are identified as potentially affected
              in this disruption scenario.
            """
        )

    if (
        estimated_value is not None
        and pd.notna(estimated_value)
    ):

        st.markdown(
            f"""
            - **Financial exposure:** The estimated value associated
              with these potentially affected customer orders is
              ₹{estimated_value:,.2f}. This is scenario exposure,
              not confirmed financial loss.
            """
        )

    st.caption(
        "This analysis identifies potential disruption exposure using "
        "the available dataset. It does not confirm that every affected "
        "customer order will be delayed or result in a financial loss."
    )
