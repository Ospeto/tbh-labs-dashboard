"""
TBH Labs Myanmar — Interactive Performance Dashboard
=====================================================
Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TBH Labs Myanmar — Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dracula Palette ──────────────────────────────────────────────────────────
BG        = "#282a36"
CURRENT   = "#44475a"
FG        = "#f8f8f2"
COMMENT   = "#6272a4"
CYAN      = "#8be9fd"
GREEN     = "#50fa7b"
ORANGE    = "#ffb86c"
PINK      = "#ff79c6"
PURPLE    = "#bd93f9"
RED       = "#ff5555"
YELLOW    = "#f1fa8c"

COLORS = [CYAN, GREEN, ORANGE, PINK, PURPLE, RED, YELLOW, "#8be9fd", "#ff79c6", "#50fa7b", "#ffb86c", "#bd93f9"]

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    /* Force Streamlit dark backgrounds */
    .stApp {{ background-color: {BG}; }}
    section[data-testid="stSidebar"] {{ background-color: #21222c; }}
    section[data-testid="stSidebar"] * {{ color: {FG}; }}

    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* Header */
    .dashboard-header {{
        background: linear-gradient(135deg, #282a36 0%, #44475a 50%, {PURPLE} 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(189, 147, 249, 0.25);
        border: 1px solid {CURRENT};
    }}
    .dashboard-header h1 {{
        color: {FG};
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.5px;
    }}
    .dashboard-header p {{
        color: {COMMENT};
        font-size: 0.95rem;
        margin: 0;
    }}

    /* KPI Cards */
    .kpi-container {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }}
    .kpi-card {{
        flex: 1;
        min-width: 160px;
        background: {CURRENT};
        border: 1px solid {COMMENT};
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }}
    .kpi-card .kpi-value {{
        font-size: 1.7rem;
        font-weight: 800;
        font-family: 'Fira Code', monospace;
        color: {PURPLE};
        line-height: 1.2;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.75rem;
        color: {COMMENT};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.3rem;
    }}

    /* Section headers */
    .section-header {{
        background: linear-gradient(90deg, {CURRENT}, transparent);
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid {PURPLE};
        margin: 2rem 0 1rem 0;
    }}
    .section-header h2 {{
        color: {FG};
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }}

    /* Insight box */
    .insight-box {{
        background: {CURRENT};
        border: 1px solid {CYAN};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0 1rem 0;
        color: {FG};
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    .insight-box strong {{ color: {CYAN}; }}

    /* Recommendation cards */
    .rec-card {{
        background: {CURRENT};
        border: 1px solid {COMMENT};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }}
    .rec-card.green {{ border-left: 4px solid {GREEN}; }}
    .rec-card.red {{ border-left: 4px solid {RED}; }}
    .rec-card.blue {{ border-left: 4px solid {PURPLE}; }}
    .rec-card h4 {{ color: {FG}; margin: 0 0 0.3rem 0; font-size: 0.95rem; }}
    .rec-card p {{ color: {COMMENT}; margin: 0; font-size: 0.85rem; line-height: 1.4; }}

    div[data-testid="stMetric"] {{
        background: {CURRENT};
        border: 1px solid {COMMENT};
        border-radius: 12px;
        padding: 1rem;
    }}

    .stPlotlyChart {{ border-radius: 12px; overflow: hidden; }}

    /* Dataframe */
    .stDataFrame {{ border-radius: 8px; overflow: hidden; }}

    /* Streamlit Inputs (Select, Multiselect, Dropdowns) */
    div[data-baseweb="select"] > div {{
        background-color: {BG};
        border-color: {COMMENT};
        color: {FG};
    }}
    span[data-baseweb="tag"] {{
        background-color: {CURRENT};
        color: {FG};
        border: 1px solid {COMMENT};
    }}
    div[role="listbox"] {{
        background-color: {BG};
    }}
    div[role="listbox"] li {{
        color: {FG};
    }}
    div[role="listbox"] li:hover {{
        background-color: {CURRENT};
    }}
    div[role="listbox"] li[aria-selected="true"] {{
        background-color: {CURRENT};
        color: {PURPLE};
    }}
</style>
""", unsafe_allow_html=True)


# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("TBH_Labs_Myanmar_Videos.csv")
    df["upload_date"] = pd.to_datetime(df["upload_date"])
    df["year"] = df["upload_date"].dt.year
    df["month"] = df["upload_date"].dt.to_period("M").astype(str)
    df["quarter"] = df["upload_date"].dt.to_period("Q").astype(str)
    df["month_num"] = df["upload_date"].dt.month
    df["duration_min"] = df["duration_seconds"] / 60
    return df

df_all = load_data()
df = df_all[df_all["year"] >= 2021].copy()

# ── Plot theme ───────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(40,42,54,0)",
    plot_bgcolor="rgba(68,71,90,0.4)",
    font=dict(family="Inter", color=FG, size=13),
    margin=dict(l=50, r=30, t=50, b=50),
    hoverlabel=dict(bgcolor=CURRENT, font_size=13, bordercolor=COMMENT),
)


# ═══════════════════ HEADER ═══════════════════════════════════════════════════
st.markdown(f"""
<div class="dashboard-header">
    <h1>📊 TBH Labs Myanmar</h1>
    <p>YouTube Channel Performance Dashboard &nbsp;|&nbsp; 2021 – 2026 &nbsp;|&nbsp; 734 Videos Analyzed</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════ KPI ROW ══════════════════════════════════════════════════
total_views = df["view_count"].sum()
avg_views = df["view_count"].mean()
med_views = df["view_count"].median()
total_videos = len(df)
like_rate = df["like_count"].sum() / df["view_count"].sum() * 100
avg_dur = df["duration_seconds"].mean()

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-value">{total_views/1e6:.1f}M</div>
        <div class="kpi-label">Total Views</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{avg_views/1e3:.1f}K</div>
        <div class="kpi-label">Avg Views / Video</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{med_views/1e3:.1f}K</div>
        <div class="kpi-label">Median Views</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{total_videos}</div>
        <div class="kpi-label">Videos</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{like_rate:.1f}%</div>
        <div class="kpi-label">Like Rate</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{int(avg_dur//60)}:{int(avg_dur%60):02d}</div>
        <div class="kpi-label">Avg Duration</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SIDEBAR ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    years = sorted(df["year"].unique())
    sel_years = st.multiselect("Year", years, default=years)

    categories = sorted(df["category"].unique())
    sel_cats = st.multiselect("Category", categories, default=categories)

    min_views = st.slider("Min Views", 0, int(df["view_count"].max()), 0, step=1000)

    st.markdown("---")
    st.markdown("### 📌 Navigation")
    st.markdown("""
    - [Overview](#overview)
    - [Time Series](#time-series-trends)
    - [Duration](#duration-analysis)
    - [Upload Timing](#best-upload-timing)
    - [Categories](#category-performance)
    - [Recommendations](#expert-recommendations)
    """)

fdf = df[(df["year"].isin(sel_years)) & (df["category"].isin(sel_cats)) & (df["view_count"] >= min_views)]


# ═══════════════════ SECTION 1: OVERVIEW ══════════════════════════════════════
st.markdown('<div class="section-header"><h2>📈 Overview</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(fdf, x="view_count", nbins=50,
                       title="View Count Distribution",
                       color_discrete_sequence=[PURPLE])
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(title="Views", gridcolor=CURRENT)
    fig.update_yaxes(title="Number of Videos", gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    pcts = [10, 25, 50, 75, 90]
    fig2 = go.Figure(data=[go.Bar(
        x=[f"P{p}" for p in pcts],
        y=[fdf["view_count"].quantile(p/100) for p in pcts],
        marker_color=[COMMENT, COMMENT, CYAN, COMMENT, COMMENT],
        text=[f"{int(fdf['view_count'].quantile(p/100)):,}" for p in pcts],
        textposition="outside",
        textfont=dict(color=FG, size=13)
    )])
    fig2.update_layout(title="View Count Percentiles", **PLOT_LAYOUT)
    fig2.update_xaxes(title="Percentile", gridcolor=CURRENT)
    fig2.update_yaxes(title="Views", gridcolor=CURRENT)
    st.plotly_chart(fig2, use_container_width=True)

# Top 10 videos
st.markdown("#### 🏆 Top 10 Videos")
top10 = fdf.nlargest(10, "view_count")[["title", "view_count", "like_count", "comment_count", "duration", "upload_date", "category"]]
top10 = top10.reset_index(drop=True)
top10.index = top10.index + 1
top10.columns = ["Title", "Views", "Likes", "Comments", "Duration", "Date", "Category"]
st.dataframe(top10, use_container_width=True)


# ═══════════════════ SECTION 2: TIME SERIES ═══════════════════════════════════
st.markdown('<div class="section-header"><h2>📅 Time Series Trends</h2></div>', unsafe_allow_html=True)

monthly = fdf.groupby("month").agg(
    count=("view_count", "size"),
    avg_views=("view_count", "mean"),
    total_views=("view_count", "sum"),
    avg_likes=("like_count", "mean"),
    like_rate=("like_count", lambda x: x.sum()),
    view_sum=("view_count", lambda x: x.sum()),
).reset_index()
monthly["like_rate_pct"] = monthly["like_rate"] / monthly["view_sum"] * 100
monthly["roll_3m"] = monthly["avg_views"].rolling(3, min_periods=1).mean()

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["avg_views"],
                             mode="lines", name="Avg Views",
                             line=dict(color=PURPLE, width=1),
                             fill="tozeroy", fillcolor="rgba(189,147,249,0.1)"))
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["roll_3m"],
                             mode="lines", name="3M Rolling Avg",
                             line=dict(color=ORANGE, width=3)))
    fig.update_layout(title="Monthly Avg Views (with 3M Rolling Average)", **PLOT_LAYOUT,
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(40,42,54,0.7)"))
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly["month"], y=monthly["count"],
                         marker_color=GREEN, name="Videos", opacity=0.8))
    fig.update_layout(title="Upload Frequency (Videos per Month)", **PLOT_LAYOUT)
    fig.update_yaxes(title="Videos", gridcolor=CURRENT)
    fig.update_xaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

# Quarterly
quarterly = fdf.groupby("quarter").agg(
    count=("view_count", "size"),
    avg_views=("view_count", "mean"),
    total_views=("view_count", "sum"),
).reset_index()

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(quarterly, x="quarter", y="avg_views",
                 title="Quarterly Avg Views",
                 color_discrete_sequence=[PURPLE])
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonal = fdf.groupby("month_num")["view_count"].mean().reindex(range(1,13)).fillna(0)
    fig = go.Figure(go.Bar(
        x=[month_names[i] for i in range(12)],
        y=seasonal.values,
        marker_color=[RED if v == seasonal.max() else CYAN for v in seasonal.values],
    ))
    fig.update_layout(title="Seasonal Pattern (Avg Views by Month of Year)", **PLOT_LAYOUT)
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

# Engagement trend — FIXED: separate subplots instead of overlapping dual-axis
st.markdown("#### 📊 Engagement Trend")
eng_q = fdf.groupby("quarter").agg(
    like_sum=("like_count", "sum"),
    view_sum=("view_count", "sum"),
    avg_comments=("comment_count", "mean"),
).reset_index()
eng_q["like_rate"] = eng_q["like_sum"] / eng_q["view_sum"] * 100

from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=("Like Rate % Over Time", "Avg Comments Per Video"),
                    vertical_spacing=0.12, row_heights=[0.5, 0.5])

fig.add_trace(go.Scatter(x=eng_q["quarter"], y=eng_q["like_rate"],
                         mode="lines+markers", name="Like Rate %",
                         line=dict(color=GREEN, width=3),
                         marker=dict(size=6)), row=1, col=1)

fig.add_trace(go.Bar(x=eng_q["quarter"], y=eng_q["avg_comments"],
                     name="Avg Comments", marker_color=PURPLE, opacity=0.7), row=2, col=1)

fig.update_layout(
    height=450,
    showlegend=False,
    **{k: v for k, v in PLOT_LAYOUT.items() if k != "margin"},
    margin=dict(l=50, r=30, t=40, b=40),
)
fig.update_xaxes(gridcolor=CURRENT)
fig.update_yaxes(gridcolor=CURRENT)
fig.update_annotations(font_color=FG, font_size=13)
st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown(f"""
<div class="insight-box">
    <strong>💡 Key Insight:</strong> Engagement is at an all-time high — like rate climbed from 3.3% (2021) to 5.35% (2026 Q1),
    a <strong>60% increase</strong>. Average comments grew from 25 to 269 — a <strong>10× increase</strong>.
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SECTION 3: DURATION ══════════════════════════════════════
st.markdown('<div class="section-header"><h2>⏱️ Duration Analysis</h2></div>', unsafe_allow_html=True)

buckets = [(0, 3), (3, 5), (5, 8), (8, 10), (10, 15), (15, 20), (20, 30), (30, 999)]
bucket_labels = ["0–3m", "3–5m", "5–8m", "8–10m", "10–15m", "15–20m", "20–30m", "30+m"]

dur_data = []
for (lo, hi), label in zip(buckets, bucket_labels):
    mask = (fdf["duration_min"] >= lo) & (fdf["duration_min"] < hi)
    group = fdf[mask]
    if len(group) > 0:
        dur_data.append({
            "Bucket": label,
            "Count": len(group),
            "Avg Views": group["view_count"].mean(),
            "Med Views": group["view_count"].median(),
            "Avg Likes": group["like_count"].mean(),
        })

dur_df = pd.DataFrame(dur_data)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dur_df["Bucket"], y=dur_df["Avg Views"],
                         name="Avg Views",
                         marker_color=[GREEN if v == dur_df["Avg Views"].max() else CYAN for v in dur_df["Avg Views"]]))
    fig.add_trace(go.Scatter(x=dur_df["Bucket"], y=dur_df["Med Views"],
                             name="Median Views", mode="lines+markers",
                             line=dict(color=ORANGE, width=3),
                             marker=dict(size=8)))
    fig.update_layout(title="Views by Duration Bucket", **PLOT_LAYOUT,
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(40,42,54,0.7)"))
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = px.scatter(fdf[fdf["duration_min"] <= 60], x="duration_min", y="view_count",
                     color="category", title="Views vs Duration (scatter)",
                     color_discrete_sequence=COLORS, opacity=0.5,
                     hover_data=["title"])
    fig.update_layout(**PLOT_LAYOUT, showlegend=False)
    fig.update_xaxes(title="Duration (minutes)", gridcolor=CURRENT)
    fig.update_yaxes(title="Views", gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown(f"""
<div class="insight-box">
    <strong>💡 Optimal Duration: 15–20 minutes</strong> — delivers 2.5× the channel average (148K avg views)
    with a strong sample size of 89 videos.
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SECTION 4: UPLOAD TIMING ═════════════════════════════════
st.markdown('<div class="section-header"><h2>🕐 Best Upload Timing</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = fdf.groupby("day_of_week")["view_count"].mean().reindex(day_order).reset_index()
    day_df.columns = ["Day", "Avg Views"]

    fig = go.Figure(go.Bar(
        x=day_df["Day"], y=day_df["Avg Views"],
        marker_color=[GREEN if d == "Tuesday" else PURPLE for d in day_df["Day"]],
        text=[f"{v/1000:.0f}K" for v in day_df["Avg Views"]],
        textposition="outside", textfont=dict(color=FG)
    ))
    fig.update_layout(title="Avg Views by Day of Week", **PLOT_LAYOUT)
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fdf_hour = fdf.copy()
    fdf_hour["hour"] = fdf_hour["upload_hour"].str.split(":").str[0].astype(int)
    hour_df = fdf_hour.groupby("hour")["view_count"].mean().reset_index()
    hour_df.columns = ["Hour", "Avg Views"]

    fig = go.Figure(go.Bar(
        x=[f"{h:02d}:00" for h in hour_df["Hour"]],
        y=hour_df["Avg Views"],
        marker_color=CYAN,
    ))
    fig.update_layout(title="Avg Views by Upload Hour (UTC)", **PLOT_LAYOUT)
    fig.update_xaxes(gridcolor=CURRENT)
    fig.update_yaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

# Heatmap
fdf_heat = fdf.copy()
fdf_heat["hour"] = fdf_heat["upload_hour"].str.split(":").str[0].astype(int)
heat = fdf_heat.groupby(["day_of_week", "hour"])["view_count"].mean().reset_index()
heat_pivot = heat.pivot_table(index="day_of_week", columns="hour", values="view_count", fill_value=0)
heat_pivot = heat_pivot.reindex(day_order)

# Dracula-flavored colorscale
dracula_scale = [
    [0, BG],
    [0.25, COMMENT],
    [0.5, PURPLE],
    [0.75, PINK],
    [1, CYAN]
]

fig = go.Figure(data=go.Heatmap(
    z=heat_pivot.values,
    x=[f"{h:02d}:00" for h in heat_pivot.columns],
    y=heat_pivot.index,
    colorscale=dracula_scale,
    text=[[f"{v/1000:.0f}K" if v > 0 else "" for v in row] for row in heat_pivot.values],
    texttemplate="%{text}",
    textfont={"size": 10, "color": FG},
    hovertemplate="Day: %{y}<br>Hour: %{x}<br>Avg Views: %{z:,.0f}<extra></extra>"
))
fig.update_layout(title="Upload Time Heatmap (Avg Views)", **PLOT_LAYOUT, height=350)
st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown(f"""
<div class="insight-box">
    <strong>💡 Best Upload Slot: Tuesday at 14:00 UTC (8:30 PM Myanmar Time)</strong> — avg 171,600 views
    across 15 uploads, nearly 2× the channel average.
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SECTION 5: CATEGORIES ════════════════════════════════════
st.markdown('<div class="section-header"><h2>🏷️ Category Performance</h2></div>', unsafe_allow_html=True)

cat_stats = fdf.groupby("category").agg(
    count=("view_count", "size"),
    avg_views=("view_count", "mean"),
    med_views=("view_count", "median"),
    total_views=("view_count", "sum"),
    avg_likes=("like_count", "mean"),
    avg_comments=("comment_count", "mean"),
    avg_duration=("duration_min", "mean"),
).reset_index().sort_values("avg_views", ascending=False)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(go.Bar(
        y=cat_stats["category"],
        x=cat_stats["avg_views"],
        orientation="h",
        marker_color=COLORS[:len(cat_stats)],
        text=[f"{v/1000:.0f}K" for v in cat_stats["avg_views"]],
        textposition="outside", textfont=dict(color=FG, size=11),
    ))
    fig.update_layout(title="Avg Views by Category", height=550, **PLOT_LAYOUT)
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(gridcolor=CURRENT)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    # Dracula treemap
    fig = px.treemap(cat_stats, path=["category"], values="total_views",
                     color="avg_views",
                     color_continuous_scale=[[0, COMMENT], [0.5, PURPLE], [1, CYAN]],
                     title="Category Share (by Total Views)")
    fig.update_layout(**PLOT_LAYOUT, height=550)
    fig.update_traces(textinfo="label+percent root",
                      textfont=dict(color=FG, size=13))
    st.plotly_chart(fig, use_container_width=True, theme=None)

# Category mix over time — FIXED: stacked bar chart instead of broken area chart
st.markdown("#### 📊 Category Mix Over Time")
cat_year = fdf.groupby(["year", "category"]).size().reset_index(name="count")
year_totals = fdf.groupby("year").size().reset_index(name="total")
cat_year = cat_year.merge(year_totals, on="year")
cat_year["pct"] = cat_year["count"] / cat_year["total"] * 100

# Select key categories for readability
key_cats = ["Knowledge", "Review", "Showcases", "Battery Drain Test",
            "First Impressions", "Wassup", "Shorts", "uncategorized"]
cat_year_key = cat_year[cat_year["category"].isin(key_cats)].copy()

fig = go.Figure()
for i, cat in enumerate(key_cats):
    cat_data = cat_year_key[cat_year_key["category"] == cat].sort_values("year")
    fig.add_trace(go.Bar(
        x=cat_data["year"],
        y=cat_data["pct"],
        name=cat,
        marker_color=COLORS[i % len(COLORS)],
    ))

fig.update_layout(
    title="Category Mix Evolution (% of uploads per year)",
    barmode="stack",
    **PLOT_LAYOUT,
    legend=dict(x=0, y=-0.25, orientation="h", font=dict(size=10)),
    height=500,
)
fig.update_xaxes(title="Year", gridcolor=CURRENT, dtick=1)
fig.update_yaxes(title="% of Uploads", gridcolor=CURRENT)
st.plotly_chart(fig, use_container_width=True, theme=None)


# ═══════════════════ SECTION 6: RECOMMENDATIONS ══════════════════════════════
st.markdown('<div class="section-header"><h2>🎯 Expert Recommendations</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✅ Double Down")
    st.markdown(f"""
    <div class="rec-card green">
        <h4>1. Knowledge is the growth engine</h4>
        <p>128K avg views, 4.9% like rate, 67.6% of 2026 content. Data fully validates this strategic bet. Aim for 50–60% at steady state.</p>
    </div>
    <div class="rec-card green">
        <h4>2. Target 15–20 minute videos</h4>
        <p>2.5× channel average views with strong engagement. This is the sweet spot for production effort vs. performance.</p>
    </div>
    <div class="rec-card green">
        <h4>3. Upload on Tuesdays at 8:30 PM MMT</h4>
        <p>171,600 avg views — nearly 2× channel average. Make this the primary upload slot for flagship content.</p>
    </div>
    <div class="rec-card green">
        <h4>4. Plan big for Q4 (Sep–Dec)</h4>
        <p>Consistently the strongest quarter. Align tentpole content with iPhone launches, holiday shopping, and year-end roundups.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### ⚠️ Fix or Cut")
    st.markdown(f"""
    <div class="rec-card red">
        <h4>5. Reduce Showcases by 50%</h4>
        <p>28% of content at only 53K avg views — 39% below average. Redirect effort to Knowledge or Comparison.</p>
    </div>
    <div class="rec-card red">
        <h4>6. Stop producing Shorts</h4>
        <p>7,500 avg views — weakest category by far. Shorts rarely convert to long-form subscribers on tech channels.</p>
    </div>
    <div class="rec-card blue">
        <h4>7. Scale hidden gems</h4>
        <p>Comparison (158K avg, 7 videos), Unboxing (151K avg, 11 videos), Company Profiles (133K avg, 3 videos) — massively underproduced.</p>
    </div>
    <div class="rec-card blue">
        <h4>8. Create branded series</h4>
        <p>"Knowledge Tuesday" at 8:30 PM MMT — creates audience habit, improves notification CTR, signals consistency to the algorithm.</p>
    </div>
    """, unsafe_allow_html=True)

# KPI targets
st.markdown("#### 📊 KPI Targets")
kpi_df = pd.DataFrame({
    "Metric": ["Avg Views/Video", "Like Rate", "Knowledge Share", "Showcases Share", "Videos/Month", "Median Views"],
    "Current": ["87,565", "5.35%", "67.6%", "13.5%", "13.8", "55,686"],
    "6-Month Target": ["100,000", "5.5%", "50–60%", "< 10%", "12–15", "65,000"],
    "12-Month Target": ["120,000", "6.0%", "50–60%", "< 10%", "12–15", "80,000"],
})
st.dataframe(kpi_df, use_container_width=True, hide_index=True)


# ═══════════════════ MILESTONES ═══════════════════════════════════════════════
st.markdown('<div class="section-header"><h2>🏆 Channel Milestones</h2></div>', unsafe_allow_html=True)

milestones_data = {
    "Milestone": ["1M Views", "5M Views", "10M Views", "25M Views", "50M Views"],
    "Reached": ["Dec 2021", "May 2022", "Nov 2022", "Nov 2023", "Apr 2025"],
    "Time": ["Baseline", "5 months", "11 months", "23 months", "40 months"],
}
st.dataframe(pd.DataFrame(milestones_data), use_container_width=True, hide_index=True)

# Cumulative views
cum = fdf.groupby("month")["view_count"].sum().cumsum().reset_index()
cum.columns = ["Month", "Cumulative Views"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=cum["Month"], y=cum["Cumulative Views"],
                         mode="lines", fill="tozeroy",
                         line=dict(color=PURPLE, width=3),
                         fillcolor="rgba(189,147,249,0.12)"))
for val, label in [(1e6, "1M"), (5e6, "5M"), (10e6, "10M"), (25e6, "25M"), (50e6, "50M")]:
    fig.add_hline(y=val, line_dash="dot", line_color=COMMENT,
                  annotation_text=label, annotation_position="bottom right",
                  annotation_font_color=COMMENT)
fig.update_layout(title="Cumulative Views Over Time", **PLOT_LAYOUT, height=400)
fig.update_yaxes(title="Cumulative Views", gridcolor=CURRENT)
fig.update_xaxes(gridcolor=CURRENT)
st.plotly_chart(fig, use_container_width=True, theme=None)


# ═══════════════════ FOOTER ═══════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COMMENT}; font-size: 0.8rem; padding: 1rem;">
    Data sourced via YouTube Data API v3 &nbsp;|&nbsp; Report generated February 28, 2026 &nbsp;|&nbsp;
    Categories assigned from 27 channel playlists
</div>
""", unsafe_allow_html=True)
