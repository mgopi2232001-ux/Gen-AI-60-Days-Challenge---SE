import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# GLOBAL STYLES
# =============================================================================
st.markdown(
    """
    <style>
    /* Global background + font */
    .stApp {
        background: radial-gradient(circle at top, #111827 0, #020617 40%, #000000 100%);
        color: #f9fafb;
    }

    html, body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Page title */
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #9ca3af;
        margin-bottom: 1.2rem;
    }

    /* Card containers */
    .card {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        border: 1px solid rgba(148, 163, 184, 0.2);
    }

    .card-soft {
        background: rgba(15, 23, 42, 0.7);
        border-radius: 14px;
        padding: 14px 16px;
        border: 1px solid rgba(55, 65, 81, 0.6);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    /* BMI result badges */
    .bmi-result-normal,
    .bmi-result-overweight,
    .bmi-result-obese,
    .bmi-result-underweight {
        padding: 14px 10px;
        border-radius: 16px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .bmi-result-normal {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: #ecfdf5;
    }
    .bmi-result-overweight {
        background: linear-gradient(135deg, #facc15, #eab308);
        color: #1f2937;
    }
    .bmi-result-obese {
        background: linear-gradient(135deg, #f97373, #ef4444);
        color: #fef2f2;
    }
    .bmi-result-underweight {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9);
        color: #e0f2fe;
    }

    .bmi-result-normal h1,
    .bmi-result-overweight h1,
    .bmi-result-obese h1,
    .bmi-result-underweight h1 {
        margin: 0;
        font-size: 2.4rem;
    }

    .bmi-result-normal p,
    .bmi-result-overweight p,
    .bmi-result-obese p,
    .bmi-result-underweight p {
        margin: 2px 0 0 0;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(31, 41, 55, 0.9);
    }
    .css-1v3fvcr, .css-1d391kg {
        color: #e5e7eb !important;
    }

    /* Dataframe tweaks (dark mode) */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(55, 65, 81, 0.8);
    }

    /* Footer text */
    .app-footer {
        text-align: center;
        color: #6b7280;
        font-size: 11px;
        padding: 6px 0 2px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# SESSION STATE
# =============================================================================
if "bmi_history" not in st.session_state:
    st.session_state.bmi_history = []

# =============================================================================
# HELPERS
# =============================================================================
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight", "normal"
    elif 25 <= bmi < 30:
        return "Overweight", "overweight"
    else:
        return "Obese", "obese"

def get_healthy_weight_range(height_m):
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return min_weight, max_weight

# =============================================================================
# SIDEBAR NAV
# =============================================================================
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Calculator", "BMI Chart", "Health Tips", "History"],
    index=0
)

# =============================================================================
# HEADER
# =============================================================================
st.markdown(
    """
    <div class="card" style="margin-bottom: 12px;">
        <div class="main-title">⚖️ BMI & Health Tracker</div>
        <div class="main-subtitle">
            Quick BMI check, smart calorie estimates, and a simple history to see your progress over time.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# PAGE: CALCULATOR
# =============================================================================
if page == "Calculator":
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Your Details</div>', unsafe_allow_html=True)

        unit = st.radio(
            "Unit system",
            ["Metric (kg, cm)", "Imperial (lbs, inches)"],
            horizontal=True
        )

        if unit == "Metric (kg, cm)":
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
            height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0, step=0.1)
            height_m = height_cm / 100
        else:
            weight_lbs = st.number_input("Weight (lbs)", min_value=1.0, max_value=1100.0, value=154.0, step=0.1)
            height_inches = st.number_input("Height (inches)", min_value=20.0, max_value=100.0, value=69.0, step=0.1)
            weight = weight_lbs * 0.453592
            height_m = height_inches * 0.0254
            height_cm = height_inches * 2.54

        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👤 Extra Info</div>', unsafe_allow_html=True)

        col_age, col_gender = st.columns(2)
        with col_age:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
        with col_gender:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        activity_level = st.selectbox(
            "Activity level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Your BMI Result</div>', unsafe_allow_html=True)

        bmi = calculate_bmi(weight, height_m)
        category, color = get_bmi_category(bmi)
        min_weight, max_weight = get_healthy_weight_range(height_m)

        html_class = f"bmi-result-{color}"
        st.markdown(
            f"""
            <div class="{html_class}">
                <h1>{bmi:.1f}</h1>
                <p>{category}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Weight", f"{weight:.1f} kg")
            st.metric("Height", f"{height_m:.2f} m")
        with metric_col2:
            st.metric("BMI", f"{bmi:.1f}")
            st.metric("Status", category)

        st.markdown('<div class="card-soft" style="margin-top: 12px;">', unsafe_allow_html=True)
        st.markdown("**🎯 Healthy weight for your height**", unsafe_allow_html=True)
        st.write(
            f"For your height, a healthy weight range is roughly **{min_weight:.1f} kg – {max_weight:.1f} kg**."
        )

        if bmi < 18.5:
            weight_diff = min_weight - weight
            st.warning(f"You're under the normal range. Approx weight to gain: **{weight_diff:.1f} kg**.")
        elif bmi >= 30:
            weight_diff = weight - max_weight
            st.warning(f"You're above the normal range. Approx weight to lose: **{weight_diff:.1f} kg**.")
        else:
            st.success("You're in the normal BMI range. Keep the good habits going 🚀")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Caloric Needs Card ----
    st.markdown('<div class="card" style="margin-top: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔥 Daily Calorie Estimate (Mifflin-St Jeor)</div>', unsafe_allow_html=True)

    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:  # Female / Other
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9,
    }

    tdee = bmr * activity_multipliers[activity_level]

    col_bmr, col_tdee, col_def, col_sur = st.columns(4)
    with col_bmr:
        st.metric("BMR", f"{bmr:.0f} cal/day")
    with col_tdee:
        st.metric("TDEE", f"{tdee:.0f} cal/day")
    with col_def:
        st.metric("Cutting Target", f"{tdee - 500:.0f} cal/day", help="Approx. 500 cal deficit")
    with col_sur:
        st.metric("Bulking Target", f"{tdee + 500:.0f} cal/day", help="Approx. 500 cal surplus")

    st.caption("These numbers are rough estimates, not medical advice. Use them as a starting point, not a rulebook.")

    # Save to history
    st.markdown("---")
    if st.button("💾 Save this entry to history"):
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "weight": weight,
            "height": height_m,
            "bmi": bmi,
            "category": category,
            "age": age,
            "gender": gender,
            "bmr": bmr,
            "tdee": tdee,
        }
        st.session_state.bmi_history.append(history_entry)
        st.success("Saved. Check the **History** tab to see your trend ✅")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE: BMI CHART
# =============================================================================
elif page == "BMI Chart":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 BMI Categories</div>', unsafe_allow_html=True)

    bmi_chart_data = {
        "Category": [
            "Underweight",
            "Normal Weight",
            "Overweight",
            "Obese (Class I)",
            "Obese (Class II)",
            "Obese (Class III)",
        ],
        "BMI Range": ["< 18.5", "18.5 - 24.9", "25.0 - 29.9", "30.0 - 34.9", "35.0 - 39.9", "≥ 40.0"],
        "Health Risk": ["Low (but risk of other issues)", "Low", "Increased", "High", "Very High", "Very High"],
    }
    df_chart = pd.DataFrame(bmi_chart_data)
    st.dataframe(df_chart, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💪 Healthy Weight by Height</div>', unsafe_allow_html=True)

    heights = [150, 160, 170, 180, 190, 200]
    weight_data = []
    for h in heights:
        h_m = h / 100
        min_w, max_w = get_healthy_weight_range(h_m)
        feet = int(h / 30.48)
        inches = int((h / 2.54) % 12)
        weight_data.append(
            {
                "Height (cm)": h,
                "Height (ft'in\")": f"{feet}'{inches}\"",
                "Min Healthy Weight (kg)": f"{min_w:.1f}",
                "Max Healthy Weight (kg)": f"{max_w:.1f}",
            }
        )
    df_weights = pd.DataFrame(weight_data)
    st.dataframe(df_weights, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 BMI Range Visualization</div>', unsafe_allow_html=True)

    bmi_values = list(range(15, 45, 5))
    categories = [get_bmi_category(bmi)[0] for bmi in bmi_values]
    chart_df = pd.DataFrame({"BMI": bmi_values, "Category": categories})
    st.bar_chart(data=chart_df.set_index("BMI"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE: HEALTH TIPS
# =============================================================================
elif page == "Health Tips":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Health Tips & Recommendations</div>', unsafe_allow_html=True)

    tips_tabs = st.tabs(["🥗 Nutrition", "🏃 Exercise", "🌙 Lifestyle", "🏥 Medical"])

    with tips_tabs[0]:
        st.write(
            """
            - Eat a balanced plate: protein + complex carbs + healthy fats
            - Watch portions (especially oils, nuts, sweets)
            - Stay hydrated – a basic target is 8 glasses/day
            - Cut down on ultra-processed junk & sugary drinks
            - Add more veggies and fruits (aim for ~5 servings/day)
            - Prefer whole grains: brown rice, millets, oats, whole wheat
            - Plan your meals so you're not stuck with random food choices
            """
        )

    with tips_tabs[1]:
        st.write(
            """
            - Target ~150 mins/week of moderate cardio (brisk walk, cycle, etc.)
            - Do strength training 2–3 times/week (bodyweight also works)
            - Warm up before and cool down after your workouts
            - Progress slowly: add intensity or time week by week
            - Choose activities you actually enjoy so you’ll stick to them
            - Keep at least 1–2 rest days for recovery
            """
        )

    with tips_tabs[2]:
        st.write(
            """
            - Aim for 7–9 hours of sleep, consistently
            - Manage stress with breathing exercises, meditation, or journaling
            - Avoid smoking and limit alcohol
            - Do periodic health checkups for BP, sugar, cholesterol, etc.
            - Stay socially connected with family & friends
            - Eat mindfully – avoid scrolling while eating if possible
            """
        )

    with tips_tabs[3]:
        st.write(
            """
            - If your BMI is extremely high/low, get a doctor’s opinion
            - If you have diabetes, BP, heart issues, thyroid, etc., don’t rely on BMI alone
            - Get medical clearance before starting intense workouts
            - Consult a doctor for unexplained weight loss/gain, chest pain, dizziness, or extreme fatigue
            - For diet plans or gym schedules tailored to your body, always talk to a professional
            """
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PAGE: HISTORY
# =============================================================================
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📜 BMI History</div>', unsafe_allow_html=True)

    if st.session_state.bmi_history:
        history_df = pd.DataFrame(st.session_state.bmi_history)
        st.markdown(f"Total Records: **{len(history_df)}**")
        st.dataframe(history_df, use_container_width=True)

        if len(history_df) > 1:
            st.markdown('<div class="section-title" style="margin-top: 10px;">📈 Trend</div>', unsafe_allow_html=True)
            trend_df = pd.DataFrame(
                {
                    "Date": history_df["date"],
                    "BMI": history_df["bmi"],
                    "Weight (kg)": history_df["weight"],
                }
            )
            st.line_chart(data=trend_df.set_index("Date"))

        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            avg_bmi = history_df["bmi"].mean()
            st.metric("Average BMI", f"{avg_bmi:.1f}")
        with col_stat2:
            min_bmi = history_df["bmi"].min()
            st.metric("Min BMI", f"{min_bmi:.1f}")
        with col_stat3:
            max_bmi = history_df["bmi"].max()
            st.metric("Max BMI", f"{max_bmi:.1f}")
        with col_stat4:
            weight_change = history_df["weight"].iloc[-1] - history_df["weight"].iloc[0]
            st.metric("Weight Change (kg)", f"{weight_change:.1f}", delta=weight_change)

        st.markdown("---")
        if st.button("🗑️ Clear history"):
            st.session_state.bmi_history = []
            st.success("History cleared.")
            st.experimental_rerun()
    else:
        st.info("No records yet. Go to **Calculator** and save your first entry.")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown(
    """
    <div class="app-footer">
        ⚠️ This tool is for general information only. Always take medical decisions with a qualified professional.<br>
        BMI Calculator v1.0 • Session-only data • Built with ❤️ on Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
