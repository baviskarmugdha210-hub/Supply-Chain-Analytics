
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
# 6. SIDEBAR NAVIGATION  (V2 LAYOUT)
# ============================================================

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


# ============================================================
# 6B. SHARED DESIGN HELPERS
# ============================================================

BLUE_DARK = "#17365D"
BLUE = "#2F6BBA"
BLUE_MID = "#6F98CC"
BLUE_LIGHT = "#A9C2E0"
BLUE_PALE = "#DCE8F5"
WARN = "#D9822B"
BAD = "#C8453B"
GOOD = "#2E8B6E"

DONUT_COLOURS = [BLUE_DARK, BLUE, BLUE_MID, BLUE_LIGHT, BLUE_PALE]

DELIVERY_COLOURS = {
    "On Time": BLUE,
    "Delayed": WARN,
    "Unknown": BLUE_PALE,
}

HEALTH_COLOURS = {
    "Critical": BAD,
    "Low": WARN,
    "Healthy": BLUE,
    "Unknown": BLUE_PALE,
}

TONES = {
    "blue": "#3976B9",
    "navy": "#142B49",
    "amber": WARN,
    "red": BAD,
    "green": GOOD,
}


def esc(value):
    return html.escape(str(value))


def inr(value):
    if value is None or pd.isna(value):
        return "N/A"
    value = float(value)
    if abs(value) >= 1e7:
        return f"₹{value / 1e7:,.2f} Cr"
    if abs(value) >= 1e5:
        return f"₹{value / 1e5:,.2f} L"
    return f"₹{value:,.0f}"


def lookup_metric(df, name):
    if (
        df is None
        or df.empty
        or "Metric" not in df.columns
        or "Value" not in df.columns
    ):
        return None

    row = df[df["Metric"].astype(str).str.strip() == name]

    if row.empty:
        return None

    value = pd.to_numeric(row["Value"], errors="coerce").iloc[0]
    return None if pd.isna(value) else float(value)


def render_fig(fig):
    try:
        st.pyplot(fig, width="stretch")
    except TypeError:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def new_fig(width=5.6, height=3.0):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    return fig, ax


def style_axes(ax, grid_axis="x"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BLUE_PALE)
    ax.tick_params(axis="both", labelsize=8, colors="#475569")
    ax.grid(axis=grid_axis, color=BLUE_PALE, linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)


@contextmanager
def card(title=None, caption=None):
    try:
        box = st.container(border=True)
    except TypeError:
        box = st.container()

    with box:
        if title:
            st.markdown(
                f'<div class="card-title">{esc(title)}</div>',
                unsafe_allow_html=True
            )
        if caption:
            st.markdown(
                f'<div class="card-caption">{esc(caption)}</div>',
                unsafe_allow_html=True
            )
        yield


def page_header(title, subtitle):
    st.markdown(
        f'<div class="main-title">{esc(title)}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">{esc(subtitle)}</div>',
        unsafe_allow_html=True
    )


def section_heading(title, caption=None):
    st.markdown(
        f'<div class="section-title">{esc(title)}</div>',
        unsafe_allow_html=True
    )
    if caption:
        st.markdown(
            f'<div class="section-sub">{esc(caption)}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="section-sub"></div>',
            unsafe_allow_html=True
        )


def kpi_html(label, value, sub=None, tone="blue"):
    colour = TONES.get(tone, TONES["blue"])
    sub_html = f'<div class="kpi-sub">{esc(sub)}</div>' if sub else ""
    return (
        f'<div class="kpi" style="border-left-color:{colour};">'
        f'<div class="kpi-label">{esc(label)}</div>'
        f'<div class="kpi-value">{esc(value)}</div>'
        f'{sub_html}</div>'
    )


def kpi_cards(items, per_row=5):
    """items: (label, value[, sub[, tone]])"""
    for start in range(0, len(items), per_row):
        row = items[start:start + per_row]
        cols = st.columns(per_row)

        for col, item in zip(cols, row):
            label, value = item[0], item[1]
            sub = item[2] if len(item) > 2 else None
            tone = item[3] if len(item) > 3 else "blue"
            col.markdown(
                kpi_html(label, value, sub, tone),
                unsafe_allow_html=True
            )


