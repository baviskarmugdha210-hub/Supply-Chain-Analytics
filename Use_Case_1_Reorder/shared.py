from contextlib import contextmanager
import html
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 4. HELPER FUNCTIONS
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
        title, fontsize=14, fontweight="bold", color="#17365D", pad=16)
    ax.set_xlabel(xlabel, fontsize=10, color="#64748B")
    ax.set_ylabel("")
    ax.tick_params( axis="both", labelsize=9, colors="#475569")
    ax.grid( axis="x", color="#DCE8F5", linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#DCE8F5")
    ax.bar_label( bars, fmt="%.1f", padding=5, fontsize=8, color="#17365D")
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
    blue_palette = [ "#17365D", "#2F6BBA","#6F98CC", "#A9C2E0", "#DCE8F5"]
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
    ax.text(0, 0, f"{counts.sum():,}", ha="center", va="center", fontsize=19, fontweight="bold", color="#17365D")

    ax.set_title( title, fontsize=14, fontweight="bold", color="#17365D", pad=16)

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


# 5. INVENTORY HEALTH PREPARATION

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

# 6B. SHARED DESIGN HELPERS

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
