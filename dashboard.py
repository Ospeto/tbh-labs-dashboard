"""
TBH Labs Myanmar — Interactive Performance Dashboard
=====================================================
Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TBH Labs Myanmar — Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Flash UI Palette ──────────────────────────────────────────────────────────
BG        = "#f8fafc"  # Very light blue-grey
CARD_BG   = "#ffffff"
FG        = "#0f172a"  # Slate 900
TEXT_MUTED= "#64748b"  # Slate 500
BORDER    = "#e2e8f0"  # Slate 200

# Vibrant Tech Gradients/Accents (Flash UI)
PRIMARY   = "#3b82f6"  # Blue
ACCENT_1  = "#8b5cf6"  # Violet
ACCENT_2  = "#ec4899"  # Pink
ACCENT_3  = "#10b981"  # Emerald
ACCENT_4  = "#f59e0b"  # Amber
ACCENT_5  = "#06b6d4"  # Cyan

COLORS = [PRIMARY, ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_5, "#f43f5e", "#8b5cf6", "#14b8a6", "#3b82f6", "#ec4899"]

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{ background-color: {BG}; }}
    
    .main .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }}

    /* Global Typography adjustments */
    h1, h2, h3, h4, h5, h6 {{
        color: {FG} !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
    }}
    p, span, div {{ color: {FG}; }}

    /* Streamlit overrides for clean UI */
    section[data-testid="stSidebar"] {{ 
        background-color: {CARD_BG}; 
        border-right: 1px solid {BORDER};
    }}
    
    div[data-testid="stMetric"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
    }}

    /* The 'Flash' Header */
    .dashboard-header {{
        background: {CARD_BG};
        padding: 3rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 1px solid {BORDER};
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    }}
    /* Gradient swoosh effect */
    .dashboard-header::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: linear-gradient(90deg, {ACCENT_5}, {PRIMARY}, {ACCENT_1}, {ACCENT_2});
    }}
    .dashboard-header h1 {{
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(to right, {FG}, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
    }}
    .dashboard-header p {{
        color: {TEXT_MUTED};
        font-size: 1.1rem;
        margin: 0;
        font-weight: 500;
    }}

    /* Custom KPI Cards */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 1.25rem;
        margin-bottom: 2.5rem;
    }}
    .kpi-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.2s ease;
    }}
    .kpi-card:hover {{
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }}
    .kpi-card .kpi-value {{
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, {PRIMARY}, {ACCENT_1});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin-bottom: 0.25rem;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Section headers */
    .section-header {{
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid {BORDER};
        display: flex;
        align-items: center;
    }}
    .section-header h2 {{
        font-size: 1.5rem;
        margin: 0;
        color: {FG};
    }}

    /* Insight box (Glassmorphism minimalist) */
    .insight-box {{
        background: rgba(59, 130, 246, 0.05);
        border-left: 4px solid {PRIMARY};
        border-radius: 0 12px 12px 0;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0 2rem 0;
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.6;
        font-weight: 500;
    }}
    .insight-box strong {{ color: {FG}; font-weight: 700; }}

    /* Recommendation cards */
    .rec-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }}
    .rec-card:hover {{ transform: scale(1.01); }}
    
    .rec-card.green .rec-icon {{ background: rgba(16, 185, 129, 0.1); color: {ACCENT_3}; }}
    .rec-card.red .rec-icon {{ background: rgba(239, 68, 68, 0.1); color: #ef4444; }}
    .rec-card.blue .rec-icon {{ background: rgba(59, 130, 246, 0.1); color: {PRIMARY}; }}
    
    .rec-card-header {{ display: flex; align-items: center; margin-bottom: 0.75rem; }}
    .rec-icon {{ 
        width: 32px; height: 32px; 
        border-radius: 8px; 
        display: flex; align-items: center; justify-content: center;
        margin-right: 1rem;
        font-weight: 800;
    }}
    
    .rec-card h4 {{ margin: 0; font-size: 1.05rem; font-weight: 700; }}
    .rec-card p {{ color: {TEXT_MUTED}; margin: 0; font-size: 0.9rem; line-height: 1.5; }}

    /* DataFrame styling */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }}
    
    /* Plotly charts container */
    .stPlotlyChart {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        padding: 0.5rem;
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
# Flash UI uses clean white plots with prominent data and subtle grid lines
PLOT_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color=TEXT_MUTED, size=13),
    margin=dict(l=40, r=20, t=60, b=40),
    hoverlabel=dict(
        bgcolor=CARD_BG, 
        font_size=13, 
        font_family="Inter",
        bordercolor=BORDER,
        font_color=FG
    ),
    title_font=dict(size=16, color=FG, family="Inter", weight="bold"),
)

def update_axes(fig):
    fig.update_xaxes(
        gridcolor="#f1f5f9", 
        zerolinecolor="#e2e8f0", 
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(size=13, color=TEXT_MUTED, weight=500)
    )
    fig.update_yaxes(
        gridcolor="#f1f5f9", 
        zerolinecolor="#e2e8f0", 
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(size=13, color=TEXT_MUTED, weight=500)
    )
    return fig


# ═══════════════════ HEADER ═══════════════════════════════════════════════════
st.markdown(f"""
<div class="dashboard-header">
    <h1>⚡ TBH Labs Analytics</h1>
    <p>Strategic Performance Dashboard &nbsp;|&nbsp; 2021–2026 &nbsp;|&nbsp; <b>{len(df_all)}</b> Videos Indexed</p>
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
        <div class="kpi-label">Lifetime Views</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{avg_views/1e3:.1f}K</div>
        <div class="kpi-label">Average Views</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{med_views/1e3:.1f}K</div>
        <div class="kpi-label">Median Views</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{total_videos}</div>
        <div class="kpi-label">Videos Published</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{like_rate:.2f}%</div>
        <div class="kpi-label">Audience Like Rate</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{int(avg_dur//60)}:{int(avg_dur%60):02d}</div>
        <div class="kpi-label">Avg Watch Length</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SIDEBAR ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    st.markdown("<br>", unsafe_allow_html=True)
    
    years = sorted(df["year"].unique())
    sel_years = st.multiselect("Timeline Selection", years, default=years)

    categories = sorted(df["category"].unique())
    sel_cats = st.multiselect("Content Verticals", categories, default=categories)

    min_views = st.slider("View Threshold", 0, int(df["view_count"].max()), 0, step=1000)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### 📌 Navigation")
    st.markdown("""
    - [Overview](#overview)
    - [Time Series Trends](#time-series-trends)
    - [Duration Sweet Spot](#duration-sweet-spot)
    - [Upload Telemetry](#upload-telemetry)
    - [Category Matrices](#category-matrices)
    - [Actionable Intel](#actionable-intel)
    """)

fdf = df[(df["year"].isin(sel_years)) & (df["category"].isin(sel_cats)) & (df["view_count"] >= min_views)]


# ═══════════════════ SECTION 1: OVERVIEW ══════════════════════════════════════
st.markdown('<div class="section-header"><h2>📈 Overview</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(fdf, x="view_count", nbins=50,
                       title="Audience Reach Distribution",
                       color_discrete_sequence=[PRIMARY])
    fig.update_layout(**PLOT_LAYOUT)
    fig = update_axes(fig)
    fig.update_xaxes(title="Total Views")
    fig.update_yaxes(title="Video Count")
    fig.update_traces(marker=dict(line=dict(width=1, color="white")))
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    pcts = [10, 25, 50, 75, 90]
    fig2 = go.Figure(data=[go.Bar(
        x=[f"p{p}" for p in pcts],
        y=[fdf["view_count"].quantile(p/100) for p in pcts],
        marker_color=["#cbd5e1", "#cbd5e1", ACCENT_1, "#cbd5e1", "#cbd5e1"],
        text=[f"{int(fdf['view_count'].quantile(p/100)):,}" for p in pcts],
        textposition="outside",
        textfont=dict(color=FG, size=13, weight="bold"),
        marker=dict(line=dict(width=0))
    )])
    fig2.update_layout(title="Performance Percentiles", **PLOT_LAYOUT)
    fig2 = update_axes(fig2)
    fig2.update_xaxes(title="Percentile Rank")
    fig2.update_yaxes(title="Total Views", range=[0, fdf["view_count"].quantile(0.9)*1.3])
    st.plotly_chart(fig2, use_container_width=True, theme=None)

# Top 10 videos
st.markdown("#### ⭐ High Impact Content (Top 10)")
top10 = fdf.nlargest(10, "view_count")[["title", "view_count", "like_count", "comment_count", "duration", "upload_date", "category"]]
top10 = top10.reset_index(drop=True)
top10.index = top10.index + 1
top10.columns = ["Content Title", "Reach", "Likes", "Engagement", "Duration", "Air Date", "Vertical"]
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
                             mode="lines", name="Monthly Avg",
                             line=dict(color="#cbd5e1", width=2),
                             fill="tozeroy", fillcolor="rgba(203, 213, 225, 0.2)"))
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["roll_3m"],
                             mode="lines", name="3M Momentum",
                             line=dict(color=PRIMARY, width=4)))
    fig.update_layout(title="View Volume Momentum", **PLOT_LAYOUT,
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=BORDER, borderwidth=1))
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly["month"], y=monthly["count"],
                         marker_color=ACCENT_5, name="Uploads", 
                         marker=dict(line=dict(width=0))))
    fig.update_layout(title="Production Velocity (Uploads/Month)", **PLOT_LAYOUT)
    fig = update_axes(fig)
    fig.update_yaxes(title="Volume")
    st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown("#### 💬 Engagement Multipliers")
