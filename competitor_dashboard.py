"""
Competitor Analysis — Myanmar Tech YouTube Landscape
=====================================================
Run: streamlit run competitor_dashboard.py --server.port 8503
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Competitor Analysis — TBH Labs",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Flash UI Palette ─────────────────────────────────────────────────────────
BG        = "#f8fafc"
CARD_BG   = "#ffffff"
FG        = "#0f172a"
TEXT_MUTED= "#64748b"
BORDER    = "#e2e8f0"
PRIMARY   = "#3b82f6"
ACCENT_1  = "#8b5cf6"
ACCENT_2  = "#ec4899"
ACCENT_3  = "#10b981"
ACCENT_4  = "#f59e0b"
ACCENT_5  = "#06b6d4"

CH_COLORS = {
    "TBH Labs": PRIMARY,
    "Myanmar Mobile Phones & Tech Review": ACCENT_4,
    "MyTech Myanmar": ACCENT_3,
    "ZEST": ACCENT_1,
    "Technity": ACCENT_2,
    "T4U2": ACCENT_5,
}

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {BG}; }}
    .main .block-container {{ padding-top: 2.5rem; max-width: 1400px; }}
    h1,h2,h3,h4,h5,h6 {{ color: {FG} !important; font-weight: 800 !important; letter-spacing: -0.025em; }}
    p, span, div {{ color: {FG}; }}
    section[data-testid="stSidebar"] {{ background-color: {CARD_BG}; border-right: 1px solid {BORDER}; }}

    .dashboard-header {{
        background: {CARD_BG}; padding: 3rem 2.5rem; border-radius: 24px;
        margin-bottom: 2rem; position: relative; overflow: hidden;
        border: 1px solid {BORDER};
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05);
    }}
    .dashboard-header::before {{
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
        background: linear-gradient(90deg, {ACCENT_5}, {PRIMARY}, {ACCENT_1}, {ACCENT_2});
    }}
    .dashboard-header h1 {{
        font-size: 3rem !important; font-weight: 900 !important; margin: 0 0 0.5rem 0;
        background: linear-gradient(to right, {FG}, #334155);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .dashboard-header p {{ color: {TEXT_MUTED}; font-size: 1.1rem; margin: 0; font-weight: 500; }}

    .insight-box {{
        background: rgba(59,130,246,0.05); border-left: 4px solid {PRIMARY};
        border-radius: 0 12px 12px 0; padding: 1.25rem 1.5rem;
        margin: 1rem 0 2rem 0; font-size: 0.95rem; line-height: 1.6; font-weight: 500; color: #334155;
    }}
    .insight-box strong {{ color: {FG}; font-weight: 700; }}

    .rank-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; background: {CARD_BG};
        border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
    .rank-table th {{ background: #f1f5f9; color: {TEXT_MUTED}; padding: 1rem; text-align: left;
        font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.75rem;
        border-bottom: 1px solid {BORDER}; }}
    .rank-table td {{ padding: 1rem; border-bottom: 1px solid {BORDER}; color: {FG}; font-weight: 500; }}
    .rank-table tr:hover {{ background: #f8fafc; }}
    .rank-highlight {{ background: rgba(59,130,246,0.05) !important; }}

    .stPlotlyChart {{ background: {CARD_BG}; border: 1px solid {BORDER}; border-radius: 16px;
        padding: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }}
    [data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 12px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Load & Pre-aggregate Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Competitor_Videos.csv")
    df["upload_date"] = pd.to_datetime(df["upload_date"])
    df["year"] = df["upload_date"].dt.year
    df["month"] = df["upload_date"].dt.to_period("M").astype(str)
    df["duration_min"] = df["duration_seconds"] / 60
    df["engagements"] = df["like_count"] + df["comment_count"]
    df["eng_rate"] = np.where(df["view_count"] > 0,
                              df["engagements"] / df["view_count"] * 100, 0)
    df["like_rate"] = np.where(df["view_count"] > 0,
                               df["like_count"] / df["view_count"] * 100, 0)
    return df

df_all = load_data()
ch_names = list(CH_COLORS.keys())

# ── Plot helpers ─────────────────────────────────────────────────────────────
PL = dict(
    template="plotly_white",
    paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color=TEXT_MUTED, size=13),
    margin=dict(l=40, r=20, t=55, b=40),
    hoverlabel=dict(bgcolor=CARD_BG, font_size=13, font_family="Inter",
                    bordercolor=BORDER, font_color=FG),
    title_font=dict(size=16, color=FG, family="Inter", weight="bold"),
)
def fax(fig):
    fig.update_xaxes(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0",
                     tickfont=dict(color=TEXT_MUTED))
    fig.update_yaxes(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0",
                     tickfont=dict(color=TEXT_MUTED))
    return fig

def fmt(v):
    if v >= 1_000_000: return f"{v/1e6:.1f}M"
    if v >= 1_000: return f"{v/1e3:.1f}K"
    return f"{int(v)}"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    years = sorted(df_all["year"].unique())
    sel_years = st.multiselect("Timeline", years, default=[y for y in years if y >= 2021])
    sel_channels = st.multiselect("Channels", ch_names, default=ch_names)
    min_views = st.slider("Min Views", 0, 50000, 0, step=1000)

df = df_all[
    (df_all["year"].isin(sel_years)) &
    (df_all["channel_name"].isin(sel_channels)) &
    (df_all["view_count"] >= min_views)
].copy()

# Pre-compute scorecard (used in multiple tabs)
@st.cache_data
def compute_scorecard(_df):
    sc = _df.groupby("channel_name").agg(
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
    return sc.sort_values("avg_views", ascending=False)

scorecard = compute_scorecard(df)

# ══════════════ HEADER ═══════════════════════════════════════════════════════
st.markdown(f"""
<div class="dashboard-header">
    <h1>⚡ Competitor Intelligence</h1>
    <p>Myanmar Tech YouTube &nbsp;|&nbsp; <b>{len(df):,}</b> Videos &nbsp;|&nbsp; <b>{len(sel_channels)}</b> Channels</p>
