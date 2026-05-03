import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ai_queries import query_all_ais
from analyzer import analyze_responses, calculate_scores, generate_insights
from report import build_report_dataframe, get_score_color

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="AEO Diagnostic",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── FORCE SIDEBAR ALWAYS OPEN ── */
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
    min-width: 250px !important;
    max-width: 250px !important;
    background: #0d0d0d !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.sidebar-logo span { color: #818cf8; }
.sidebar-section {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.28);
    margin: 1rem 0 0.4rem;
}
.step-row { display:flex; align-items:flex-start; gap:12px; margin-bottom:0.8rem; }
.step-num {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.25);
    color: #818cf8;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    width: 26px; height: 26px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-text { color: rgba(255,255,255,0.45); font-size: 0.8rem; line-height: 1.5; padding-top: 3px; }

.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(129,140,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.08) !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.45) !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #ec4899) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 26px rgba(99,102,241,0.45) !important;
}

.hero-wrap {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 60%, #0f0f0f 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content:''; position:absolute; top:-80px; right:-80px;
    width:280px; height:280px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #818cf8;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    margin: 0 0 0.6rem;
}
.hero-title span {
    background: linear-gradient(135deg, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub { color: rgba(255,255,255,0.45); font-size: 0.95rem; max-width: 480px; line-height: 1.6; }
.hero-badges { display:flex; gap:8px; margin-top:1.2rem; flex-wrap:wrap; }
.badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.55);
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.76rem;
}

