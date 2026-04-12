"""
FoodWise AI 2026 — Python / Streamlit Edition
All four features:
  1. Eco-Score Gamification + CO₂ savings
  2. Smart Pantry Expiry Manager
  3. Multimodal HCI (Voice & Barcode stubs)
  4. Community Food-Sharing P2P Map (Folium)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime, timedelta, date
import math
import json

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="FoodWise AI 2026",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b1210;
    color: #e8f0ec;
}
[data-testid="stSidebar"] {
    background-color: #0f1a14;
    border-right: 1px solid #2a3d32;
}
[data-testid="stSidebar"] * { color: #e8f0ec !important; }

/* ── Cards ── */
.fw-card {
    background: #131d18;
    border: 1px solid #2a3d32;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 18px;
}
.fw-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #e8f0ec;
    margin-bottom: 16px;
    letter-spacing: 0.2px;
}

/* ── Stat tiles ── */
.stat-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }
.stat-tile {
    flex: 1 1 120px;
    background: #1a2820;
    border: 1px solid #2a3d32;
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
}
.stat-val  { font-size: 24px; font-weight: 600; color: #4ade80; }
.stat-val-red  { font-size: 24px; font-weight: 600; color: #f87171; }
.stat-val-white{ font-size: 24px; font-weight: 600; color: #e8f0ec; }
.stat-lbl  { font-size: 11px; color: #7a9a87; margin-top: 4px; }

/* ── Tags ── */
.tag-urgent { background:#3d1515; color:#f87171; padding:3px 10px;
              border-radius:20px; font-size:11px; font-weight:600; }
.tag-soon   { background:#3d2e00; color:#fbbf24; padding:3px 10px;
              border-radius:20px; font-size:11px; font-weight:600; }
.tag-fresh  { background:#1a3d28; color:#4ade80; padding:3px 10px;
              border-radius:20px; font-size:11px; font-weight:600; }

/* ── Pantry rows ── */
.pantry-row {
    display:flex; justify-content:space-between; align-items:center;
    background:#1a2820; border-radius:10px;
    padding:10px 14px; margin-bottom:8px;
}
.pantry-name  { font-weight:600; font-size:14px; }
.pantry-date  { font-size:12px; color:#7a9a87; margin-top:2px; }

/* ── HCI buttons row ── */
.hci-row { display:flex; gap:10px; margin-bottom:14px; }
.hci-btn {
    display:inline-flex; align-items:center; gap:6px;
    padding:9px 16px;
    background:transparent;
    border:1px solid #2a3d32;
    color:#7a9a87; border-radius:10px;
    font-size:13px; cursor:pointer;
    transition: all 0.15s;
}
.hci-btn-active {
    border-color:#4ade80 !important;
    color:#4ade80 !important;
}

/* ── NGO cards ── */
.ngo-row {
    display:flex; justify-content:space-between; align-items:center;
    background:#1a2820; border-radius:10px;
    padding:12px 16px; margin-bottom:8px;
}
.ngo-name { font-weight:600; font-size:14px; }
.ngo-sub  { font-size:12px; color:#7a9a87; margin-top:2px; }

/* ── Sidebar nav ── */
.sidebar-logo {
    font-size:20px; font-weight:700;
    color:#4ade80; margin-bottom:4px;
}
.sidebar-sub { font-size:12px; color:#7a9a87; margin-bottom:24px; }

/* ── Eco note box ── */
.eco-note {
    background:#162a1f; border:1px solid #2a3d32;
    border-radius:10px; padding:12px 14px;
    font-size:13px; color:#7a9a87; margin-top:12px;
}

/* ── Diet rows ── */
.diet-row {
    display:flex; align-items:center; gap:12px;
    background:#1a2820; border-radius:10px;
    padding:10px 14px; margin-bottom:8px;
}
.diet-day { font-size:12px; color:#7a9a87; min-width:30px; }
.diet-meal { font-size:13px; color:#e8f0ec; }

/* ── Community rows ── */
.comm-row {
    display:flex; justify-content:space-between; align-items:center;
    background:#1a2820; border-radius:10px;
    padding:10px 14px; margin-bottom:8px;
}

/* ── Streamlit overrides ── */
.stButton > button {
    background: #4ade80 !important;
    color: #0b1210 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; }
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stSelectbox"] select {
    background: #0f1a14 !important;
    border: 1px solid #2a3d32 !important;
    color: #e8f0ec !important;
    border-radius: 10px !important;
}
div[data-testid="stMetric"] {
    background: #1a2820;
    border: 1px solid #2a3d32;
    border-radius: 12px;
    padding: 14px !important;
}
div[data-testid="stMetric"] label { color: #7a9a87 !important; font-size: 12px !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #4ade80 !important; font-size: 24px !important;
}
[data-testid="stAlert"] { border-radius: 10px !important; }
.stRadio label, .stSelectbox label, .stNumberInput label,
.stTextInput label, .stDateInput label { color: #7a9a87 !important; font-size: 13px !important; }
hr { border-color: #2a3d32 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATIC DATA
# ─────────────────────────────────────────────────────────────────────────────

FOODS_DB = {
    "rice":    dict(calories=206, protein=4.3,  fat=0.4,  carbs=45, digestion="2–3 hrs"),
    "banana":  dict(calories=89,  protein=1.1,  fat=0.3,  carbs=23, digestion="1–2 hrs"),
    "chicken": dict(calories=239, protein=27,   fat=14,   carbs=0,  digestion="3–5 hrs"),
    "oats":    dict(calories=307, protein=11,   fat=5,    carbs=55, digestion="2–4 hrs"),
    "egg":     dict(calories=155, protein=13,   fat=11,   carbs=1,  digestion="2–3 hrs"),
    "bread":   dict(calories=265, protein=9,    fat=3.2,  carbs=49, digestion="1–2 hrs"),
    "lentil":  dict(calories=116, protein=9,    fat=0.4,  carbs=20, digestion="2–4 hrs"),
    "spinach": dict(calories=23,  protein=2.9,  fat=0.4,  carbs=3.6,digestion="1–2 hrs"),
}
FOODS_DEFAULT = dict(calories=420, protein=18, fat=10, carbs=52, digestion="3–5 hrs")

COMMUNITY_MARKERS = [
    dict(lat=12.972, lng=77.595, name="Priya S.",  item="3 Apples",     qty="~0.5 kg"),
    dict(lat=12.981, lng=77.603, name="Rajan M.",  item="Bread Loaf",   qty="1 loaf"),
    dict(lat=12.968, lng=77.612, name="Deepa K.",  item="Dal",          qty="500 g"),
    dict(lat=12.960, lng=77.592, name="Arjun T.",  item="Mixed Veggies",qty="1 kg"),
    dict(lat=12.975, lng=77.581, name="Meena R.",  item="Rice",         qty="2 kg"),
]

NGOS = [
    dict(name="Robin Hood Army",  area="Pan-India",       focus="Meal distribution"),
    dict(name="Feeding India",    area="Bengaluru region",focus="Surplus food rescue"),
    dict(name="Roti Bank",        area="Mumbai & South",  focus="Chapati drives"),
    dict(name="No Waste Kitchen", area="Bengaluru",       focus="Zero-waste catering"),
]

WEEKLY_DIET = [
    ("Mon", "Oats + Banana + Nuts"),
    ("Tue", "Brown Rice + Dal + Curd"),
    ("Wed", "Chapati + Sabzi + Salad"),
    ("Thu", "Quinoa Soup + Roasted Veggies"),
    ("Fri", "Brown Rice + Grilled Chicken"),
    ("Sat", "Smoothie Bowl + Seasonal Fruits"),
    ("Sun", "Balanced Flex / Cheat Day"),
]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults = dict(
        history=[],
        total_food=0.0,
        total_waste=0.0,
        eco_score=100,
        co2_saved=0.0,
        pantry=[
            dict(id=1, name="Spinach",      expiry=date.today() + timedelta(hours=20/24)),
            dict(id=2, name="Greek Yogurt", expiry=date.today() + timedelta(days=2)),
            dict(id=3, name="Tomatoes",     expiry=date.today() + timedelta(days=5)),
        ],
        next_pantry_id=4,
        voice_active=False,
        scan_active=False,
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def hours_until_expiry(exp_date):
    delta = datetime.combine(exp_date, datetime.max.time()) - datetime.now()
    return delta.total_seconds() / 3600

def expiry_tag_html(exp_date):
    h = hours_until_expiry(exp_date)
    if h <= 24:
        return '<span class="tag-urgent">⚠ Urgent</span>'
    elif h <= 72:
        return '<span class="tag-soon">⏳ Soon</span>'
    return '<span class="tag-fresh">✓ Fresh</span>'

def calc_eco_score(total_food, total_waste):
    """
    Eco-Score = max(0, 100 − (totalWaste / totalFood × 100))
    Linear penalty: 1 point lost per 1% of food wasted.
    """
    if total_food == 0:
        return 100
    return max(0, round(100 - (total_waste / total_food * 100)))

def calc_co2_saved(total_food, total_waste):
    """
    CO₂ Savings = (totalFood − totalWaste) × 2.5 kg CO₂e
    Factor 2.5 from WRAP's lifecycle emissions for avoided food waste.
    """
    return round((total_food - total_waste) * 2.5, 2)

def calc_waste(food_kg, num_people):
    ratio = food_kg / num_people
    return max(0, 0.08 * food_kg + 0.002 * num_people
               + (0.15 * (ratio - 0.3) if ratio > 0.3 else 0))

def eco_score_color(score):
    if score >= 70: return "#4ade80"
    if score >= 40: return "#fbbf24"
    return "#f87171"

def lookup_nutrition(food_str):
    food_lower = food_str.lower()
    for key, data in FOODS_DB.items():
        if key in food_lower:
            return data
    return FOODS_DEFAULT

def build_gauge(score):
    color = eco_score_color(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"color": color, "size": 48}},
        gauge=dict(
            axis=dict(range=[0, 100], tickfont=dict(color="#7a9a87"), tickwidth=1),
            bar=dict(color=color, thickness=0.25),
            bgcolor="#1a2820",
            bordercolor="#2a3d32",
            steps=[
                dict(range=[0,  40], color="#3d1515"),
                dict(range=[40, 70], color="#3d2e00"),
                dict(range=[70,100], color="#1a3d28"),
            ],
        ),
        domain=dict(x=[0, 1], y=[0, 1]),
    ))
    fig.update_layout(
        height=240, margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8f0ec",
    )
    return fig

def build_history_chart(history):
    df = pd.DataFrame(history)
    fig = go.Figure()
    fig.add_bar(x=df.index + 1, y=df["food"],  name="Food (kg)",  marker_color="#2d6e48")
    fig.add_bar(x=df.index + 1, y=df["waste"], name="Waste (kg)", marker_color="#7f1d1d")
    fig.update_layout(
        barmode="group",
        xaxis_title="Prediction #",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#131d18",
        font_color="#7a9a87",
        legend=dict(font=dict(color="#7a9a87")),
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        xaxis=dict(gridcolor="#1a2820"),
        yaxis=dict(gridcolor="#1a2820"),
    )
    return fig

def build_community_map():
    m = folium.Map(
        location=[12.970, 77.597],
        zoom_start=14,
        tiles="CartoDB dark_matter",
    )
    # You marker
    folium.Marker(
        location=[12.970, 77.597],
        popup=folium.Popup("<b>You</b><br>Surplus Rice", max_width=160),
        tooltip="📍 You",
        icon=folium.Icon(color="green", icon="home", prefix="fa"),
    ).add_to(m)
    # Community markers
    for mk in COMMUNITY_MARKERS:
        folium.Marker(
            location=[mk["lat"], mk["lng"]],
            popup=folium.Popup(
                f"<b>{mk['name']}</b><br>{mk['item']} · {mk['qty']}", max_width=180
            ),
            tooltip=f"🌿 {mk['name']} — {mk['item']}",
            icon=folium.Icon(color="darkgreen", icon="leaf", prefix="fa"),
        ).add_to(m)
    return m

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌿 FoodWise AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">2026 Sustainability Platform</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        options=["🍽️  Predict", "📦  Pantry", "🧬  Nutrition", "🥗  Diet",
                 "🗺️  Community", "📊  Dashboard", "🤝  Donate"],
        label_visibility="collapsed",
    )
    st.divider()

    # Mini stats in sidebar
    st.markdown("**Session Stats**")
    st.markdown(f"""
    <div style="font-size:13px;color:#7a9a87;line-height:2">
    🌱 Eco-Score: <b style="color:#4ade80">{st.session_state.eco_score}</b><br>
    🍱 Total Food: <b style="color:#e8f0ec">{st.session_state.total_food:.1f} kg</b><br>
    ♻️ CO₂ Saved: <b style="color:#4ade80">{st.session_state.co2_saved} kg</b><br>
    📋 Predictions: <b style="color:#e8f0ec">{len(st.session_state.history)}</b>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