</div>
""", unsafe_allow_html=True)

# ══════════════ TAB LAYOUT (renders only the active tab) ═════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Scorecard", "👁️ Views", "💬 Engagement",
    "📈 Growth", "⏱️ Duration", "🔥 Top Videos"
])

# ── TAB 1: SCORECARD ─────────────────────────────────────────────────────────
with tab1:
    rows_html = ""
    for _, r in scorecard.iterrows():
        color = CH_COLORS.get(r["channel_name"], "#888")
        hl = ' class="rank-highlight"' if r["channel_name"] == "TBH Labs" else ""
        rows_html += f"""<tr{hl}>
            <td><span style="color:{color};font-weight:900;font-size:1.2em;">•</span> {r['channel_name']}</td>
            <td>{r['videos']}</td><td>{fmt(r['total_views'])}</td>
            <td><b>{fmt(r['avg_views'])}</b></td><td>{fmt(r['med_views'])}</td>
            <td>{fmt(r['total_likes'])}</td><td>{r['avg_eng_rate']:.2f}%</td>
            <td>{r['avg_like_rate']:.2f}%</td><td>{r['avg_duration']:.1f}m</td>
        </tr>"""

    st.markdown(f"""
    <table class="rank-table">
    <tr><th>Channel</th><th>Videos</th><th>Total Views</th><th>Avg Views</th><th>Med Views</th>
    <th>Total Likes</th><th>Eng Rate</th><th>Like Rate</th><th>Avg Dur</th></tr>
    {rows_html}</table>
    """, unsafe_allow_html=True)

    if "TBH Labs" in scorecard["channel_name"].values:
        tbh = scorecard[scorecard["channel_name"] == "TBH Labs"].iloc[0]
        tbh_rank = list(scorecard["channel_name"]).index("TBH Labs") + 1
        leader = scorecard.iloc[0]
        st.markdown(f"""
        <div class="insight-box">
            <strong>🎯 Market Position:</strong> TBH Labs ranks <strong>#{tbh_rank}</strong> of {len(scorecard)} channels
            by avg views ({fmt(tbh['avg_views'])}). Leader: <strong>{leader['channel_name']}</strong> ({fmt(leader['avg_views'])}).
            TBH Like Rate: <strong>{tbh['avg_like_rate']:.2f}%</strong> · Engagement Rate: <strong>{tbh['avg_eng_rate']:.2f}%</strong>
        </div>
        """, unsafe_allow_html=True)

    # Radar chart
    metrics = ["avg_views", "avg_likes", "avg_comments", "avg_eng_rate", "avg_like_rate"]
    labels = ["Avg Views", "Avg Likes", "Avg Comments", "Eng Rate", "Like Rate"]
    fig = go.Figure()
    for ch in scorecard["channel_name"]:
        vals = []
        for m in metrics:
            mx = scorecard[m].max()
            vals.append(scorecard[scorecard["channel_name"]==ch][m].values[0] / mx * 100 if mx > 0 else 0)
        vals.append(vals[0])
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels + [labels[0]], fill="toself", name=ch[:15],
            line=dict(color=CH_COLORS.get(ch, "#888"), width=2),
            opacity=0.8 if ch == "TBH Labs" else 0.4,
        ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(255,255,255,0)",
                   radialaxis=dict(visible=True, range=[0,110], gridcolor="#e2e8f0",
                                   tickfont=dict(color=TEXT_MUTED)),
                   angularaxis=dict(gridcolor="#e2e8f0", tickfont=dict(color=FG, size=12))),
        title="Competitive Radar", height=480, **PL)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ── TAB 2: VIEWS ─────────────────────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        for ch in scorecard["channel_name"]:
            v = df[df["channel_name"] == ch]["view_count"]
            fig.add_trace(go.Box(y=v, name=ch[:12],
                                 marker_color=CH_COLORS.get(ch, "#888"),
                                 boxmean="sd", line=dict(width=2), boxpoints=False))
        fig.update_layout(title="View Distribution", showlegend=False, height=450, **PL)
        fig.update_yaxes(title="Views (Log)", type="log")
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:
        fig = go.Figure(go.Bar(
            x=scorecard["channel_name"].str[:12],
            y=scorecard["avg_views"],
            marker_color=[CH_COLORS.get(ch, "#888") for ch in scorecard["channel_name"]],
            text=[fmt(v) for v in scorecard["avg_views"]],
            textposition="outside", textfont=dict(color=FG, size=13, weight="bold"),
            marker=dict(line=dict(width=0))
        ))
        fig.update_layout(title="Avg Views per Upload", showlegend=False, height=450, **PL)
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    # Hit rate
    st.markdown("#### 🎯 Hit Rate Analysis")
    hit_data = []
    for ch in scorecard["channel_name"]:
        ch_df = df[df["channel_name"] == ch]
        total = len(ch_df)
        if total > 0:
            for t, lbl in [(10000, ">10K"), (50000, ">50K"), (100000, ">100K")]:
                hit_data.append({"Channel": ch[:12], "Threshold": lbl,
                                 "Hit Rate": len(ch_df[ch_df["view_count"] > t]) / total * 100})
    hit_df = pd.DataFrame(hit_data)
    fig = px.bar(hit_df, x="Channel", y="Hit Rate", color="Threshold", barmode="group",
                 title="% of Videos Exceeding View Thresholds",
                 color_discrete_sequence=[PRIMARY, ACCENT_4, "#ef4444"])
    fig.update_layout(height=400, **PL)
    fig.update_traces(marker=dict(line=dict(width=0)))
    fax(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ── TAB 3: ENGAGEMENT ────────────────────────────────────────────────────────
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        eng_comp = scorecard[["channel_name", "avg_like_rate", "avg_eng_rate"]].copy()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=eng_comp["channel_name"].str[:12], y=eng_comp["avg_like_rate"],
                             name="Like Rate %", marker_color=PRIMARY,
                             marker=dict(line=dict(width=0))))
        fig.add_trace(go.Bar(x=eng_comp["channel_name"].str[:12], y=eng_comp["avg_eng_rate"],
                             name="Eng Rate %", marker_color=ACCENT_2,
                             marker=dict(line=dict(width=0))))
        fig.update_layout(title="Community Loyalty Metrics", barmode="group", height=420, **PL,
                          legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)",
                                      bordercolor=BORDER, borderwidth=1))
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:
        # avg likes and comments per channel
        fig = go.Figure()
        fig.add_trace(go.Bar(x=scorecard["channel_name"].str[:12], y=scorecard["avg_likes"],
                             name="Avg Likes", marker_color=ACCENT_3,
                             marker=dict(line=dict(width=0))))
        fig.add_trace(go.Bar(x=scorecard["channel_name"].str[:12], y=scorecard["avg_comments"],
                             name="Avg Comments", marker_color=ACCENT_5,
                             marker=dict(line=dict(width=0))))
        fig.update_layout(title="Avg Likes & Comments per Video", barmode="group", height=420, **PL)
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    # Consistency
    st.markdown("#### 📏 Performance Consistency")
    cv_data = df.groupby("channel_name")["view_count"].agg(["mean", "std"]).reset_index()
    cv_data["cv"] = cv_data["std"] / cv_data["mean"] * 100
    cv_data = cv_data.sort_values("cv")
    fig = go.Figure(go.Bar(
        x=cv_data["channel_name"].str[:12], y=cv_data["cv"],
        marker_color=[CH_COLORS.get(ch, "#888") for ch in cv_data["channel_name"]],
        text=[f"{v:.0f}%" for v in cv_data["cv"]],
        textposition="outside", textfont=dict(color=FG, weight="bold"),
        marker=dict(line=dict(width=0))
    ))
    fig.update_layout(title="View Volatility (Lower = More Consistent)", height=380, **PL)
    fig.update_yaxes(title="Coefficient of Variation %")
    fax(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)


# ── TAB 4: GROWTH ────────────────────────────────────────────────────────────
with tab4:
    monthly = df.groupby(["month", "channel_name"]).agg(
        count=("video_id", "count"),
        avg_views=("view_count", "mean"),
    ).reset_index().sort_values("month")

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        for ch in ch_names:
            ch_m = monthly[monthly["channel_name"] == ch].copy()
            if len(ch_m) > 2:
                ch_m["roll"] = ch_m["avg_views"].rolling(3, min_periods=1).mean()
                fig.add_trace(go.Scatter(x=ch_m["month"], y=ch_m["roll"], mode="lines",
                                         name=ch[:15], line=dict(color=CH_COLORS.get(ch, "#888"), width=3)))
        fig.update_layout(title="View Momentum (3M Rolling)", height=450, **PL)
        fig.update_xaxes(tickangle=-45, dtick=6)
        fig.update_yaxes(title="Avg Views")
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:
        fig = go.Figure()
        for ch in ch_names:
            ch_m = monthly[monthly["channel_name"] == ch]
            fig.add_trace(go.Bar(x=ch_m["month"], y=ch_m["count"], name=ch[:15],
                                 marker_color=CH_COLORS.get(ch, "#888"),
                                 marker=dict(line=dict(width=0))))
        fig.update_layout(title="Upload Frequency", height=450, barmode="stack", **PL)
        fig.update_xaxes(tickangle=-45, dtick=6)
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    # Year-over-year
    st.markdown("#### 📅 Year-Over-Year")
    yearly = df.groupby(["year", "channel_name"]).agg(
        count=("video_id", "count"),
        avg_views=("view_count", "mean"),
    ).reset_index()
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(yearly, x="year", y="avg_views", color="channel_name", barmode="group",
                     color_discrete_map=CH_COLORS, title="Avg Views per Year")
        fig.update_layout(height=380, **PL)
        fig.update_xaxes(dtick=1)
        fig.update_traces(marker=dict(line=dict(width=0)))
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    with col2:
        fig = px.bar(yearly, x="year", y="count", color="channel_name", barmode="group",
                     color_discrete_map=CH_COLORS, title="Videos Published per Year")
        fig.update_layout(height=380, **PL)
        fig.update_xaxes(dtick=1)
        fig.update_traces(marker=dict(line=dict(width=0)))
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)


# ── TAB 5: DURATION ──────────────────────────────────────────────────────────
with tab5:
    col1, col2 = st.columns(2)
    with col1:
        dur_bins = [(0,1,"<1m"), (1,5,"1-5m"), (5,10,"5-10m"), (10,15,"10-15m"),
                    (15,20,"15-20m"), (20,60,"20-60m"), (60,9999,"60m+")]
        dur_data = []
        for ch in ch_names:
            ch_df = df[df["channel_name"] == ch]
            for lo, hi, lbl in dur_bins:
                subset = ch_df[(ch_df["duration_min"] >= lo) & (ch_df["duration_min"] < hi)]
                if len(subset) > 0:
                    dur_data.append({"Channel": ch[:12], "Duration": lbl,
                                     "Avg Views": subset["view_count"].mean()})
        if dur_data:
            dur_df = pd.DataFrame(dur_data)
            fig = px.bar(dur_df, x="Duration", y="Avg Views", color="Channel", barmode="group",
                         color_discrete_map={ch[:12]: CH_COLORS.get(ch, "#888") for ch in ch_names},
                         title="Avg Views by Duration")
            fig.update_layout(height=450, **PL)
            fig.update_traces(marker=dict(line=dict(width=0)))
            fax(fig)
            st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:
        avg_dur = df.groupby("channel_name")["duration_min"].mean().sort_values(ascending=False).reset_index()
        fig = go.Figure(go.Bar(
            y=avg_dur["channel_name"].str[:12], x=avg_dur["duration_min"], orientation="h",
            marker_color=[CH_COLORS.get(ch, "#888") for ch in avg_dur["channel_name"]],
            text=[f"{v:.1f}m" for v in avg_dur["duration_min"]],
            textposition="outside", textfont=dict(color=FG, weight="bold"),
            marker=dict(line=dict(width=0))
        ))
        fig.update_layout(title="Avg Video Duration", height=450, **PL)
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)


# ── TAB 6: TOP VIDEOS ────────────────────────────────────────────────────────
with tab6:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ⭐ Top 15 by Views")
        top15 = df.nlargest(15, "view_count")[
            ["channel_name", "title", "view_count", "like_count", "comment_count", "upload_date"]
        ].reset_index(drop=True)
        top15.index += 1
        top15.columns = ["Channel", "Title", "Views", "Likes", "Comments", "Date"]
        top15["Title"] = top15["Title"].str[:50]
        st.dataframe(top15, use_container_width=True, height=520)

    with col2:
        st.markdown("#### 🏆 Top 50 Dominance")
        top50 = df.nlargest(50, "view_count")
        dom = top50["channel_name"].value_counts().reset_index()
        dom.columns = ["Channel", "Count"]
        fig = go.Figure(go.Bar(
            x=dom["Channel"].str[:12], y=dom["Count"],
            marker_color=[CH_COLORS.get(ch, "#888") for ch in dom["Channel"]],
            text=dom["Count"], textposition="outside",
            textfont=dict(color=FG, size=15, weight="bold"),
            marker=dict(line=dict(width=0))
        ))
        fig.update_layout(title="Share of Top 50 Viral Hits", height=480, **PL)
        fax(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    st.markdown("#### ⭐ Top 15 by Engagement")
    top_eng = df.nlargest(15, "engagements")[
        ["channel_name", "title", "engagements", "view_count", "eng_rate", "upload_date"]
    ].reset_index(drop=True)
    top_eng.index += 1
    top_eng.columns = ["Channel", "Title", "Engagements", "Views", "Eng%", "Date"]
    top_eng["Title"] = top_eng["Title"].str[:55]
    st.dataframe(top_eng, use_container_width=True, height=520)


# ══════════════ FOOTER ═══════════════════════════════════════════════════════
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: {TEXT_MUTED}; font-size: 0.85rem; padding: 2rem;">
    <b>TBH Labs Operating System — Competitor Matrix</b><br>
    Data via YouTube Data API v3 &nbsp;•&nbsp; February 2026
</div>
""", unsafe_allow_html=True)