def format_metric_value(value):
    number = pd.to_numeric(value, errors="coerce")
    if pd.notna(number):
        if float(number).is_integer():
            return f"{number:,.0f}"
        return f"{number:,.2f}"
    return str(value)


def summary_cards(df, per_row=4):
    if (
        df is None
        or df.empty
        or "Metric" not in df.columns
        or "Value" not in df.columns
    ):
        st.info("Summary metrics are unavailable.")
        return

    items = []

    for _, row in df.iterrows():
        name = str(row["Metric"])
        lowered = name.lower()
        tone = "amber" if ("delay" in lowered or "late" in lowered) else "blue"
        items.append((name, format_metric_value(row["Value"]), None, tone))

    kpi_cards(items, per_row=per_row)


def insight_panel(title, lines):
    items = "".join(f"<li>{line}</li>" for line in lines)
    st.markdown(
        '<div class="section-panel">'
        f'<div style="font-weight:700;color:#142B49;margin-bottom:6px;">'
        f'{esc(title)}</div>'
        '<ul style="margin:0;padding-left:18px;color:#34445A;'
        f'font-size:0.88rem;line-height:1.65;">{items}</ul>'
        '</div>',
        unsafe_allow_html=True
    )


def callout(text, warn=False):
    css = "callout callout-warn" if warn else "callout"
    st.markdown(
        f'<div class="{css}">{text}</div>',
        unsafe_allow_html=True
    )