.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.metric-label { font-size: 0.72rem; color: rgba(255,255,255,0.38); text-transform: uppercase; letter-spacing: 0.06em; }
.score-green { color: #34d399; }
.score-orange { color: #fbbf24; }
.score-red { color: #f87171; }

.section-head {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    margin: 1.8rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-head::after {
    content:''; flex:1; height:1px;
    background: rgba(255,255,255,0.07); margin-left:8px;
}

.insight-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.55;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.07);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    color: rgba(255,255,255,0.4) !important;
    padding: 7px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #818cf8 !important;
}

.ex-pill {
    display:inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    color: rgba(255,255,255,0.5);
    padding: 5px 13px;
    border-radius: 100px;
    font-size: 0.8rem;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">AEO <span>Diagnostic</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Search Query</div>', unsafe_allow_html=True)
    user_query = st.text_input("Query", placeholder="e.g. best protein powder for gym", label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">Your Brand</div>', unsafe_allow_html=True)
    your_brand = st.text_input("Brand", placeholder="e.g. Optimum Nutrition", label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">Competitors (one per line)</div>', unsafe_allow_html=True)
    competitors_input = st.text_area("Competitors", placeholder="MyProtein\nMuscleBlaze\nDymatize", label_visibility="collapsed", height=90)

    run_button = st.button("⚡ Run Diagnostic", type="primary", use_container_width=True)

    if st.session_state.get("has_results"):
        if st.button("🔄 Search Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">How it works</div>', unsafe_allow_html=True)
    for num, text in [
        ("1", "Sends query to GPT, Claude & Gemini"),
        ("2", "Extracts brand mentions"),
        ("3", "Scores & ranks 0–100"),
        ("4", "Surfaces actionable insights"),
    ]:
        st.markdown(f'<div class="step-row"><div class="step-num">{num}</div><div class="step-text">{text}</div></div>', unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">Answer Engine Optimization</div>
    <div class="hero-title">How does your brand<br>rank across <span>AI engines?</span></div>
    <div class="hero-sub">Query GPT-4, Claude & Gemini simultaneously. Get a real-time report card on your AI visibility vs competitors.</div>
    <div class="hero-badges">
        <span class="badge">🤖 GPT-4o-mini</span>
        <span class="badge">🟣 Claude Haiku</span>
        <span class="badge">💎 Gemini Flash</span>
        <span class="badge">📊 Live Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── RUN HANDLER ──────────────────────────────────────
if run_button:
    if not user_query or not your_brand:
        st.error("⚠️ Please enter both a search query and your brand name in the sidebar.")
    else:
        competitors = [
            c.strip() for c in competitors_input.split('\n')
            if c.strip() and c.strip().lower() != your_brand.lower()
        ][:5]

        with st.spinner("🤖 Querying GPT, Claude & Gemini... ~15 seconds"):
            ai_responses = query_all_ais(user_query)

        analysis = analyze_responses(ai_responses, your_brand, competitors)
        scores   = calculate_scores(analysis, ai_responses)
        insights = generate_insights(analysis, scores, your_brand, ai_responses)

        st.session_state["has_results"]  = True
        st.session_state["ai_responses"] = ai_responses
        st.session_state["analysis"]     = analysis
        st.session_state["scores"]       = scores
        st.session_state["insights"]     = insights
        st.session_state["saved_query"]  = user_query
        st.session_state["saved_brand"]  = your_brand
        st.rerun()

# ── RESULTS ──────────────────────────────────────────
if st.session_state.get("has_results"):
    ai_responses = st.session_state["ai_responses"]
    analysis     = st.session_state["analysis"]
    scores       = st.session_state["scores"]
    insights     = st.session_state["insights"]
    saved_query  = st.session_state["saved_query"]
    saved_brand  = st.session_state["saved_brand"]
    ai_names     = list(ai_responses.keys())

    st.success(f"✅ Results for **\"{saved_query}\"** — Your brand: **{saved_brand}**")

    your_score      = scores.get(saved_brand, 0)
    color_class     = "score-green" if your_score >= 70 else "score-orange" if your_score >= 40 else "score-red"
    mentioned_count = len(analysis.get(saved_brand, {}).get("mentioned_by", []))
    rank            = sorted(scores.values(), reverse=True).index(your_score) + 1
    total_brands    = len(scores)
    comp_dict       = {b: s for b, s in scores.items() if b != saved_brand}
    top_comp        = max(comp_dict, key=comp_dict.get) if comp_dict else "N/A"
    top_score       = comp_dict.get(top_comp, 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-number {color_class}">{your_score}</div><div class="metric-label">AEO Score / 100</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-number" style="color:#818cf8">#{rank}</div><div class="metric-label">Rank of {total_brands}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-number" style="color:#38bdf8">{mentioned_count}/{len(ai_names)}</div><div class="metric-label">AIs mention you</div></div>', unsafe_allow_html=True)
    with c4:
        tc_display = top_comp[:12] + "..." if len(top_comp) > 12 else top_comp
        st.markdown(f'<div class="metric-card"><div class="metric-number score-red" style="font-size:1.3rem;padding-top:0.5rem">{tc_display}</div><div class="metric-label">Top competitor ({top_score}/100)</div></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-head">📋 Report Card</div>', unsafe_allow_html=True)
        df = build_report_dataframe(analysis, scores, ai_names)
        st.dataframe(df, use_container_width=True, height=260)

    with col_right:
        st.markdown('<div class="section-head">📊 Score Comparison</div>', unsafe_allow_html=True)
        bar_colors = [
            "#818cf8" if b == saved_brand else
            "#34d399" if scores.get(b, 0) >= 70 else
            "#fbbf24" if scores.get(b, 0) >= 40 else "#f87171"
            for b in df["Brand"]
        ]
        fig = go.Figure(go.Bar(
            x=df["Brand"], y=df["Score"],
            marker_color=bar_colors,
            text=df["Score"], textposition="outside",
            textfont=dict(color="white", size=12)
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.5)", family="DM Sans"),
            yaxis=dict(range=[0, 115], gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=260, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-head">💡 Actionable Insights</div>', unsafe_allow_html=True)
    for insight in insights:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-head">🤖 Raw AI Responses</div>', unsafe_allow_html=True)
    tabs = st.tabs([f"  {name}  " for name in ai_names])
    for tab, (ai_name, response) in zip(tabs, ai_responses.items()):
        with tab:
            st.markdown(response)
            snippets = analysis.get(saved_brand, {}).get("snippets", {})
            if ai_name in snippets:
                st.info(f"📍 **{saved_brand}** found here: {snippets[ai_name]}")

# ── EMPTY STATE ──────────────────────────────────────
else:
    st.markdown('<div class="section-head">✨ Example Queries</div>', unsafe_allow_html=True)
    pills = "".join([
        f'<span class="ex-pill">"{e}"</span>'
        for e in [
            "best protein powder for muscle gain",
            "affordable yoga mat for beginners",
            "wireless earbuds under 2000 rupees",
            "best CRM for small business",
            "top magnesium supplement for seniors",
        ]
    ])
    st.markdown(f'<div style="margin-bottom:1.5rem">{pills}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(99,102,241,0.06);
        border: 1px dashed rgba(99,102,241,0.22);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
    ">
        <div style="font-size:2.2rem;margin-bottom:0.8rem">🎯</div>
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:rgba(255,255,255,0.65);margin-bottom:0.4rem">
            Ready to check your AI visibility?
        </div>
        <div style="color:rgba(255,255,255,0.3);font-size:0.84rem">
            Fill in the sidebar → click Run Diagnostic → get your report in ~15 seconds
        </div>
    </div>
    """, unsafe_allow_html=True)