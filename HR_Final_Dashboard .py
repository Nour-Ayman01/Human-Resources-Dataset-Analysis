import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HR Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --red:     #e63946;
    --green:   #2dc653;
    --bg:      #f4f6f9;
    --card:    #ffffff;
    --border:  #e8ecf1;
    --text:    #1a1d23;
    --muted:   #7c8797;
    --accent:  #1f4e79;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--accent) !important;
    padding-top: 10px;
}
section[data-testid="stSidebar"] * { color: #ffffff !important; }
section[data-testid="stSidebar"] .stSelectbox > label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6) !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    text-align: center;
    padding: 20px 10px 30px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 20px;
}
.sidebar-logo .icon { font-size: 2.8rem; margin-bottom: 6px; }
.sidebar-logo h2 {
    font-size: 1rem; font-weight: 800;
    color: #fff; margin: 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.sidebar-logo p {
    font-size: 11px; color: rgba(255,255,255,0.5);
    margin: 2px 0 0; letter-spacing: 2px;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    gap: 16px;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--border);
}
.page-header h1 {
    font-size: 2rem; font-weight: 800;
    color: var(--accent); margin: 0; line-height: 1;
}
.page-header .badge {
    background: var(--accent);
    color: #fff;
    font-size: 10px; font-weight: 700;
    letter-spacing: 1.5px;
    padding: 4px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-bottom: 3px;
}

/* ── KPI card ── */
.kpi-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 18px 18px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    transition: box-shadow .2s, transform .2s;
}
.kpi-wrap:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.10); transform: translateY(-2px); }
.kpi-strip {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 16px 16px 0 0;
}
.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
    display: block;
}
.kpi-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    color: var(--text);
}
.kpi-sub {
    font-size: 11px;
    color: var(--muted);
    margin-top: 6px;
}

/* ── Section title ── */
.section-title {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 32px 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Chart card ── */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 6px 6px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 16px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 30px 0 10px;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1.5px;
}