def observation_list(observations):
    if not observations:
        st.info("Not enough data to generate observations.")
        return

    for text in observations:
        # text uses **bold** markers; convert to <b> for the card layout
        parts = text.split("**")
        rendered = "".join(
            f"<b>{esc(p)}</b>" if i % 2 else esc(p)
            for i, p in enumerate(parts)
        )
        st.markdown(
            f'<div class="obs-item">{rendered}</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# Chart helpers (titles are rendered by card(), not matplotlib)
# ------------------------------------------------------------

def hbar_chart(
    df, label_col, value_col, xlabel,
    fmt="%.1f", colour=BLUE, top_n=10,
    highlight=True, highlight_colour=BLUE_DARK,
    ref_line=None, ref_label="Average"
):
    if (
        df is None
        or df.empty
        or label_col not in df.columns
        or value_col not in df.columns
    ):
        st.info("Chart data is not available.")
        return

    data = df[[label_col, value_col]].copy()
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = (
        data.dropna()
        .sort_values(value_col, ascending=True)
        .tail(top_n)
    )

    if data.empty:
        st.info("No numeric data available for this chart.")
        return

    colours = [colour] * len(data)
    if highlight:
        colours[-1] = highlight_colour

    fig, ax = new_fig(5.6, max(2.4, 0.34 * len(data) + 1.0))

    bars = ax.barh(
        data[label_col].astype(str),
        data[value_col],
        color=colours,
        height=0.6
    )

    ax.set_xlabel(xlabel, fontsize=8.5, color="#64748B")
    style_axes(ax, "x")

    ax.bar_label(bars, fmt=fmt, padding=3, fontsize=8, color=BLUE_DARK)

    if ref_line is not None and pd.notna(ref_line):
        ax.axvline(
            ref_line, color=WARN, linestyle="--", linewidth=1.2,
            label=f"{ref_label}: {ref_line:.1f}"
        )
        ax.legend(loc="lower right", frameon=False, fontsize=8)

    ax.margins(x=0.14)
    fig.tight_layout()
    render_fig(fig)


def variance_chart(df, label_col, actual_col, expected_col, unit="days", top_n=10):
    needed = [label_col, actual_col, expected_col]

    if df is None or df.empty or not all(c in df.columns for c in needed):
        st.info("Chart data is not available.")
        return

    data = df[needed].copy()
    data[actual_col] = pd.to_numeric(data[actual_col], errors="coerce")
    data[expected_col] = pd.to_numeric(data[expected_col], errors="coerce")
    data = data.dropna()

    if data.empty:
        st.info("No numeric data available for this chart.")
        return

    data["variance"] = data[actual_col] - data[expected_col]
    data = data.sort_values("variance", ascending=True).tail(top_n)

    colours = [WARN if v > 0 else BLUE_MID for v in data["variance"]]

    fig, ax = new_fig(5.6, max(2.4, 0.34 * len(data) + 1.0))

    bars = ax.barh(
        data[label_col].astype(str),
        data["variance"],
        color=colours,
        height=0.6
    )

    ax.axvline(0, color="#475569", linewidth=0.9)
    ax.set_xlabel(
        f"Actual minus expected lead time ({unit})",
        fontsize=8.5, color="#64748B"
    )
    style_axes(ax, "x")
    ax.bar_label(bars, fmt="%+.1f", padding=3, fontsize=8, color=BLUE_DARK)
    ax.margins(x=0.18)
    fig.tight_layout()
    render_fig(fig)


def grouped_hbar_chart(df, label_col, series, xlabel, sort_col, top_n=10):
    """series: list of (column, legend label, colour); first series is drawn on top."""
    needed = [label_col, sort_col] + [s[0] for s in series]

    if df is None or df.empty or not all(c in df.columns for c in needed):
        st.info("Chart data is not available.")
        return

    data = df[list(dict.fromkeys(needed))].copy()

    for col in dict.fromkeys([sort_col] + [s[0] for s in series]):
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna().sort_values(sort_col, ascending=True).tail(top_n)

    if data.empty:
        st.info("No numeric data available for this chart.")
        return

    count = len(series)
    bar_height = 0.72 / count
    positions = list(range(len(data)))

    fig, ax = new_fig(5.6, max(2.6, 0.44 * len(data) + 1.0))

    for index, (col, label, colour) in enumerate(series):
        offset = ((count - 1) / 2 - index) * bar_height
        ax.barh(
            [p + offset for p in positions],
            data[col],
            height=bar_height,
            color=colour,
            label=label
        )

    ax.set_yticks(positions)
    ax.set_yticklabels(data[label_col].astype(str))
    ax.set_xlabel(xlabel, fontsize=8.5, color="#64748B")
    style_axes(ax, "x")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    ax.margins(x=0.06)
    fig.tight_layout()
    render_fig(fig)


def donut_compact(counts, colour_map=None, centre_label="records"):
    counts = counts[counts > 0]

    if counts.empty:
        st.info("No category data available.")
        return

    labels = [str(i) for i in counts.index]

    if colour_map:
        colours = [colour_map.get(label, BLUE_LIGHT) for label in labels]
    else:
        colours = [
            DONUT_COLOURS[i % len(DONUT_COLOURS)]
            for i in range(len(labels))
        ]

    fig, ax = new_fig(4.6, 3.4)

    wedges, _, autotexts = ax.pie(
        counts.values,
        colors=colours,
        startangle=90,
        autopct=lambda p: f"{p:.0f}%" if p >= 6 else "",
        pctdistance=0.79,
        wedgeprops={"width": 0.38, "edgecolor": "#FFFFFF", "linewidth": 2}
    )

    dark = (BLUE_DARK, BLUE, BAD, WARN)

    for text, colour in zip(autotexts, colours):
        text.set_fontsize(8)
        text.set_fontweight("bold")
        text.set_color("#FFFFFF" if colour in dark else BLUE_DARK)

    ax.text(
        0, 0.06, f"{int(counts.sum()):,}",
        ha="center", va="center",
        fontsize=16, fontweight="bold", color=BLUE_DARK
    )
    ax.text(
        0, -0.18, centre_label,
        ha="center", va="center", fontsize=8, color="#718096"
    )

    ax.legend(
        wedges,
        [f"{l} ({int(v):,})" for l, v in zip(labels, counts.values)],
        loc="upper center",
        bbox_to_anchor=(0.5, 0.02),
        ncol=min(len(labels), 3),
        frameon=False,
        fontsize=8
    )

    ax.axis("equal")
    fig.tight_layout()
    render_fig(fig)


def stacked_bar_chart(data, colour_map, percent=True, xlabel=None, top_n=10):
    """data: rows = categories, columns = series."""
    if data is None or data.empty:
        st.info("Chart data is not available.")
        return

    data = data.tail(top_n)
    columns = list(data.columns)

    fig, ax = new_fig(5.6, max(2.6, 0.38 * len(data) + 1.4))

    left = pd.Series(0.0, index=data.index)

    for col in columns:
        ax.barh(
            data.index.astype(str),
            data[col].values,
            left=left.values,
            color=colour_map.get(str(col), BLUE_LIGHT),
            height=0.6,
            label=str(col)
        )
        left = left + data[col]

    style_axes(ax, "x")

    if percent:
        ax.set_xlim(0, 100)
        ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0f}%")
    elif xlabel:
        ax.set_xlabel(xlabel, fontsize=8.5, color="#64748B")

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12 if percent else -0.2),
        ncol=min(len(columns), 4),
        frameon=False,
        fontsize=8
    )
    fig.tight_layout()
    render_fig(fig)