eng_q = fdf.groupby("quarter").agg(
    like_sum=("like_count", "sum"),
    view_sum=("view_count", "sum"),
    avg_comments=("comment_count", "mean"),
).reset_index()
eng_q["like_rate"] = eng_q["like_sum"] / eng_q["view_sum"] * 100

fig = make_subplots(rows=1, cols=2, shared_xaxes=False,
                    subplot_titles=("Audience Like Rate (%)", "Conversation Depth (Avg Comments)"))

fig.add_trace(go.Scatter(x=eng_q["quarter"], y=eng_q["like_rate"],
                         mode="lines+markers", line=dict(color=ACCENT_3, width=3),
                         fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.1)",
                         marker=dict(size=8, color=ACCENT_3, line=dict(color="white", width=2))), row=1, col=1)

fig.add_trace(go.Bar(x=eng_q["quarter"], y=eng_q["avg_comments"],
                     marker_color=ACCENT_2, opacity=0.85,
                     marker=dict(line=dict(width=0))), row=1, col=2)

fig.update_layout(
    height=380, showlegend=False,
    **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["margin", "height"]}
)
fig.update_annotations(font_color=FG, font_size=16, font_family="Inter", font_weight="bold")
fig = update_axes(fig)
st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown(f"""
<div class="insight-box">
    <strong>💡 The Engagement Surge:</strong> The audience is deeper into the funnel than ever. Like rate skyrocketed from 3.3% (2021) to <strong>5.35% (2026 Q1)</strong>,
    while average comments <strong>10x'd</strong> (25 → 269). Less passive viewing, more active community participation.
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SECTION 3: DURATION ══════════════════════════════════════
st.markdown('<div class="section-header"><h2>⏱️ Duration Sweet Spot</h2></div>', unsafe_allow_html=True)

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
        })

dur_df = pd.DataFrame(dur_data)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dur_df["Bucket"], y=dur_df["Avg Views"],
                         name="Average Reach",
                         marker_color=["#cbd5e1" if v < dur_df["Avg Views"].max() else ACCENT_1 for v in dur_df["Avg Views"]],
                         marker=dict(line=dict(width=0))))
    fig.add_trace(go.Scatter(x=dur_df["Bucket"], y=dur_df["Med Views"],
                             name="Median Reach", mode="lines+markers",
                             line=dict(color=FG, width=3),
                             marker=dict(size=8, color=CARD_BG, line=dict(color=FG, width=2))))
    fig.update_layout(title="Reach Density by Format Length", **PLOT_LAYOUT,
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=BORDER, borderwidth=1))
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = px.scatter(fdf[fdf["duration_min"] <= 60], x="duration_min", y="view_count",
                     color="category", title="Duration vs Reach Map",
                     color_discrete_sequence=COLORS, opacity=0.7,
                     hover_data=["title"])
    fig.update_layout(**PLOT_LAYOUT, showlegend=False)
    fig.update_traces(marker=dict(line=dict(width=1, color="white")))
    fig = update_axes(fig)
    fig.update_xaxes(title="Runtime (minutes)")
    fig.update_yaxes(title="Total Views")
    st.plotly_chart(fig, use_container_width=True, theme=None)

st.markdown(f"""
<div class="insight-box">
    <strong>💡 Optimal Format 15–20m:</strong> This runtime delivers <strong>2.5× the channel average</strong> (148K avg views)
    with a proven sample size of 89 videos. 30+ minutes performs technically higher on average (due to massive hits), but mid-longform is much safer.
</div>
""", unsafe_allow_html=True)


# ═══════════════════ SECTION 4: UPLOAD TIMING ═════════════════════════════════
st.markdown('<div class="section-header"><h2>🕐 Upload Telemetry</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = fdf.groupby("day_of_week")["view_count"].mean().reindex(day_order).reset_index()
    day_df.columns = ["Day", "Avg Views"]

    fig = go.Figure(go.Bar(
        x=day_df["Day"], y=day_df["Avg Views"],
        marker_color=[PRIMARY if d == "Tuesday" else "#cbd5e1" for d in day_df["Day"]],
        text=[f"{v/1000:.0f}K" for v in day_df["Avg Views"]],
        textposition="outside", textfont=dict(color=FG, weight="bold"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Velocity by Weekday", **PLOT_LAYOUT)
    fig = update_axes(fig)
    fig.update_yaxes(range=[0, day_df["Avg Views"].max() * 1.2])
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fdf_hour = fdf.copy()
    fdf_hour["hour"] = fdf_hour["upload_hour"].str.split(":").str[0].astype(int)
    hour_df = fdf_hour.groupby("hour")["view_count"].mean().reset_index()
    hour_df.columns = ["Hour", "Avg Views"]

    fig = go.Figure(go.Bar(
        x=[f"{h:02d}:00" for h in hour_df["Hour"]],
        y=hour_df["Avg Views"],
        marker_color=ACCENT_5,
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Velocity by Hour (UTC)", **PLOT_LAYOUT)
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ═══════════════════ SECTION 5: CATEGORIES ════════════════════════════════════
st.markdown('<div class="section-header"><h2>🏷️ Category Matrices</h2></div>', unsafe_allow_html=True)

cat_stats = fdf.groupby("category").agg(
    count=("view_count", "size"),
    avg_views=("view_count", "mean"),
    med_views=("view_count", "median"),
    total_views=("view_count", "sum"),
).reset_index().sort_values("avg_views", ascending=False)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(go.Bar(
        y=cat_stats["category"],
        x=cat_stats["avg_views"],
        orientation="h",
        marker_color=COLORS[:len(cat_stats)],
        text=[f"{v/1000:.0f}K" for v in cat_stats["avg_views"]],
        textposition="outside", textfont=dict(color=FG, size=12, weight="600"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Average Reach by Vertical", height=500, **PLOT_LAYOUT)
    fig.update_yaxes(autorange="reversed")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    # Stacked bar area
    cat_year = fdf.groupby(["year", "category"]).size().reset_index(name="count")
    year_totals = fdf.groupby("year").size().reset_index(name="total")
    cat_year = cat_year.merge(year_totals, on="year")
    cat_year["pct"] = cat_year["count"] / cat_year["total"] * 100

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
            marker=dict(line=dict(color=CARD_BG, width=1))
        ))

    fig.update_layout(
        title="Vertical Strategy Evolution (% of timeline)",
        barmode="stack",
        height=500,
        **PLOT_LAYOUT,
        legend=dict(x=0, y=-0.25, orientation="h", font=dict(size=11)),
    )
    fig = update_axes(fig)
    fig.update_xaxes(title="Year", dtick=1)
    fig.update_yaxes(title="% of Output")
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ═══════════════════ SECTION 6: RECOMMENDATIONS ══════════════════════════════
st.markdown('<div class="section-header"><h2>🎯 Actionable Intel</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="rec-card green">
        <div class="rec-card-header">
            <div class="rec-icon">✓</div>
            <h4>Scale the Engine</h4>
        </div>
        <p><b>Knowledge is king.</b> 128K avg views, 4.9% like rate. It claimed 67.6% of output in 2026 for a reason. Stabilize at 50–60% of total schedule at steady state.</p>
    </div>
    <div class="rec-card green">
        <div class="rec-card-header">
            <div class="rec-icon">✓</div>
            <h4>Adopt the 15M Standard</h4>
        </div>
        <p>15-20 min features pull <b>2.5× higher volume.</b> This is the algorithmic sweet spot matching production capability to viewer retention.</p>
    </div>
    <div class="rec-card blue">
        <div class="rec-card-header">
            <div class="rec-icon">↗</div>
            <h4>Leverage Q4 Momentum</h4>
        </div>
        <p>September through December is a massive growth window (iPhone + holiday cycle). Plan major tentpole content well in advance of Q4.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="rec-card red">
        <div class="rec-card-header">
            <div class="rec-icon">✕</div>
            <h4>Sever the Weak Links</h4>
        </div>
        <p><b>Cut Showcases format by half AND completely halt Shorts.</b> Showcases average 39% beneath channel baseline. Shorts are dead weight (7.5K avg) on deep-tech channels.</p>
    </div>
    <div class="rec-card blue">
        <div class="rec-card-header">
            <div class="rec-icon">↗</div>
            <h4>Establish 'Flagship Slots'</h4>
        </div>
        <p><b>Tuesday at 8:30 PM MMT</b> peaks at 171.6K views on average. Treat this window as sacred ground for highest-value productions to hack early-momentum.</p>
    </div>
    <div class="rec-card blue">
        <div class="rec-card-header">
            <div class="rec-icon">↗</div>
            <h4>Scale Hidden Gems</h4>
        </div>
        <p><b>Comparisons (158K) & Unboxings (151K).</b> These are significantly underproduced relative to their high, consistent return profiles.</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════ FOOTER ═══════════════════════════════════════════════════
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: {TEXT_MUTED}; font-size: 0.85rem; padding: 2rem;">
    <b>TBH Labs Operating System</b><br>
    Data sourced live via YouTube Data API v3 &nbsp;•&nbsp; Generated February 28, 2026
</div>
""", unsafe_allow_html=True)