/* hide default streamlit metric */
[data-testid="metric-container"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("HR_Analytics.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="icon">👥</div>
    <h2>HR Analytics</h2>
    <p>PEOPLE INTELLIGENCE</p>
</div>
""", unsafe_allow_html=True)

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique().tolist()),
)
joblevel = st.sidebar.selectbox(
    "Job Level",
    ["All"] + sorted(df["JobLevel"].unique().tolist()),
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='font-size:10px;color:rgba(255,255,255,0.35);text-align:center;letter-spacing:1px;'>HR DASHBOARD v2.0</p>",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════
#  FILTER
# ══════════════════════════════════════════════════════════════════════
filtered = df.copy()
if department != "All":
    filtered = filtered[filtered["Department"] == department]
if joblevel != "All":
    filtered = filtered[filtered["JobLevel"] == joblevel]

# ══════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <div>
        <div class="badge">Live Report</div>
        <h1>Employee Attrition Dashboard</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  KPI CALCULATIONS
# ══════════════════════════════════════════════════════════════════════
total      = len(filtered)
att_yes    = filtered[filtered["Attrition"] == "Yes"].shape[0]
att_no     = total - att_yes
att_rate   = round((att_yes / total) * 100, 1) if total > 0 else 0
avg_inc    = filtered["MonthlyIncome"].mean() if total > 0 else 0
avg_years  = filtered["YearsAtCompany"].mean() if total > 0 else 0
avg_age    = filtered["Age"].mean() if total > 0 else 0

# ── KPI Row ─────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

kpi_data = [
    (c1, "👥", "Total Employees", f"{total:,}", "في الفلتر الحالي", "linear-gradient(135deg,#1f4e79,#2874a6)"),
    (c2, "🔴", "Attrition Count", f"{att_yes:,}", f"من أصل {total:,} موظف", "linear-gradient(135deg,#e63946,#c0392b)"),
    (c3, "📊", "Attrition Rate", f"{att_rate}%", "نسبة ترك العمل", "linear-gradient(135deg,#e63946,#e67e22)" if att_rate > 15 else "linear-gradient(135deg,#2dc653,#27ae60)"),
    (c4, "💰", "Avg Monthly Income", f"${avg_inc:,.0f}", "متوسط الراتب الشهري", "linear-gradient(135deg,#2dc653,#1e8449)"),
    (c5, "🗓️", "Avg Years at Co.", f"{avg_years:.1f} yrs", "متوسط سنوات الخبرة", "linear-gradient(135deg,#8e44ad,#6c3483)"),
]

for col, icon, label, value, sub, gradient in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-strip" style="background:{gradient};"></div>
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  CHART COLORS & LAYOUT
# ══════════════════════════════════════════════════════════════════════
COLOR_MAP = {"Yes": "#e63946", "No": "#2dc653"}

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#5a6275", size=12),
    title_font=dict(family="Plus Jakarta Sans, sans-serif", size=14, color="#1a1d23"),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
        font=dict(size=11),
    ),
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis=dict(showgrid=False, linecolor="#e8ecf1", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#f0f2f5", linecolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
)

# ══════════════════════════════════════════════════════════════════════
#  SECTION 1 – ATTRITION OVERVIEW
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📌 Attrition Overview</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1, 1])

# ── PIE CHART – Attrition Distribution ──────────────────────────────
with col1:
    pie_df = filtered["Attrition"].value_counts().reset_index()
    pie_df.columns = ["Attrition", "Count"]

    fig_pie = go.Figure(go.Pie(
        labels=pie_df["Attrition"],
        values=pie_df["Count"],
        hole=0.62,
        marker=dict(
            colors=[COLOR_MAP.get(a, "#999") for a in pie_df["Attrition"]],
            line=dict(color="#ffffff", width=3),
        ),
        textinfo="percent+label",
        textfont=dict(size=13, family="Plus Jakarta Sans"),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"<b>{att_rate}%</b><br><span style='font-size:11px'>Attrition</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#1a1d23", family="Plus Jakarta Sans"),
        align="center",
    )
    fig_pie.update_layout(
        **{k: v for k, v in BASE_LAYOUT.items() if k not in ("xaxis", "yaxis")},
        title="Attrition Distribution",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        height=320,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── BAR – Attrition by Department ────────────────────────────────────
with col2:
    dept_df = (
        df.groupby(["Department", "Attrition"])
        .size()
        .reset_index(name="Count")
    )
    fig1 = px.bar(
        dept_df,
        x="Department",
        y="Count",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        barmode="group",
        title="Attrition by Department",
        text="Count",
    )
    fig1.update_traces(textposition="outside", textfont_size=10, marker_line_width=0, width=0.35)
    fig1.update_layout(**BASE_LAYOUT, height=320, bargap=0.3)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── BAR – Attrition by Job Level ─────────────────────────────────────
with col3:
    jl_df = (
        df.groupby(["JobLevel", "Attrition"])
        .size()
        .reset_index(name="Count")
    )
    fig2 = px.bar(
        jl_df,
        x="JobLevel",
        y="Count",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        barmode="group",
        title="Attrition by Job Level",
        text="Count",
    )
    fig2.update_traces(textposition="outside", textfont_size=10, marker_line_width=0, width=0.35)
    fig2.update_layout(**BASE_LAYOUT, height=320, bargap=0.3)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  SECTION 2 – INCOME & TENURE
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">💼 Income & Tenure Analysis</div>', unsafe_allow_html=True)

col4, col5 = st.columns(2)

# ── BOX – Monthly Income by Attrition ────────────────────────────────
with col4:
    fig3 = px.box(
        filtered,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        title="Monthly Income Distribution by Attrition",
        points="outliers",
    )
    fig3.update_traces(
        marker=dict(opacity=0.4, size=4),
        line=dict(width=2),
    )
    fig3.update_layout(**BASE_LAYOUT, height=330)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── BOX – Years at Company by Attrition ──────────────────────────────
with col5:
    fig4 = px.box(
        filtered,
        x="Attrition",
        y="YearsAtCompany",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        title="Years at Company by Attrition",
        points="outliers",
    )
    fig4.update_traces(
        marker=dict(opacity=0.4, size=4),
        line=dict(width=2),
    )
    fig4.update_layout(**BASE_LAYOUT, height=330)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  SECTION 3 – OVERTIME & AGE
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⏱️ Overtime & Age Breakdown</div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)

# ── BAR – Overtime vs Attrition ──────────────────────────────────────
with col6:
    ot_df = (
        df.groupby(["OverTime", "Attrition"])
        .size()
        .reset_index(name="Count")
    )
    fig5 = px.bar(
        ot_df,
        x="OverTime",
        y="Count",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        barmode="group",
        title="Overtime vs Attrition",
        text="Count",
    )
    fig5.update_traces(textposition="outside", textfont_size=11, marker_line_width=0, width=0.35)
    fig5.update_layout(**BASE_LAYOUT, height=330, bargap=0.3)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── HISTOGRAM – Age Distribution by Attrition ────────────────────────
with col7:
    fig6 = px.histogram(
        df,
        x="Age",
        color="Attrition",
        color_discrete_map=COLOR_MAP,
        barmode="overlay",
        opacity=0.75,
        nbins=20,
        title="Age Distribution by Attrition",
    )
    fig6.update_layout(**BASE_LAYOUT, height=330, bargap=0.05)
    fig6.update_traces(marker_line_width=0)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    HR ANALYTICS DASHBOARD · BUILT WITH STREAMLIT & PLOTLY · 2026
</div>
""", unsafe_allow_html=True)