def hist_chart(values, xlabel, bins=15):
    values = pd.to_numeric(values, errors="coerce").dropna()

    if values.empty:
        st.info("No numeric data available for this chart.")
        return

    fig, ax = new_fig(5.6, 3.1)

    ax.hist(
        values,
        bins=min(bins, max(5, int(values.nunique()))),
        color=BLUE_MID,
        edgecolor="#FFFFFF"
    )
    ax.axvline(
        values.mean(), color=BLUE_DARK, linestyle="--", linewidth=1.3,
        label=f"Mean {values.mean():.1f}"
    )
    ax.axvline(
        values.median(), color=WARN, linestyle=":", linewidth=1.6,
        label=f"Median {values.median():.1f}"
    )

    style_axes(ax, "y")
    ax.set_xlabel(xlabel, fontsize=8.5, color="#64748B")
    ax.set_ylabel("Orders", fontsize=8.5, color="#64748B")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    render_fig(fig)


def box_chart(df, group_col, value_col, xlabel, top_n=10):
    if (
        df is None
        or df.empty
        or group_col not in df.columns
        or value_col not in df.columns
    ):
        st.info("Chart data is not available.")
        return

    data = df[[group_col, value_col]].copy()
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = data.dropna()

    if data.empty:
        st.info("No numeric data available for this chart.")
        return

    medians = data.groupby(group_col)[value_col].median().sort_values()
    groups = list(medians.index)[-top_n:]
    series = [data.loc[data[group_col] == g, value_col].values for g in groups]

    version = tuple(int(x) for x in mpl.__version__.split(".")[:2])
    orient = (
        {"orientation": "horizontal"} if version >= (3, 10)
        else {"vert": False}
    )

    fig, ax = new_fig(5.6, max(2.6, 0.4 * len(groups) + 1.0))

    bp = ax.boxplot(
        series,
        patch_artist=True,
        showfliers=False,
        widths=0.55,
        medianprops={"color": BLUE_DARK, "linewidth": 1.6},
        **orient
    )

    for patch in bp["boxes"]:
        patch.set(facecolor=BLUE_PALE, edgecolor=BLUE_MID)

    ax.set_yticks(range(1, len(groups) + 1))
    ax.set_yticklabels([str(g) for g in groups])
    ax.set_xlabel(xlabel, fontsize=8.5, color="#64748B")
    style_axes(ax, "x")
    fig.tight_layout()
    render_fig(fig)


# ------------------------------------------------------------
# Data helpers
# ------------------------------------------------------------

def alert_snapshot(df):
    """Latest record per product (and warehouse, when available)."""
    data = df.copy()

    keys = ["product_id"]
    for col in ("warehouse_id", "warehouse_name"):
        if col in data.columns:
            keys.append(col)
            break

    if "date" in data.columns and "product_id" in data.columns:
        data["_date"] = pd.to_datetime(data["date"], errors="coerce")
        data = data.sort_values("_date")
        data = data.drop_duplicates(subset=keys, keep="last")
        data = data.drop(columns=["_date"])

    return data