#  1.  PREDICT
# ══════════════════════════════════════════════════════════════════════════════
if page.startswith("🍽️"):
    st.markdown("## 🍽️ Food Waste Prediction")

    col_form, col_score = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">Enter Food Details</div>', unsafe_allow_html=True)

        # ── Multimodal HCI buttons ─────────────────────────────────────────
        hci_col1, hci_col2 = st.columns(2)
        with hci_col1:
            if st.button("🎤  Voice Input", key="voice_btn"):
                st.session_state.voice_active = not st.session_state.voice_active

        with hci_col2:
            if st.button("📷  Barcode Scan", key="scan_btn"):
                st.session_state.scan_active = not st.session_state.scan_active

        if st.session_state.voice_active:
            st.info(
                "🎤 **Voice mode active** — In production, integrate `speech_recognition` "
                "library with Google Web Speech API. Say: *'5 kg rice, 20 people'*",
                icon="🎙️",
            )
        if st.session_state.scan_active:
            st.info(
                "📷 **Barcode mode active** — In production, integrate `pyzbar` + `opencv-python` "
                "to decode product barcodes from camera stream and auto-fill quantity.",
                icon="📦",
            )

        st.divider()

        food_kg = st.number_input("Food quantity (kg)", min_value=0.1, max_value=1000.0,
                                   value=5.0, step=0.5)
        num_people = st.number_input("Number of people", min_value=1, max_value=10000,
                                      value=20, step=1)

        analyze = st.button("⚡ Analyze Waste")
        st.markdown("</div>", unsafe_allow_html=True)

        if analyze:
            waste = calc_waste(food_kg, num_people)
            waste = round(waste, 2)
            served = math.floor(food_kg / 0.3)

            st.session_state.total_food  += food_kg
            st.session_state.total_waste += waste
            st.session_state.eco_score    = calc_eco_score(
                st.session_state.total_food, st.session_state.total_waste)
            st.session_state.co2_saved    = calc_co2_saved(
                st.session_state.total_food, st.session_state.total_waste)
            st.session_state.history.append(
                dict(food=food_kg, waste=waste, served=served, people=num_people))

            st.success(f"✅ Estimated waste: **{waste} kg** | People that can be served: **{served}**")

    with col_score:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">🌱 Eco-Score</div>', unsafe_allow_html=True)
        st.plotly_chart(build_gauge(st.session_state.eco_score),
                        use_container_width=True, config={"displayModeBar": False})

        color = eco_score_color(st.session_state.eco_score)
        level = ("Excellent 🌟" if st.session_state.eco_score >= 70
                 else "Moderate ⚠️" if st.session_state.eco_score >= 40
                 else "Critical 🔴")
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-tile">
                <div class="stat-val">{st.session_state.total_food:.1f}</div>
                <div class="stat-lbl">Total Food (kg)</div>
            </div>
            <div class="stat-tile">
                <div class="stat-val-red">{st.session_state.total_waste:.2f}</div>
                <div class="stat-lbl">Waste (kg)</div>
            </div>
            <div class="stat-tile">
                <div class="stat-val">{st.session_state.co2_saved}</div>
                <div class="stat-lbl">CO₂ Saved (kg)</div>
            </div>
        </div>
        <div class="eco-note">
            <b>Algorithm:</b> Score = max(0, 100 − waste% × 100)<br>
            <b>CO₂:</b> (food − waste) × 2.5 kg CO₂e (WRAP factor)<br>
            <b>Status:</b> <span style="color:{color}">{level}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  2.  PANTRY
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("📦"):
    st.markdown("## 📦 Smart Pantry Manager")

    col_add, col_list = st.columns([1, 1.2], gap="large")

    with col_add:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">Add New Item</div>', unsafe_allow_html=True)

        item_name = st.text_input("Item name", placeholder="e.g. Spinach, Tomatoes…")
        exp_date  = st.date_input("Expiry date", value=date.today() + timedelta(days=3),
                                   min_value=date.today())

        if st.button("➕ Add to Pantry"):
            if item_name.strip():
                st.session_state.pantry.append(dict(
                    id=st.session_state.next_pantry_id,
                    name=item_name.strip(),
                    expiry=exp_date,
                ))
                st.session_state.next_pantry_id += 1
                st.success(f"Added **{item_name}** to pantry!")
            else:
                st.warning("Please enter an item name.")

        # ── Urgent recipe suggestion ───────────────────────────────────────
        urgent_items = [p for p in st.session_state.pantry
                        if hours_until_expiry(p["expiry"]) <= 24]
        if urgent_items:
            st.divider()
            names = ", ".join(p["name"] for p in urgent_items)
            st.warning(f"⚠️ **{len(urgent_items)} item(s) expiring within 24 hours:** {names}")
            if st.button("🍳 Generate Recipe Ideas"):
                st.info(
                    f"**Suggested Recipe:** {urgent_items[0]['name']} Stir-Fry — "
                    "In production, call an LLM/Spoonacular API with urgent item list "
                    "to get real recipe suggestions.",
                    icon="👨‍🍳",
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Expiry summary donut ───────────────────────────────────────────
        if st.session_state.pantry:
            urgent  = sum(1 for p in st.session_state.pantry if hours_until_expiry(p["expiry"]) <= 24)
            soon    = sum(1 for p in st.session_state.pantry if 24 < hours_until_expiry(p["expiry"]) <= 72)
            fresh   = len(st.session_state.pantry) - urgent - soon
            donut = go.Figure(go.Pie(
                labels=["Urgent", "Soon", "Fresh"],
                values=[urgent, soon, fresh],
                marker_colors=["#f87171", "#fbbf24", "#4ade80"],
                hole=0.6,
                textfont=dict(color="#e8f0ec"),
            ))
            donut.update_layout(
                height=200, showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#7a9a87",
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(font=dict(color="#7a9a87", size=11)),
            )
            st.plotly_chart(donut, use_container_width=True, config={"displayModeBar": False})

    with col_list:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="fw-card-title">🗄️ Inventory ({len(st.session_state.pantry)} items)</div>',
                    unsafe_allow_html=True)

        if not st.session_state.pantry:
            st.markdown('<p style="color:#7a9a87;font-size:13px">Pantry is empty.</p>',
                        unsafe_allow_html=True)
        else:
            to_delete = None
            for item in st.session_state.pantry:
                tag_html = expiry_tag_html(item["expiry"])
                st.markdown(f"""
                <div class="pantry-row">
                    <div>
                        <div class="pantry-name">{item['name']}</div>
                        <div class="pantry-date">Expires: {item['expiry'].strftime('%d %b %Y')}</div>
                    </div>
                    <div>{tag_html}</div>
                </div>
                """, unsafe_allow_html=True)
                # Delete button rendered below the HTML row
                if st.button("✕", key=f"del_{item['id']}",
                             help=f"Remove {item['name']}"):
                    to_delete = item["id"]

            if to_delete:
                st.session_state.pantry = [
                    p for p in st.session_state.pantry if p["id"] != to_delete]
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  3.  NUTRITION
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("🧬"):
    st.markdown("## 🧬 Nutrition Analyzer")

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">Analyze a Food Item</div>', unsafe_allow_html=True)
        food_name = st.text_input("Food name",
                                   placeholder="rice, banana, chicken, oats, egg…")

        uploaded = st.file_uploader("Or upload a food image (future: vision AI)",
                                     type=["jpg", "jpeg", "png"],
                                     help="In production: send to Claude Vision / USDA FoodData API")
        if uploaded:
            st.image(uploaded, caption="Uploaded image", use_container_width=True)
            st.info("📸 In production, this image is sent to a vision model to identify "
                    "the food and auto-fill the analyzer.", icon="🤖")

        analyze_nut = st.button("🔬 Analyze Nutrition")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_result:
        if analyze_nut and food_name.strip():
            nut = lookup_nutrition(food_name)
            st.markdown('<div class="fw-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="fw-card-title">Results for: {food_name.title()}</div>',
                        unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("🔥 Calories", f"{nut['calories']} kcal")
            m2.metric("💪 Protein",  f"{nut['protein']}g")
            m3.metric("🥑 Fat",      f"{nut['fat']}g")
            m4, m5 = st.columns(2)
            m4.metric("🌾 Carbs",     f"{nut['carbs']}g")
            m5.metric("⏳ Digestion", nut["digestion"])

            # Macro donut
            macro_fig = go.Figure(go.Pie(
                labels=["Protein", "Fat", "Carbs"],
                values=[nut["protein"], nut["fat"], nut["carbs"]],
                marker_colors=["#4ade80", "#fbbf24", "#60a5fa"],
                hole=0.55,
                textfont=dict(color="#e8f0ec"),
            ))
            macro_fig.update_layout(
                height=200, paper_bgcolor="rgba(0,0,0,0)",
                font_color="#7a9a87", margin=dict(l=0, r=0, t=10, b=0),
                showlegend=True, legend=dict(font=dict(color="#7a9a87", size=11)),
            )
            st.plotly_chart(macro_fig, use_container_width=True,
                            config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
        elif analyze_nut:
            st.warning("Please enter a food name.")


# ══════════════════════════════════════════════════════════════════════════════
#  4.  DIET
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("🥗"):
    st.markdown("## 🥗 Smart Diet Plan")

    col_form, col_plan = st.columns([1, 1.2], gap="large")

    with col_form:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">Personalize Your Plan</div>', unsafe_allow_html=True)

        age    = st.number_input("Age",        min_value=10, max_value=100, value=25)
        weight = st.number_input("Weight (kg)",min_value=20.0, max_value=300.0, value=65.0)
        height = st.number_input("Height (cm)",min_value=100, max_value=250, value=170)
        gender = st.selectbox("Gender", ["Male", "Female"])
        goal   = st.selectbox("Goal", ["Maintain weight", "Lose weight", "Gain muscle"])

        gen = st.button("🥗 Generate Plan")
        st.markdown("</div>", unsafe_allow_html=True)

        if gen:
            # Mifflin-St Jeor BMR
            if gender == "Male":
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            tdee = bmr * 1.55  # Moderate activity
            if goal == "Lose weight":   target = tdee - 500
            elif goal == "Gain muscle": target = tdee + 300
            else:                       target = tdee

            bmi = weight / ((height / 100) ** 2)
            bmi_cat = ("Underweight" if bmi < 18.5 else
                       "Normal" if bmi < 25 else
                       "Overweight" if bmi < 30 else "Obese")

            st.markdown(f"""
            <div class="fw-card">
                <div class="fw-card-title">📊 Your Metrics</div>
                <div class="stat-grid">
                    <div class="stat-tile">
                        <div class="stat-val">{round(bmr)}</div>
                        <div class="stat-lbl">BMR (kcal)</div>
                    </div>
                    <div class="stat-tile">
                        <div class="stat-val">{round(target)}</div>
                        <div class="stat-lbl">Target (kcal/day)</div>
                    </div>
                    <div class="stat-tile">
                        <div class="stat-val-white">{bmi:.1f}</div>
                        <div class="stat-lbl">BMI · {bmi_cat}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_plan:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">📅 Weekly Meal Plan</div>', unsafe_allow_html=True)
        for day, meal in WEEKLY_DIET:
            st.markdown(f"""
            <div class="diet-row">
                <span class="diet-day">{day}</span>
                <span class="diet-meal">{meal}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Macro split bar
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">🎯 Recommended Macro Split</div>',
                    unsafe_allow_html=True)
        macros = dict(Protein=30, Carbohydrates=45, Fats=25)
        macro_bar = go.Figure(go.Bar(
            x=list(macros.values()),
            y=list(macros.keys()),
            orientation="h",
            marker_color=["#4ade80", "#60a5fa", "#fbbf24"],
            text=[f"{v}%" for v in macros.values()],
            textposition="inside",
            textfont=dict(color="#0b1210", size=12),
        ))
        macro_bar.update_layout(
            height=130, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#131d18", font_color="#7a9a87",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
            yaxis=dict(gridcolor="#1a2820"),
        )
        st.plotly_chart(macro_bar, use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  5.  COMMUNITY MAP
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("🗺️"):
    st.markdown("## 🗺️ Community Food Sharing")

    col_map, col_list = st.columns([1.4, 1], gap="large")

    with col_map:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">Live P2P Sharing Map — Bengaluru</div>',
                    unsafe_allow_html=True)
        st.caption("Click a marker to see what neighbours are sharing.")
        st_folium(build_community_map(), width=None, height=380, returned_objects=[])
        st.markdown("</div>", unsafe_allow_html=True)

    with col_list:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">📦 Available Nearby</div>',
                    unsafe_allow_html=True)
        for mk in COMMUNITY_MARKERS:
            st.markdown(f"""
            <div class="comm-row">
                <div>
                    <div style="font-weight:600;font-size:14px">{mk['item']} · {mk['qty']}</div>
                    <div style="font-size:12px;color:#7a9a87">Shared by {mk['name']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.button("Request →", key=f"req_{mk['name']}",
                      help=f"Request {mk['item']} from {mk['name']}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">📤 Share Your Surplus</div>',
                    unsafe_allow_html=True)
        share_item = st.text_input("What are you sharing?", placeholder="e.g. 2 kg Rice")
        share_qty  = st.text_input("Quantity", placeholder="e.g. 2 kg")
        if st.button("📍 Post to Community"):
            if share_item.strip():
                st.success(f"✅ Posted **{share_item}** to the community map!")
            else:
                st.warning("Please enter an item name.")
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  6.  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("📊"):
    st.markdown("## 📊 Sustainability Dashboard")

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌱 Eco-Score",    st.session_state.eco_score, delta=None)
    c2.metric("🍱 Total Food",   f"{st.session_state.total_food:.1f} kg")
    c3.metric("♻️ Waste",        f"{st.session_state.total_waste:.2f} kg")
    c4.metric("🌍 CO₂ Saved",    f"{st.session_state.co2_saved} kg")

    st.divider()

    col_gauge, col_chart = st.columns([1, 1.5], gap="large")

    with col_gauge:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">🌱 Eco-Score Gauge</div>', unsafe_allow_html=True)
        st.plotly_chart(build_gauge(st.session_state.eco_score),
                        use_container_width=True, config={"displayModeBar": False})
        color = eco_score_color(st.session_state.eco_score)
        level = ("Excellent 🌟" if st.session_state.eco_score >= 70
                 else "Moderate ⚠️" if st.session_state.eco_score >= 40
                 else "Critical 🔴")
        st.markdown(f"""
        <div class="eco-note">
            <b>Score:</b> {st.session_state.eco_score}/100 &nbsp;·&nbsp;
            <span style="color:{color}">{level}</span><br>
            <b>CO₂ prevented:</b> {st.session_state.co2_saved} kg CO₂e<br>
            <b>Equiv. to:</b> {round(st.session_state.co2_saved / 21, 1)} trees planted 🌳
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<div class="fw-card-title">📈 Prediction History</div>',
                    unsafe_allow_html=True)
        if st.session_state.history:
            st.plotly_chart(build_history_chart(st.session_state.history),
                            use_container_width=True, config={"displayModeBar": False})
            df = pd.DataFrame(st.session_state.history)
            df.index += 1
            df.columns = ["Food (kg)", "Waste (kg)", "People Served", "People Present"]
            st.dataframe(df.style.format("{:.2f}"),
                         use_container_width=True, height=160)
        else:
            st.markdown(
                '<p style="color:#7a9a87;font-size:13px;padding:20px;text-align:center">'
                'No predictions yet. Go to Predict tab to get started.</p>',
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  7.  DONATE
# ══════════════════════════════════════════════════════════════════════════════
elif page.startswith("🤝"):
    st.markdown("## 🤝 Donate Surplus Food")

    for ngo in NGOS:
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div class="ngo-row">
                <div>
                    <div class="ngo-name">{ngo['name']}</div>
                    <div class="ngo-sub">📍 {ngo['area']} &nbsp;·&nbsp; {ngo['focus']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            if st.button(f"Donate →", key=f"donate_{ngo['name']}"):
                st.success(f"🎉 Donation request sent to **{ngo['name']}**! They will contact you shortly.")
    st.divider()
    st.markdown("""
    <div class="eco-note">
        💡 <b>How it works:</b> Log your surplus food in the Community tab, then contact
        one of the NGOs above. Most accept same-day pickups for quantities above 2 kg.
        Every kg donated prevents ~2.5 kg CO₂e from entering the atmosphere.
    </div>
    """, unsafe_allow_html=True)



    
    
