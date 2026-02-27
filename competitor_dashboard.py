"""
Competitor Analysis — Myanmar Tech YouTube Landscape
=====================================================
Run: streamlit run competitor_dashboard.py --server.port 8503
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Competitor Analysis — TBH Labs",
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

CH_COLORS = {
    "TBH Labs": PRIMARY,
    "Myanmar Mobile Phones & Tech Review": ACCENT_4,
    "MyTech Myanmar": ACCENT_3,
    "ZEST": ACCENT_1,
    "Technity": ACCENT_2,
    "T4U2": ACCENT_5,
}

# ── Custom CSS (Flash UI) ───────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{ background-color: {BG}; }}
    
    .main .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* Global Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {FG} !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
    }}
    p, span, div {{ color: {FG}; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{ 
        background-color: {CARD_BG}; 
        border-right: 1px solid {BORDER};
    }}

    /* Flash Header */
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

    /* Section Headers */
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

    /* Insight box */
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

    /* Tables */
    .rank-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; margin-bottom: 2rem; background: {CARD_BG}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
    .rank-table th {{ background: #f1f5f9; color: {TEXT_MUTED}; padding: 1rem; text-align: left; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.75rem; border-bottom: 1px solid {BORDER}; }}
    .rank-table td {{ padding: 1rem; border-bottom: 1px solid {BORDER}; color: {FG}; font-weight: 500; }}
    .rank-table tr:hover {{ background: #f8fafc; }}
    .rank-highlight {{ background: rgba(59, 130, 246, 0.05) !important; }}

    .stPlotlyChart {{ background: {CARD_BG}; border: 1px solid {BORDER}; border-radius: 16px; padding: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }}
    [data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Competitor_Videos.csv")
    df["upload_date"] = pd.to_datetime(df["upload_date"])
    df["year"] = df["upload_date"].dt.year
    df["month"] = df["upload_date"].dt.to_period("M").astype(str)
    df["quarter"] = df["upload_date"].dt.to_period("Q").astype(str)
    df["duration_min"] = df["duration_seconds"] / 60
    df["engagements"] = df["like_count"] + df["comment_count"]
    df["eng_rate"] = np.where(df["view_count"] > 0, df["engagements"] / df["view_count"] * 100, 0)
    df["like_rate"] = np.where(df["view_count"] > 0, df["like_count"] / df["view_count"] * 100, 0)
    return df

df_all = load_data()

# ── Plot Theme ───────────────────────────────────────────────────────────────
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

ch_names = list(CH_COLORS.keys())
ch_color_map = CH_COLORS

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    years = sorted(df_all["year"].unique())
    sel_years = st.multiselect("Timeline Selection", years, default=[y for y in years if y >= 2021])
    sel_channels = st.multiselect("Channels", ch_names, default=ch_names)
    min_views = st.slider("View Threshold", 0, 50000, 0, step=1000)

df = df_all[
    (df_all["year"].isin(sel_years)) &
    (df_all["channel_name"].isin(sel_channels)) &
    (df_all["view_count"] >= min_views)
].copy()


# ══════════════ HEADER ═══════════════════════════════════════════════════════
st.markdown(f"""
<div class="dashboard-header">
    <h1>⚡ Competitor Intelligence</h1>
    <p>Myanmar Tech YouTube Landscape &nbsp;|&nbsp; <b>{len(df_all):,}</b> Videos indexed across <b>{len(ch_names)}</b> channels</p>
