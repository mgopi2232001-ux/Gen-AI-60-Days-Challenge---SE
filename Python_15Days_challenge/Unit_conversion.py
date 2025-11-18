import streamlit as st
import pandas as pd

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Ultimate Unit Converter",
    page_icon="🔁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# GLOBAL STYLES (DARK THEME, WHITE TEXT)
# =============================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    background: #050816;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, h4, h5, h6, label, p, span, div {
    color: #FFFFFF !important;
}

/* Cards */
.converter-card {
    background: linear-gradient(145deg, #0B1120, #020617);
    border-radius: 18px;
    padding: 20px 18px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.6);
    border: 1px solid rgba(148, 163, 184, 0.3);
}

/* Result badge */
.result-badge {
    background: radial-gradient(circle at top left, #22C55E, #16A34A);
    border-radius: 999px;
    padding: 10px 18px;
    display: inline-block;
    font-weight: 600;
    margin-top: 8px;
}

/* Inputs + selects */
input, select, textarea {
    color: #FFFFFF !important;
}

/* Slider label */
[data-baseweb="slider"] > div:nth-child(1) {
    color: #FFFFFF !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# SESSION STATE INIT
# =============================================================================
if "history" not in st.session_state:
    st.session_state["history"] = []

# state for swaps (separate from widget keys)
defaults = {
    "cur_from": "INR",
    "cur_to": "USD",
    "temp_from": "Celsius (°C)",
    "temp_to": "Fahrenheit (°F)",
    "len_from": "Centimeter (cm)",
    "len_to": "Inch (in)",
    "w_from": "Kilogram (kg)",
    "w_to": "Pound (lb)",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =============================================================================
# SIDEBAR SETTINGS
# =============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    decimal_places = st.slider("Decimal places", 0, 6, 2)
    show_steps = st.checkbox("Show formula / steps", value=True)

    st.markdown("---")
    st.markdown("### 💱 Currency Settings")
    fx_rate = st.number_input(
        "Static rate (1 USD = ? INR)",
        min_value=1.0,
        max_value=200.0,
        value=84.0,
        step=0.1,
    )
    st.caption("Using static rate only (no live FX).")

# =============================================================================
# HELPERS
# =============================================================================
def add_to_history(category, amount, from_unit, to_unit, result, extra=""):
    entry = {
        "Category": category,
        "Input": f"{amount} {from_unit}",
        "Output": f"{round(result, decimal_places)} {to_unit}",
        "Details": extra,
    }
    st.session_state["history"].append(entry)
    st.session_state["history"] = st.session_state["history"][-10:]


def round_num(x):
    try:
        return round(x, decimal_places)
    except Exception:
        return x


# =============================================================================
# MAIN TITLE
# =============================================================================
st.markdown("## 🔁 Ultimate Unit Converter")
st.caption("Currency • Temperature • Length • Weight • Bulk mode — all in one place.")

# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💱 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight", "📊 Bulk Mode"]
)

# =============================================================================
# TAB 1: CURRENCY
# =============================================================================
with tab1:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("Currency — INR ⇄ USD")

    col1, _ = st.columns([2, 1])
    with col1:
        amount_cur = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)

    options_cur = ["INR", "USD"]
    col3, col4 = st.columns(2)
    with col3:
        from_currency = st.selectbox(
            "From",
            options_cur,
            index=options_cur.index(st.session_state.cur_from),
            key="cur_from_widget",
        )
    with col4:
        to_currency = st.selectbox(
            "To",
            options_cur,
            index=options_cur.index(st.session_state.cur_to),
            key="cur_to_widget",
        )

    # update state from widget values
    st.session_state.cur_from = from_currency
    st.session_state.cur_to = to_currency

    if st.button("Swap units ⇄", key="swap_currency"):
        st.session_state.cur_from, st.session_state.cur_to = (
            st.session_state.cur_to,
            st.session_state.cur_from,
        )

    from_currency = st.session_state.cur_from
    to_currency = st.session_state.cur_to

    if from_currency == to_currency:
        st.warning("Choose different units to convert.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Convert 💱", key="convert_currency"):
            if amount_cur == 0:
                st.info("Enter an amount greater than zero.")
            else:
                if from_currency == "INR" and to_currency == "USD":
                    result_cur = amount_cur / fx_rate
                    formula = f"{amount_cur} INR ÷ {fx_rate} = {round_num(result_cur)} USD"
                else:
                    result_cur = amount_cur * fx_rate
                    formula = f"{amount_cur} USD × {fx_rate} = {round_num(result_cur)} INR"

                st.markdown(
                    f'<div class="result-badge">Result: {round_num(result_cur)} {to_currency}</div>',
                    unsafe_allow_html=True,
                )

                if show_steps:
                    st.markdown("#### Steps")
                    st.code(formula, language="text")

                extra = f"Rate used: 1 USD = {fx_rate} INR"
                add_to_history("Currency", amount_cur, from_currency, to_currency, result_cur, extra)

        st.caption(f"Static rate in use: 1 USD = {fx_rate} INR")
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: TEMPERATURE
# =============================================================================
with tab2:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("Temperature — °C ⇄ °F")

    col1, _ = st.columns([2, 1])
    with col1:
        temp_val = st.number_input("Temperature", value=37.0, step=0.5)

    temp_options = ["Celsius (°C)", "Fahrenheit (°F)"]
    col3, col4 = st.columns(2)
    with col3:
        from_temp = st.selectbox(
            "From",
            temp_options,
            index=temp_options.index(st.session_state.temp_from),
            key="temp_from_widget",
        )
    with col4:
        to_temp = st.selectbox(
            "To",
            temp_options,
            index=temp_options.index(st.session_state.temp_to),
            key="temp_to_widget",
        )

    st.session_state.temp_from = from_temp
    st.session_state.temp_to = to_temp

    if st.button("Swap units ⇄", key="swap_temp"):
        st.session_state.temp_from, st.session_state.temp_to = (
            st.session_state.temp_to,
            st.session_state.temp_from,
        )

    from_temp = st.session_state.temp_from
    to_temp = st.session_state.temp_to

    if from_temp == to_temp:
        st.warning("Choose different units to convert.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Convert 🌡️", key="convert_temp"):
            if from_temp.startswith("Celsius"):
                res_temp = (temp_val * 9 / 5) + 32
                formula = f"({temp_val} × 9/5) + 32 = {round_num(res_temp)}"
                from_u, to_u = "°C", "°F"
            else:
                res_temp = (temp_val - 32) * 5 / 9
                formula = f"({temp_val} - 32) × 5/9 = {round_num(res_temp)}"
                from_u, to_u = "°F", "°C"

            st.markdown(
                f'<div class="result-badge">Result: {round_num(res_temp)} {to_u}</div>',
                unsafe_allow_html=True,
            )

            if show_steps:
                st.markdown("#### Steps")
                st.code(formula, language="text")

            add_to_history("Temperature", temp_val, from_u, to_u, res_temp)

        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 3: LENGTH
# =============================================================================
with tab3:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("Length — cm ⇄ inch (plus m & ft)")

    length_units = {
        "Centimeter (cm)": "cm",
        "Meter (m)": "m",
        "Inch (in)": "in",
        "Foot (ft)": "ft",
    }
    length_factor_cm = {
        "cm": 1.0,
        "m": 100.0,
        "in": 2.54,
        "ft": 30.48,
    }

    col1, _ = st.columns([2, 1])
    with col1:
        length_val = st.number_input("Length", value=100.0, step=1.0)

    len_labels = list(length_units.keys())
    col3, col4 = st.columns(2)
    with col3:
        from_len_label = st.selectbox(
            "From",
            len_labels,
            index=len_labels.index(st.session_state.len_from),
            key="len_from_widget",
        )
    with col4:
        to_len_label = st.selectbox(
            "To",
            len_labels,
            index=len_labels.index(st.session_state.len_to),
            key="len_to_widget",
        )

    st.session_state.len_from = from_len_label
    st.session_state.len_to = to_len_label

    if st.button("Swap units ⇄", key="swap_length"):
        st.session_state.len_from, st.session_state.len_to = (
            st.session_state.len_to,
            st.session_state.len_from,
        )

    from_len_label = st.session_state.len_from
    to_len_label = st.session_state.len_to

    from_len_code = length_units[from_len_label]
    to_len_code = length_units[to_len_label]

    if from_len_code == to_len_code:
        st.warning("Choose different units to convert.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Convert 📏", key="convert_length"):
            in_cm = length_val * length_factor_cm[from_len_code]
            res_len = in_cm / length_factor_cm[to_len_code]

            st.markdown(
                f'<div class="result-badge">Result: {round_num(res_len)} {to_len_code}</div>',
                unsafe_allow_html=True,
            )

            if show_steps:
                step_text = (
                    f"1. Convert {length_val} {from_len_code} → cm:\n"
                    f"   {length_val} × {length_factor_cm[from_len_code]} = {in_cm} cm\n"
                    f"2. Convert cm → {to_len_code}:\n"
                    f"   {in_cm} ÷ {length_factor_cm[to_len_code]} = {round_num(res_len)} {to_len_code}"
                )
                st.markdown("#### Steps")
                st.code(step_text, language="text")

            add_to_history("Length", length_val, from_len_code, to_len_code, res_len)

        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 4: WEIGHT
# =============================================================================
with tab4:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("Weight — kg ⇄ lb")

    weight_units = {
        "Kilogram (kg)": "kg",
        "Pound (lb)": "lb",
    }
    weight_factor_kg = {
        "kg": 1.0,
        "lb": 0.45359237,
    }

    col1, _ = st.columns([2, 1])
    with col1:
        weight_val = st.number_input("Weight", value=70.0, step=0.5)

    w_labels = list(weight_units.keys())
    col3, col4 = st.columns(2)
    with col3:
        from_w_label = st.selectbox(
            "From",
            w_labels,
            index=w_labels.index(st.session_state.w_from),
            key="w_from_widget",
        )
    with col4:
        to_w_label = st.selectbox(
            "To",
            w_labels,
            index=w_labels.index(st.session_state.w_to),
            key="w_to_widget",
        )

    st.session_state.w_from = from_w_label
    st.session_state.w_to = to_w_label

    if st.button("Swap units ⇄", key="swap_weight"):
        st.session_state.w_from, st.session_state.w_to = (
            st.session_state.w_to,
            st.session_state.w_from,
        )

    from_w_label = st.session_state.w_from
    to_w_label = st.session_state.w_to

    from_w_code = weight_units[from_w_label]
    to_w_code = weight_units[to_w_label]

    if from_w_code == to_w_code:
        st.warning("Choose different units to convert.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Convert ⚖️", key="convert_weight"):
            in_kg = weight_val * weight_factor_kg[from_w_code]
            res_w = in_kg / weight_factor_kg[to_w_code]

            st.markdown(
                f'<div class="result-badge">Result: {round_num(res_w)} {to_w_code}</div>',
                unsafe_allow_html=True,
            )

            if show_steps:
                step_text = (
                    f"1. Convert {weight_val} {from_w_code} → kg:\n"
                    f"   {weight_val} × {weight_factor_kg[from_w_code]} = {in_kg} kg\n"
                    f"2. Convert kg → {to_w_code}:\n"
                    f"   {in_kg} ÷ {weight_factor_kg[to_w_code]} = {round_num(res_w)} {to_w_code}"
                )
                st.markdown("#### Steps")
                st.code(step_text, language="text")

            add_to_history("Weight", weight_val, from_w_code, to_w_code, res_w)

        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 5: BULK MODE  (unchanged from earlier)
# =============================================================================
with tab5:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("Bulk Mode — Convert Multiple Values")

    mode = st.selectbox("Category", ["Currency (INR ⇄ USD)", "Temperature", "Length", "Weight"])

    # same factors as above
    length_factor_cm = {"cm": 1.0, "m": 100.0, "in": 2.54, "ft": 30.48}
    weight_factor_kg = {"kg": 1.0, "lb": 0.45359237}

    if mode.startswith("Currency"):
        from_u = st.selectbox("From unit", ["INR", "USD"], key="bulk_cur_from")
        to_u = "USD" if from_u == "INR" else "INR"
        st.write(f"To unit: **{to_u}** (auto-selected)")
    elif mode == "Temperature":
        from_u = st.selectbox("From unit", ["C", "F"], key="bulk_temp_from")
        to_u = "F" if from_u == "C" else "C"
        st.write(f"To unit: **{to_u}** (auto-selected)")
    elif mode == "Length":
        from_u = st.selectbox("From unit", ["cm", "m", "in", "ft"], key="bulk_len_from")
        to_u = st.selectbox("To unit", ["cm", "m", "in", "ft"], index=2, key="bulk_len_to")
        if from_u == to_u:
            st.warning("For bulk length conversion, choose different units.")
    else:
        from_u = st.selectbox("From unit", ["kg", "lb"], key="bulk_w_from")
        to_u = "lb" if from_u == "kg" else "kg"
        st.write(f"To unit: **{to_u}** (auto-selected)")

    st.markdown("#### Paste numbers (one per line)")
    raw_text = st.text_area(
        "Values",
        placeholder="Example:\n10\n25.5\n100\n...",
        height=150,
    )

    def parse_lines(text):
        lines = text.splitlines()
        values = []
        errors = []
        for i, line in enumerate(lines, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                values.append(float(s))
            except ValueError:
                errors.append(f"Line {i}: '{s}' is not a valid number.")
        return values, errors

    if st.button("Convert List 📊", key="bulk_convert"):
        values, errs = parse_lines(raw_text)
        if errs:
            st.error("Some lines could not be parsed:")
            for e in errs:
                st.write(f"- {e}")

        if not values:
            st.info("No valid numbers to convert.")
        else:
            results = []
            if mode.startswith("Currency"):
                for v in values:
                    if from_u == "INR":
                        r = v / fx_rate
                    else:
                        r = v * fx_rate
                    results.append(r)
            elif mode == "Temperature":
                for v in values:
                    if from_u == "C":
                        r = (v * 9 / 5) + 32
                    else:
                        r = (v - 32) * 5 / 9
                    results.append(r)
            elif mode == "Length":
                for v in values:
                    in_cm = v * length_factor_cm[from_u]
                    r = in_cm / length_factor_cm[to_u]
                    results.append(r)
            else:
                for v in values:
                    in_kg = v * weight_factor_kg[from_u]
                    r = in_kg / weight_factor_kg[to_u]
                    results.append(r)

            df = pd.DataFrame(
                {
                    f"Input ({from_u})": values,
                    f"Output ({to_u})": [round_num(x) for x in results],
                }
            )
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv,
                file_name="bulk_conversion.csv",
                mime="text/csv",
            )

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# HISTORY SECTION
# =============================================================================
if st.session_state["history"]:
    st.markdown("### 🕒 Recent conversions")
    for item in reversed(st.session_state["history"]):
        st.markdown(
            f"- **{item['Category']}**: {item['Input']} → `{item['Output']}`"
            + (f"  \n  _{item['Details']}_" if item["Details"] else "")
        )