def find_days_column(df):
    """A numeric 'total ... days' column in the outbound analysis, if any."""
    for col in df.columns:
        lowered = col.lower()
        if "total" in lowered and "day" in lowered:
            if pd.to_numeric(df[col], errors="coerce").notna().any():
                return col
    return None


def find_stage_columns(df):
    processing = shipping = None

    for col in df.columns:
        lowered = col.lower()
        if "day" not in lowered or "total" in lowered:
            continue
        if processing is None and "process" in lowered:
            processing = col
        elif shipping is None and ("shipping" in lowered or "transit" in lowered):
            shipping = col

    if processing and shipping:
        return processing, shipping
    return None, None


# ============================================================
# 7. OVERVIEW
# ============================================================

if page == "Overview":

    page_header(
        "Dashboard",
        "A consolidated view of inventory, supplier performance, "
        "customer deliveries and disruption risk."
    )

    # --------------------------------------------------------
    # 1. FIGURES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 2. KPI CARDS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 3. INVENTORY AND DELIVERY HEALTH
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 4. SUPPLIER RELIABILITY
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 5. WAREHOUSES AND DISRUPTION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 6. OPERATIONAL TABLES
    # --------------------------------------------------------

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


# ============================================================
# 8. UC1 - INBOUND REORDER
# ============================================================

elif page == "UC1 - Inbound Reorder":

    page_header(
        "Inbound Reorder Analysis",
        "Monitor stock availability, identify replenishment requirements "
        "and evaluate supplier reliability."
    )

    if reorder_alerts.empty or supplier_performance.empty:
        st.error("UC1 output files are missing. Run uc1_analysis.py first.")
        st.stop()

    # --------------------------------------------------------
    # 1. CLEAN DATA
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

    # --------------------------------------------------------
    # 2. KPI CARDS
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

    # --------------------------------------------------------
    # 3. REORDER EXPOSURE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 4. PRODUCTS REQUIRING ATTENTION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 5. SUPPLIER DELIVERY PERFORMANCE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 6. KEY OBSERVATIONS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 7. DETAIL TABLES
    # --------------------------------------------------------

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


# ============================================================
# 9. UC2 - OUTBOUND DELIVERIES
# ============================================================

elif page == "UC2 - Outbound Deliveries":

    page_header(
        "Outbound Delivery Analysis",
        "Track customer order fulfilment, evaluate warehouse performance "
        "and identify delivery delays."
    )

    if delivery_summary.empty or outbound_analysis.empty:
        st.error("UC2 output files are missing. Run uc2_analysis.py first.")
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

    if "average_total_days" in warehouse_view.columns:
        warehouse_view["average_total_days"] = pd.to_numeric(
            warehouse_view["average_total_days"], errors="coerce"
        )

    days_col = find_days_column(outbound_view)
    processing_col, shipping_col = find_stage_columns(outbound_view)

    # --------------------------------------------------------
    # 2. SUMMARY
    # --------------------------------------------------------

    section_heading("Delivery Performance Summary")
    summary_cards(delivery_summary, per_row=4)

    # --------------------------------------------------------
    # 3. DELIVERY OUTCOMES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 4. DELAY HOTSPOTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 5. DELIVERY TIME DISTRIBUTION (only when a total-days column exists)
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 6. KEY OBSERVATIONS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 7. DETAIL TABLES
    # --------------------------------------------------------

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


# ============================================================
# 10. UC3 - SUPPLIER CONTROL TOWER
# ============================================================

elif page == "UC3 - Supplier Control Tower":

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

    # --------------------------------------------------------
    # 1. PREPARE DATA
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 2. KPI CARDS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 3. SUPPLIER DISRUPTION PROFILE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 4. CUSTOMER ORDER IMPACT
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 5. KEY OBSERVATIONS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 6. DETAIL TABLES
    # --------------------------------------------------------

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