</div>
""", unsafe_allow_html=True)


# ══════════════ SECTION 1: CHANNEL SCORECARD ═════════════════════════════════
st.markdown('<div class="section-header"><h2>📊 Channel Scorecard</h2></div>', unsafe_allow_html=True)

def fmt(v, unit=""):
    if v >= 1_000_000: return f"{v/1e6:.1f}M{unit}"
    if v >= 1_000: return f"{v/1e3:.1f}K{unit}"
    return f"{int(v)}{unit}"

scorecard = df.groupby("channel_name").agg(
    videos=("video_id", "count"),
    total_views=("view_count", "sum"),
    avg_views=("view_count", "mean"),
    med_views=("view_count", "median"),
    total_likes=("like_count", "sum"),
    avg_likes=("like_count", "mean"),
    total_comments=("comment_count", "sum"),
    avg_comments=("comment_count", "mean"),
    avg_eng_rate=("eng_rate", "mean"),
    avg_like_rate=("like_rate", "mean"),
    avg_duration=("duration_min", "mean"),
).reset_index()
scorecard = scorecard.sort_values("avg_views", ascending=False)

rows_html = ""
for i, r in scorecard.iterrows():
    color = ch_color_map.get(r["channel_name"], "#888")
    hl = ' class="rank-highlight"' if r["channel_name"] == "TBH Labs" else ""
    rows_html += f"""<tr{hl}>
        <td><span style="color:{color};font-weight:900;font-size:1.2em;vertical-align:middle;">•</span> {r['channel_name']}</td>
        <td>{r['videos']}</td>
        <td>{fmt(r['total_views'])}</td>
        <td><b>{fmt(r['avg_views'])}</b></td>
        <td>{fmt(r['med_views'])}</td>
        <td>{fmt(r['total_likes'])}</td>
        <td>{r['avg_eng_rate']:.2f}%</td>
        <td>{r['avg_like_rate']:.2f}%</td>
        <td>{r['avg_duration']:.1f}m</td>
    </tr>"""

st.markdown(f"""
<table class="rank-table">
<tr><th>Channel</th><th>Videos</th><th>Total Views</th><th>Avg Views</th><th>Med Views</th>
<th>Total Likes</th><th>Eng Rate</th><th>Like Rate</th><th>Avg Duration</th></tr>
{rows_html}
</table>
""", unsafe_allow_html=True)

if "TBH Labs" in scorecard["channel_name"].values:
    tbh_row = scorecard[scorecard["channel_name"] == "TBH Labs"].iloc[0]
    tbh_rank = list(scorecard["channel_name"]).index("TBH Labs") + 1
    leader = scorecard.iloc[0]
    st.markdown(f"""
    <div class="insight-box">
        <strong>🎯 Market Position:</strong> TBH Labs currently ranks <strong>#{tbh_rank}</strong> out of {len(scorecard)} measured channels by average viewership ({fmt(tbh_row['avg_views'])} avg), while the market leader <strong>{leader['channel_name']}</strong> holds {fmt(leader['avg_views'])} avg views. TBH Labs maintains a healthy <strong>{tbh_row['avg_like_rate']:.2f}%</strong> Like Rate and a <strong>{tbh_row['avg_eng_rate']:.2f}%</strong> overall Engagement Rate.
    </div>
    """, unsafe_allow_html=True)


# ══════════════ SECTION 2: VIEWS DISTRIBUTION ══════════════════════════════════
st.markdown('<div class="section-header"><h2>👁️ Audience Reach Distribution</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for ch in scorecard["channel_name"]:
        vals = df[df["channel_name"] == ch]["view_count"]
        fig.add_trace(go.Box(y=vals, name=ch[:12], marker_color=ch_color_map.get(ch, "#888"),
                             boxmean="sd", line=dict(width=2), boxpoints=False))
    fig.update_layout(title="View Distribution across Network", showlegend=False, height=450, **PLOT_LAYOUT)
    fig.update_yaxes(title="Views (Log Scale)", type="log")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = go.Figure()
    for ch in scorecard["channel_name"]:
        fig.add_trace(go.Bar(
            x=[ch[:12]], y=[scorecard[scorecard["channel_name"]==ch]["avg_views"].values[0]],
            marker_color=ch_color_map.get(ch, "#888"), name=ch[:12],
            text=[f"{scorecard[scorecard['channel_name']==ch]['avg_views'].values[0]/1000:.0f}K"],
            textposition="outside", textfont=dict(color=FG, size=13, weight="bold"),
            marker=dict(line=dict(width=0))
        ))
    fig.update_layout(title="Average Views per Upload", showlegend=False, height=450, **PLOT_LAYOUT)
    fig.update_yaxes(title="Average Views")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ SECTION 3: ENGAGEMENT DYNAMICS ══════════════════════════════
st.markdown('<div class="section-header"><h2>💬 Engagement Dynamics</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for ch_name in scorecard["channel_name"]:
        ch_df = df[df["channel_name"] == ch_name]
        fig.add_trace(go.Scattergl(
            x=ch_df["view_count"], y=ch_df["engagements"],
            mode="markers", name=ch_name[:12],
            marker=dict(color=ch_color_map.get(ch_name, "#888"), size=6, opacity=0.6,
                        line=dict(width=0.5, color="white")),
            hovertemplate="<b>%{text}</b><br>Views: %{x:,}<br>Eng: %{y:,}",
            text=ch_df["title"],
        ))
    fig.update_layout(title="Views vs Total Engagements Map", height=450, **PLOT_LAYOUT)
    fig.update_xaxes(title="Total Views", type="log")
    fig.update_yaxes(title="Engagements (Likes + Comments)", type="log")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    eng_comp = scorecard[["channel_name", "avg_like_rate", "avg_eng_rate"]].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=eng_comp["channel_name"].str[:12], y=eng_comp["avg_like_rate"],
                         name="Like Rate %", marker_color=PRIMARY, marker=dict(line=dict(width=0))))
    fig.add_trace(go.Bar(x=eng_comp["channel_name"].str[:12], y=eng_comp["avg_eng_rate"],
                         name="Engagement Rate %", marker_color=ACCENT_2, marker=dict(line=dict(width=0))))
    fig.update_layout(title="Community Loyalty Metrics", barmode="group", height=450, **PLOT_LAYOUT,
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=BORDER, borderwidth=1))
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ SECTION 4: MOMENTUM TIMELINE ═══════════════════════════════════
st.markdown('<div class="section-header"><h2>📈 Momentum & Growth Timeline</h2></div>', unsafe_allow_html=True)

monthly = df.groupby(["month", "channel_name"]).agg(
    count=("video_id", "count"),
    avg_views=("view_count", "mean"),
    total_views=("view_count", "sum"),
).reset_index().sort_values("month")

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for ch in ch_names:
        ch_m = monthly[monthly["channel_name"] == ch].copy()
        if len(ch_m) > 2:
            ch_m["roll"] = ch_m["avg_views"].rolling(3, min_periods=1).mean()
            fig.add_trace(go.Scatter(x=ch_m["month"], y=ch_m["roll"], mode="lines",
                                     name=ch[:12], line=dict(color=ch_color_map.get(ch, "#888"), width=3)))
    fig.update_layout(title="View Volume Momentum (3M Rolling Avg)", height=450, **PLOT_LAYOUT)
    fig.update_yaxes(title="Avg Views (3M)")
    fig.update_xaxes(tickangle=-45, dtick=3)
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    fig = go.Figure()
    for ch in ch_names:
        ch_m = monthly[monthly["channel_name"] == ch]
        fig.add_trace(go.Bar(x=ch_m["month"], y=ch_m["count"], name=ch[:12],
                             marker_color=ch_color_map.get(ch, "#888"), marker=dict(line=dict(width=0))))
    fig.update_layout(title="Production Velocity (Uploads/Month)", height=450, barmode="stack", **PLOT_LAYOUT)
    fig.update_xaxes(tickangle=-45, dtick=3)
    fig.update_yaxes(title="Videos")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ SECTION 5: FORMAT LAB ════════════════════════════════════════
st.markdown('<div class="section-header"><h2>⏱️ Format & Duration Lab</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    dur_bins = [(0,1,"<1m (Shorts)"), (1,5,"1-5m"), (5,10,"5-10m"), (10,15,"10-15m"), (15,20,"15-20m"), (20,60,"20-60m"), (60,9999,"60m+")]
    dur_data = []
    for ch in ch_names:
        ch_df = df[df["channel_name"] == ch]
        for lo, hi, lbl in dur_bins:
            subset = ch_df[(ch_df["duration_min"] >= lo) & (ch_df["duration_min"] < hi)]
            if len(subset) > 0:
                dur_data.append({"Channel": ch[:12], "Duration": lbl, "Avg Views": subset["view_count"].mean(), "Count": len(subset)})
    dur_df = pd.DataFrame(dur_data)
    if len(dur_df) > 0:
        fig = px.bar(dur_df, x="Duration", y="Avg Views", color="Channel", barmode="group",
                     color_discrete_map={ch[:12]: ch_color_map.get(ch, "#888") for ch in ch_names},
                     title="Average Reach by Content Length")
        fig.update_layout(height=450, **PLOT_LAYOUT)
        fig.update_traces(marker=dict(line=dict(width=0)))
        fig = update_axes(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    avg_dur = df.groupby("channel_name")["duration_min"].mean().sort_values(ascending=False).reset_index()
    fig = go.Figure(go.Bar(
        y=avg_dur["channel_name"].str[:12], x=avg_dur["duration_min"], orientation="h",
        marker_color=[ch_color_map.get(ch, "#888") for ch in avg_dur["channel_name"]],
        text=[f"{v:.1f}m" for v in avg_dur["duration_min"]],
        textposition="outside", textfont=dict(color=FG, weight="bold"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Baseline Video Duration", height=450, **PLOT_LAYOUT)
    fig.update_xaxes(title="Minutes")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ SECTION 6: HIGH IMPACT CONTENT ═══════════════════════════════
st.markdown('<div class="section-header"><h2>🔥 High Impact Content</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### ⭐ Top 15 Across Network (By Views)")
    top15 = df.nlargest(15, "view_count")[["channel_name", "title", "view_count", "like_count", "eng_rate", "upload_date"]].copy()
    top15 = top15.reset_index(drop=True)
    top15.index = top15.index + 1
    top15.columns = ["Channel", "Title", "Views", "Likes", "Eng Rate (%)", "Date"]
    top15["Title"] = top15["Title"].str[:50] + "..."
    st.dataframe(top15, use_container_width=True, height=520)

with col2:
    st.markdown("#### 🏆 Network Top 50 Dominance")
    top50 = df.nlargest(50, "view_count")
    dom = top50["channel_name"].value_counts().reset_index()
    dom.columns = ["Channel", "Videos in Top 50"]
    fig = go.Figure(go.Bar(
        x=dom["Channel"].str[:12], y=dom["Videos in Top 50"],
        marker_color=[ch_color_map.get(ch, "#888") for ch in dom["Channel"]],
        text=dom["Videos in Top 50"], textposition="outside", textfont=dict(color=FG, size=15, weight="bold"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Share of Top 50 Viral Hits", height=480, **PLOT_LAYOUT)
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ SECTION 7: RADAR & CONSISTENCY ═══════════════════════════════
st.markdown('<div class="section-header"><h2>🎯 Multi-Dimensional Radar</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if "TBH Labs" in scorecard["channel_name"].values:
        metrics = ["avg_views", "avg_likes", "avg_comments", "avg_eng_rate", "avg_like_rate"]
        labels = ["Avg Views", "Avg Likes", "Avg Comments", "Eng Rate", "Like Rate"]

        fig = go.Figure()
        for ch in scorecard["channel_name"]:
            vals = []
            for m in metrics:
                max_val = scorecard[m].max()
                vals.append(scorecard[scorecard["channel_name"]==ch][m].values[0] / max_val * 100 if max_val > 0 else 0)
            vals.append(vals[0])  # close the polygon
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=labels + [labels[0]], fill="toself", name=ch[:12],
                line=dict(color=ch_color_map.get(ch, "#888"), width=2),
                opacity=0.5 if ch != "TBH Labs" else 0.8,
            ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0)",
                radialaxis=dict(visible=True, range=[0, 110], gridcolor="#e2e8f0", tickfont=dict(color=TEXT_MUTED)),
                angularaxis=dict(gridcolor="#e2e8f0", tickfont=dict(color=FG, size=13, weight="bold")),
            ),
            title="Relative Channel Strength Radar", height=500, **PLOT_LAYOUT,
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    cv_data = df.groupby("channel_name")["view_count"].agg(["mean", "std"]).reset_index()
    cv_data["cv"] = cv_data["std"] / cv_data["mean"] * 100
    cv_data = cv_data.sort_values("cv")
    fig = go.Figure(go.Bar(
        x=cv_data["channel_name"].str[:12], y=cv_data["cv"],
        marker_color=[ch_color_map.get(ch, "#888") for ch in cv_data["channel_name"]],
        text=[f"{v:.0f}%" for v in cv_data["cv"]],
        textposition="outside", textfont=dict(color=FG, weight="bold"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="Performance Volatility (Lower CV% = More Consistent)", height=500, **PLOT_LAYOUT)
    fig.update_yaxes(title="Coefficient of Variation %")
    fig = update_axes(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ══════════════ FOOTER ═══════════════════════════════════════════════════════
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: {TEXT_MUTED}; font-size: 0.9rem; padding: 2rem;">
    <b>TBH Labs Operating System — Competitor Matrix</b><br>
    Data sourced live via YouTube Data API v3 &nbsp;•&nbsp; Generated February 2026
</div>
""", unsafe_allow_html=True)
