import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json
import uuid

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Expense Split Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# DARK UI (ALL TEXT WHITE)
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

/* Hide Streamlit bits */
#MainMenu, footer, header { visibility: hidden; }

/* Dark background */
.stApp {
  background:
    radial-gradient(1200px circle at 8% 10%, rgba(102,126,234,0.12), transparent 45%),
    radial-gradient(1100px circle at 92% 15%, rgba(118,75,162,0.14), transparent 40%),
    linear-gradient(180deg, #0B0F1A 0%, #0B0F1A 60%);
}

/* Make ALL text white */
html, body, [data-testid="stAppViewContainer"], p, span, div, label, small,
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
  color: #ffffff !important;
}
strong, b { color: #ffffff !important; }

/* Headings */
h1, h2, h3, h4 { color: #ffffff !important; font-weight: 800 !important; }
h1 {
  font-size: 2rem !important;
  background: linear-gradient(135deg, #7aa2ff 0%, #b892ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Layout spacing */
.main .block-container { max-width: 1500px; padding: 16px !important; }

/* Glass cards */
.glass {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 16px;
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
  padding: 16px 16px;
}

/* Nav */
.nav-card { padding: 12px; position: sticky; top: 12px; }
.nav-title {
  font-weight: 800; letter-spacing: -0.3px; margin-bottom: 8px; font-size: 1.1rem;
  background: linear-gradient(135deg, #7aa2ff 0%, #b892ff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
div[data-testid="stRadio"] > label { display: none; }
.stRadio > div { row-gap: 6px; }
.stRadio [role="radiogroup"] > div {
  padding: 10px 12px; border-radius: 12px; border: 1.5px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.03); transition: .18s ease;
}
.stRadio [role="radiogroup"] > div:hover {
  border-color: rgba(122,162,255,.45); box-shadow: 0 6px 14px rgba(122,162,255,.22);
}
.stRadio [aria-checked="true"] {
  border-color: rgba(122,162,255,.85) !important; background: rgba(122,162,255,.08);
}

/* Inputs */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stDateInput>div>div>input {
  background: rgba(255,255,255,.06) !important;
  color: #ffffff !important;
  border: 2px solid rgba(255,255,255,.14) !important;
  border-radius: 12px !important;
  padding: 10px 12px !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder { color: #e5e7eb !important; opacity: .8 !important; }

.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stDateInput>div>div>input:focus {
  border-color: #7aa2ff !important;
  box-shadow: 0 0 0 3px rgba(122,162,255,0.25) !important;
}

/* Selects */
.stSelectbox>div>div {
  background: rgba(255,255,255,.06) !important;
  border: 2px solid rgba(255,255,255,.14) !important;
  border-radius: 12px !important;
}
.stSelectbox>div>div>div { color: #ffffff !important; }
.stSelectbox svg { fill: #ffffff !important; color:#ffffff !important; }
.stSelectbox [role="listbox"] {
  background: #0f1525 !important;
  color: #ffffff !important;
  border: 2px solid rgba(255,255,255,.14) !important;
  border-radius: 12px !important;
}
.stSelectbox [role="option"] {
  color: #ffffff !important; background: #0f1525 !important; font-weight: 600 !important;
}
.stSelectbox [role="option"]:hover { background: #18203a !important; color: #ffffff !important; }

/* Calendar */
[data-baseweb="calendar"] {
  background: #0f1525 !important;
  border: 2px solid rgba(255,255,255,.14) !important;
  border-radius: 12px !important;
}
[data-baseweb="calendar"] button { color: #ffffff !important; background: #0f1525 !important; }
[data-baseweb="calendar"] [aria-selected="true"] { background: #7aa2ff !important; color: #0b0f1a !important; }

/* Buttons */
.stButton>button, .stDownloadButton>button {
  color: #0b0f1a !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 11px 18px !important;
  font-weight: 800 !important;
  letter-spacing: .3px;
  font-size: .82rem !important;
  text-transform: uppercase;
}
.stButton>button {
  background: linear-gradient(135deg, #7aa2ff 0%, #b892ff 100%) !important;
  box-shadow: 0 10px 22px rgba(122,162,255,.35) !important;
}
.stButton>button:hover { filter: brightness(1.06); }
.stDownloadButton>button {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
  box-shadow: 0 10px 22px rgba(34,197,94,.35) !important;
}

/* Metrics */
div[data-testid="stMetricValue"] {
  font-size: 1.55rem; font-weight: 800;
  background: linear-gradient(135deg, #7aa2ff 0%, #b892ff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* Cards */
.expense-card {
  background: rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.12);
  border-radius:12px; padding:12px 14px;
  box-shadow:0 2px 8px rgba(0,0,0,.35); margin-bottom:10px;
}
.balance-positive { color:#34d399 !important; font-weight:800; }
.balance-negative { color:#f87171 !important; font-weight:800; }

/* Scroll areas */
.pane { max-height: 520px; overflow: auto; padding-right: 4px; }
.pane-tall { max-height: 620px; overflow: auto; padding-right: 4px; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# STATE INIT
# =============================================================================
if "members" not in st.session_state: st.session_state.members = []  # [{id, name, upi}]
if "member_seq" not in st.session_state: st.session_state.member_seq = 0  # monotonic
if "expenses" not in st.session_state: st.session_state.expenses = []  # [{...}]
if "split_type" not in st.session_state: st.session_state.split_type = "Equal"
if "active_view" not in st.session_state: st.session_state.active_view = "📊 Dashboard"
if "show_success" not in st.session_state: st.session_state.show_success = False
if "success_message" not in st.session_state: st.session_state.success_message = ""
if "edit_expense_id" not in st.session_state: st.session_state.edit_expense_id = None

def next_member_id():
    st.session_state.member_seq += 1
    return st.session_state.member_seq

def member_map():
    return {m["id"]: m for m in st.session_state.members}

def get_member_name(member_id):
    mm = member_map()
    return mm.get(member_id, {}).get("name", "Unknown")

# =============================================================================
# CORE LOGIC
# =============================================================================
def calculate_balances():
    mm_ids = {m["id"] for m in st.session_state.members}
    balances = {mid: 0.0 for mid in mm_ids}
    for e in st.session_state.expenses:
        if e["payer"] in mm_ids:
            balances[e["payer"]] += e["amount"]
        for mid, amount in e["splits"].items():
            try:
                mi = int(mid)
            except:
                mi = mid
            if mi in mm_ids:
                balances[mi] -= amount
    return balances

def calculate_settlements():
    balances = calculate_balances()
    creditors = [(mid, bal) for mid, bal in balances.items() if bal > 0.01]
    debtors = [(mid, abs(bal)) for mid, bal in balances.items() if bal < -0.01]
    if not creditors or not debtors: return []
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
    settlements, i, j = [], 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor_id, credit_amount = creditors[i]
        debtor_id, debt_amount = debtors[j]
        amount = round(min(credit_amount, debt_amount), 2)
        creditor_name = get_member_name(creditor_id)
        debtor_name = get_member_name(debtor_id)
        settlements.append({"from_id": debtor_id, "to_id": creditor_id, "from": debtor_name, "to": creditor_name, "amount": amount})
        creditors[i] = (creditor_id, round(credit_amount - amount, 2))
        debtors[j] = (debtor_id, round(debt_amount - amount, 2))
        if creditors[i][1] < 0.01: i += 1
        if debtors[j][1] < 0.01: j += 1
    return settlements

def export_to_excel():
    if not st.session_state.expenses: return None
    tx_rows = []
    for e in st.session_state.expenses:
        payer = get_member_name(e["payer"])
        participants, split_details = [], []
        for mid, amt in e["splits"].items():
            name = get_member_name(int(mid))
            participants.append(name)
            split_details.append(f"{name}: ₹{amt:.2f}")
        tx_rows.append({
            "Date": e["date"],
            "Description": e["description"],
            "Category": e["category"],
            "Total Amount": f"₹{e['amount']:.2f}",
            "Paid By": payer,
            "Participants": ", ".join(participants),
            "Split Details": " | ".join(split_details),
            "Split Type": e.get("split_type",""),
        })
    df_tx = pd.DataFrame(tx_rows)

    bals = calculate_balances()
    bal_rows = []
    for m in st.session_state.members:
        bal = bals.get(m["id"], 0.0)
        status = "Gets Back" if bal > 0.01 else "Owes" if bal < -0.01 else "Settled"
        bal_rows.append({"Member Name": m["name"], "Balance Amount": f"₹{abs(bal):.2f}", "Status": status})
    df_bal = pd.DataFrame(bal_rows)

    sets = calculate_settlements()
    df_set = pd.DataFrame([{"Transaction #": i+1, "From": s["from"], "To": s["to"], "Amount": f"₹{s['amount']:.2f}"} for i, s in enumerate(sets)])

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_tx.to_excel(writer, sheet_name="Transactions", index=False)
        df_bal.to_excel(writer, sheet_name="Balances", index=False)
        if not df_set.empty:
            df_set.to_excel(writer, sheet_name="Settlements", index=False)
        for sheet in writer.sheets.values():
            for column in sheet.columns:
                max_len = 0
                col_letter = column[0].column_letter
                for cell in column:
                    try: max_len = max(max_len, len(str(cell.value)))
                    except: pass
                sheet.column_dimensions[col_letter].width = min(max_len + 2, 50)
    output.seek(0)
    return output

def export_state_json():
    data = {
        "members": st.session_state.members,
        "member_seq": st.session_state.member_seq,
        "expenses": st.session_state.expenses
    }
    return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

def import_state_json(file_bytes: bytes):
    try:
        data = json.loads(file_bytes.decode("utf-8"))
        st.session_state.members = data.get("members", [])
        st.session_state.member_seq = data.get("member_seq", len(st.session_state.members))
        st.session_state.expenses = data.get("expenses", [])
        st.session_state.show_success = True
        st.session_state.success_message = "✅ Data imported."
        st.rerun()
    except Exception as e:
        st.error(f"Import failed: {e}")

# =============================================================================
# CHARTS (dark theme, white fonts)
# =============================================================================
def create_category_chart():
    if not st.session_state.expenses: return None
    category_data = {}
    for e in st.session_state.expenses:
        category_data[e["category"]] = category_data.get(e["category"], 0) + e["amount"]
    df = pd.DataFrame(list(category_data.items()), columns=["Category", "Amount"])
    if df.empty: return None
    fig = px.pie(
        df, values="Amount", names="Category",
        color_discrete_sequence=["#7aa2ff", "#b892ff", "#f093fb", "#4facfe", "#00f2fe", "#43e97b"]
    )
    fig.update_traces(
        textposition="inside", textinfo="percent+label",
        textfont=dict(size=13, color="white", family="Inter"),
        marker=dict(line=dict(color="#0b0f1a", width=2))
    )
    fig.update_layout(
        height=320, margin=dict(t=36,b=10,l=10,r=10), showlegend=True,
        paper_bgcolor="#0b0f1a", plot_bgcolor="#0b0f1a",
        title=dict(text="<b>By Category</b>", font=dict(size=16, color="#ffffff")),
        legend=dict(font=dict(size=12, color="#ffffff", family="Inter")),
        font=dict(color="#ffffff", family="Inter", size=12)
    )
    return fig

def create_member_share_chart():
    if not st.session_state.expenses: return None
    member_spending = {m["name"]: 0 for m in st.session_state.members}
    for e in st.session_state.expenses:
        for mid, amt in e["splits"].items():
            member_spending[get_member_name(int(mid))] += amt
    df = pd.DataFrame(list(member_spending.items()), columns=["Member", "Share"])
    if df.empty: return None
    fig = px.bar(
        df, x="Member", y="Share", color="Share",
        color_continuous_scale=["#7aa2ff", "#b892ff"]
    )
    fig.update_layout(
        height=320, margin=dict(t=36,b=10,l=10,r=10), showlegend=False,
        paper_bgcolor="#0b0f1a", plot_bgcolor="#0b0f1a",
        title=dict(text="<b>Share per Member</b>", font=dict(size=16, color="#ffffff")),
        font=dict(color="#ffffff", family="Inter", size=12),
        xaxis=dict(
            title=dict(text="Member", font=dict(color="#ffffff")),
            tickfont=dict(color="#ffffff"),
            gridcolor="rgba(255,255,255,.1)"
        ),
        yaxis=dict(
            title=dict(text="Amount", font=dict(color="#ffffff")),
            tickfont=dict(color="#ffffff"),
            gridcolor="rgba(255,255,255,.1)"
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Share", font=dict(color="#ffffff")),
            tickfont=dict(color="#ffffff")
        )
    )
    fig.update_traces(marker_line_color="#0b0f1a", marker_line_width=1.2)
    return fig

def create_balance_doughnut():
    if not st.session_state.members or not st.session_state.expenses: return None
    bals = calculate_balances()
    rows = []
    for m in st.session_state.members:
        bal = bals.get(m["id"], 0.0)
        status = "Owes" if bal < -0.01 else "Gets Back" if bal > 0.01 else "Settled"
        if abs(bal) > 0.01:
            rows.append({"Member": m["name"], "Amount": abs(bal), "Status": status})
    df = pd.DataFrame(rows)
    if df.empty: return None
    fig = go.Figure(data=[go.Pie(
        labels=df["Member"] + " (" + df["Status"] + ")", values=df["Amount"], hole=.45,
        marker=dict(colors=["#7aa2ff","#b892ff","#f093fb","#4facfe","#00f2fe","#43e97b"],
                    line=dict(color="#0b0f1a", width=2)),
        textfont=dict(size=13, color="white", family="Inter")
    )])
    fig.update_layout(
        height=320, margin=dict(t=36,b=10,l=10,r=10),
        paper_bgcolor="#0b0f1a", plot_bgcolor="#0b0f1a",
        title=dict(text="<b>Balance Distribution</b>", font=dict(size=16, color="#ffffff")),
        legend=dict(font=dict(size=12, color="#ffffff", family="Inter")),
        font=dict(color="#ffffff", family="Inter", size=12)
    )
    return fig

# =============================================================================
# CONSTANTS
# =============================================================================
CATEGORY_OPTIONS = [
    ("🍔 Food","Food"), ("✈️ Travel","Travel"), ("💡 Utilities","Utilities"),
    ("🎬 Entertainment","Entertainment"), ("🛍️ Shopping","Shopping"), ("📌 Other","Other")
]
FILTER_CATEGORIES = ["All"] + [c[1] for c in CATEGORY_OPTIONS]

# =============================================================================
# HEADER
# =============================================================================
st.markdown("<h1>💰 Expense Split Tracker</h1>", unsafe_allow_html=True)
st.caption("Split expenses with zero drama — clean, quick, accurate.")

if st.session_state.show_success:
    st.success(st.session_state.success_message)
    st.session_state.show_success = False

# =============================================================================
# LAYOUT
# =============================================================================
nav, content = st.columns([0.22, 0.78], gap="large")

with nav:
    st.markdown('<div class="glass nav-card">', unsafe_allow_html=True)
    st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
    selected = st.radio(
        "Navigate",
        ["📊 Dashboard", "👥 Members", "➕ Add Expense", "📋 View & Edit", "💰 Balances", "🔄 Settle Up"],
        index=["📊 Dashboard","👥 Members","➕ Add Expense","📋 View & Edit","💰 Balances","🔄 Settle Up"].index(st.session_state.active_view),
    )
    st.session_state.active_view = selected

    st.divider()
    st.markdown("**Backup & Restore**")
    colx, coly = st.columns(2)
    with colx:
        json_bytes = export_state_json()
        st.download_button("⬇️ Export JSON", data=json_bytes, file_name=f"expense_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json")
    with coly:
        up = st.file_uploader("Import JSON", type=["json"], label_visibility="collapsed")
        if up is not None:
            import_state_json(up.read())

    st.markdown("</div>", unsafe_allow_html=True)

with content:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    # ------------------ DASHBOARD ------------------
    if st.session_state.active_view == "📊 Dashboard":
        top = st.container()
        with top:
            c1, c2, c3, c4 = st.columns([0.25,0.25,0.25,0.25])
            total = sum(e["amount"] for e in st.session_state.expenses)
            with c1: st.metric("Total Expenses", f"₹{total:.2f}")
            with c2: st.metric("Members", len(st.session_state.members))
            with c3: st.metric("Transactions", len(st.session_state.expenses))
            with c4:
                excel = export_to_excel()
                if excel:
                    st.download_button(
                        "📥 Export Excel",
                        data=excel,
                        file_name=f"expense_tracker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        if st.session_state.expenses and st.session_state.members:
            colA, colB, colC = st.columns([0.34, 0.33, 0.33])
            with colA:
                fig = create_category_chart()
                if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with colB:
                fig = create_balance_doughnut()
                if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with colC:
                fig = create_member_share_chart()
                if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("#### Recent")
        st.markdown('<div class="pane">', unsafe_allow_html=True)
        if st.session_state.expenses:
            for e in list(reversed(st.session_state.expenses[-8:])):
                payer = get_member_name(e["payer"])
                participants = [get_member_name(int(mid)) for mid in e["splits"].keys()]
                st.markdown(
                    f"""
                    <div class="expense-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                                <div style="font-weight:800;color:#fff">{e['description']}</div>
                                <div style="font-size:.85rem;color:#e5e7eb">{e['category']} • {e['date']} • Paid by {payer}</div>
                                <div style="font-size:.85rem;color:#d1d5db">Split: {', '.join(participants)}</div>
                            </div>
                            <div style="font-weight:800;color:#7aa2ff;font-size:1.1rem">₹{e['amount']:.2f}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No expenses yet. Add your first expense!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ MEMBERS ------------------
    elif st.session_state.active_view == "👥 Members":
        st.markdown("### Add Member")
        with st.form("add_member", clear_on_submit=True):
            c1, c2, c3 = st.columns([0.5, 0.3, 0.2])
            with c1:
                name = st.text_input("Member Name", placeholder="Enter name")
            with c2:
                upi = st.text_input("UPI ID (optional)", placeholder="name@bank")
            with c3:
                submitted = st.form_submit_button("➕ Add", use_container_width=True)
            if submitted:
                if name.strip():
                    if any(m["name"].strip().lower()==name.strip().lower() for m in st.session_state.members):
                        st.error("Member already exists.")
                    else:
                        st.session_state.members.append({"id": next_member_id(), "name": name.strip(), "upi": upi.strip() if upi.strip() else ""})
                        st.session_state.show_success = True
                        st.session_state.success_message = f"✅ Member '{name}' added!"
                        st.rerun()
                else:
                    st.error("Please enter a name.")
        st.markdown("### Members")
        st.markdown('<div class="pane">', unsafe_allow_html=True)
        if st.session_state.members:
            used_ids = {e["payer"] for e in st.session_state.expenses} | {int(k) for e in st.session_state.expenses for k in e["splits"].keys()}
            for m in st.session_state.members:
                col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
                with col1: st.markdown(f"**{m['name']}**  {'• ' + m['upi'] if m.get('upi') else ''}")
                with col2:
                    new_upi = st.text_input("Update UPI", value=m.get("upi",""), key=f"upi_{m['id']}", label_visibility="collapsed")
                with col3:
                    if m["id"] in used_ids:
                        st.button("🔒 In use", disabled=True, key=f"lock_{m['id']}", use_container_width=True)
                    else:
                        if st.button("🗑️ Remove", key=f"remove_{m['id']}", use_container_width=True):
                            st.session_state.members = [x for x in st.session_state.members if x["id"] != m["id"]]
                            st.rerun()
                if new_upi != m.get("upi",""):
                    m["upi"] = new_upi
        else:
            st.info("No members yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ ADD EXPENSE ------------------
    elif st.session_state.active_view == "➕ Add Expense":
        st.markdown("### Add Expense")
        if not st.session_state.members:
            st.warning("Add members first.")
        else:
            desc = st.text_input("Description", placeholder="e.g., Dinner at Little Italy")
            c1, c2, c3 = st.columns([0.33,0.33,0.34])
            with c1:
                amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
            with c2:
                cat_choice = st.selectbox("Category", CATEGORY_OPTIONS, format_func=lambda x: x[0])
                category = cat_choice[1]
            with c3:
                date_val = st.date_input("Date", value=date.today())

            payer = st.selectbox("Paid By", options=[m["id"] for m in st.session_state.members], format_func=lambda x: get_member_name(x))
            st.session_state.split_type = st.radio("Split Type", ["Equal","Custom","Percentage"], horizontal=True)

            selected = {}
            if st.session_state.split_type == "Equal":
                cols = st.columns(3)
                for i, m in enumerate(st.session_state.members):
                    with cols[i % 3]:
                        if st.checkbox(m["name"], True, key=f"eq_add_{m['id']}"):
                            selected[m["id"]] = None

            elif st.session_state.split_type == "Custom":
                cols = st.columns(2)
                for i, m in enumerate(st.session_state.members):
                    with cols[i % 2]:
                        include = st.checkbox(m["name"], True, key=f"cu_on_add_{m['id']}")
                        if include:
                            amt_i = st.number_input("Amount", min_value=0.0, step=0.01, key=f"cu_amt_add_{m['id']}", label_visibility="collapsed")
                            selected[m["id"]] = amt_i

            elif st.session_state.split_type == "Percentage":
                cols = st.columns(2)
                for i, m in enumerate(st.session_state.members):
                    with cols[i % 2]:
                        include = st.checkbox(m["name"], True, key=f"pr_on_add_{m['id']}")
                        if include:
                            pct_i = st.number_input("Percent", min_value=0.0, max_value=100.0, step=0.01, key=f"pr_pct_add_{m['id']}", label_visibility="collapsed")
                            selected[m["id"]] = pct_i

            if st.button("✅ Add Expense", use_container_width=True):
                if not desc or amount <= 0:
                    st.error("Fill all required fields.")
                elif not selected:
                    st.error("Select at least one participant.")
                else:
                    final_splits = {}
                    if st.session_state.split_type == "Equal":
                        mids = list(selected.keys())
                        base = round(amount / len(mids), 2)
                        final_splits = {mid: base for mid in mids}
                        diff = round(amount - sum(final_splits.values()), 2)
                        final_splits[mids[-1]] += diff
                    elif st.session_state.split_type == "Custom":
                        total = round(sum(selected.values()), 2)
                        if abs(total - amount) > 0.05:
                            st.error(f"Custom amounts must add up to ₹{amount:.2f}. (Now: ₹{total:.2f})"); st.stop()
                        final_splits = {mid: round(v,2) for mid, v in selected.items()}
                    else:
                        total_pct = round(sum(selected.values()), 4)
                        if abs(total_pct - 100.0) > 0.05:
                            st.error("Percentages must add up to ~100%."); st.stop()
                        for mid, pct in selected.items():
                            final_splits[mid] = round((amount * pct) / 100.0, 2)
                        diff = round(amount - sum(final_splits.values()), 2)
                        last = next(reversed(final_splits))
                        final_splits[last] += diff

                    st.session_state.expenses.append({
                        "id": str(uuid.uuid4()),
                        "description": desc.strip(),
                        "amount": round(amount, 2),
                        "category": category,
                        "date": date_val.strftime("%Y-%m-%d"),
                        "payer": payer,
                        "splits": final_splits,
                        "split_type": st.session_state.split_type
                    })
                    st.session_state.show_success = True
                    st.session_state.success_message = f"✅ Expense '{desc}' of ₹{amount:.2f} added!"
                    st.rerun()

    # ------------------ VIEW & EDIT ------------------
    elif st.session_state.active_view == "📋 View & Edit":
        st.markdown("### All Expenses")
        if st.session_state.expenses:
            f1, f2, f3 = st.columns([0.35,0.35,0.30])
            with f1:
                filter_category = st.selectbox("Category", FILTER_CATEGORIES, index=0)
            with f2:
                dr = st.date_input("Date range", value=(date(2000,1,1), date.today()))
            with f3:
                q = st.text_input("Search description", placeholder="Type to search...")

            filtered = []
            dmin, dmax = dr if isinstance(dr, tuple) else (date(2000,1,1), date.today())
            for e in st.session_state.expenses:
                in_cat = (filter_category=="All" or e["category"]==filter_category)
                d = datetime.strptime(e["date"], "%Y-%m-%d").date()
                in_range = (dmin <= d <= dmax)
                in_search = (q.strip().lower() in e["description"].lower()) if q.strip() else True
                if in_cat and in_range and in_search:
                    filtered.append(e)

            st.markdown("##### Select items to delete or edit")
            selections = {}
            st.markdown('<div class="pane-tall">', unsafe_allow_html=True)
            for e in sorted(filtered, key=lambda x: x["date"], reverse=True):
                row = st.columns([0.08, 0.62, 0.15, 0.15])
                with row[0]:
                    selections[e["id"]] = st.checkbox("", key=f"view_sel_{e['id']}")
                with row[1]:
                    payer = get_member_name(e["payer"])
                    st.markdown(
                        f"""
                        <div class="expense-card">
                            <div><b>{e['description']}</b> — {e['category']}</div>
                            <small>{e['date']} • Paid by {payer}</small>
                        </div>
                        """, unsafe_allow_html=True
                    )
                with row[2]:
                    st.markdown(f"<div style='margin-top:10px;font-weight:800;color:#7aa2ff'>₹{e['amount']:.2f}</div>", unsafe_allow_html=True)
                with row[3]:
                    if st.button("✏️ Edit", key=f"edit_{e['id']}", use_container_width=True):
                        st.session_state.edit_expense_id = e["id"]
            st.markdown("</div>", unsafe_allow_html=True)

            colA, colB = st.columns([0.5,0.5])
            with colA:
                if st.button("🗑️ Delete Selected", use_container_width=True):
                    ids_to_delete = {eid for eid, checked in selections.items() if checked}
                    if ids_to_delete:
                        st.session_state.expenses = [e for e in st.session_state.expenses if e["id"] not in ids_to_delete]
                        st.session_state.show_success = True
                        st.session_state.success_message = f"🧹 Deleted {len(ids_to_delete)} item(s)."
                        st.rerun()
                    else:
                        st.info("No items selected.")
            with colB:
                if st.button("Clear Filters", use_container_width=True):
                    st.rerun()

            if st.session_state.edit_expense_id:
                st.divider()
                st.markdown("### Edit Expense")
                exp = next((x for x in st.session_state.expenses if x["id"]==st.session_state.edit_expense_id), None)
                if exp:
                    with st.form("edit_form", clear_on_submit=False):
                        d1, d2, d3 = st.columns([0.42,0.28,0.30])
                        with d1:
                            new_desc = st.text_input("Description", value=exp["description"])
                        with d2:
                            new_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, value=float(exp["amount"]), format="%.2f")
                        with d3:
                            cat_idx = next((i for i, c in enumerate(CATEGORY_OPTIONS) if c[1]==exp["category"]), 0)
                            new_cat = st.selectbox("Category", CATEGORY_OPTIONS, index=cat_idx, format_func=lambda x: x[0])

                        e1, e2 = st.columns([0.5,0.5])
                        with e1:
                            new_date = st.date_input("Date", value=datetime.strptime(exp["date"], "%Y-%m-%d"))
                        with e2:
                            all_ids = [m["id"] for m in st.session_state.members]
                            default_idx = all_ids.index(exp["payer"]) if exp["payer"] in all_ids else 0
                            new_payer = st.selectbox("Paid By", options=all_ids, index=default_idx, format_func=lambda x: get_member_name(x))

                        split_mode = st.radio("Split Type", ["Equal","Custom","Percentage"], index=["Equal","Custom","Percentage"].index(exp.get("split_type","Equal")), horizontal=True)

                        new_selected = {}
                        if split_mode == "Equal":
                            cols = st.columns(3)
                            existing_ids = set(int(k) for k in exp["splits"].keys())
                            for i, m in enumerate(st.session_state.members):
                                with cols[i % 3]:
                                    checked = m["id"] in existing_ids
                                    if st.checkbox(m["name"], checked, key=f"eq_edit_{exp['id']}_{m['id']}"):
                                        new_selected[m["id"]] = None

                        elif split_mode == "Custom":
                            cols = st.columns(2)
                            ex = {int(k): v for k, v in exp["splits"].items()}
                            for i, m in enumerate(st.session_state.members):
                                with cols[i % 2]:
                                    include = m["id"] in ex
                                    include = st.checkbox(m["name"], include, key=f"cu_on_edit_{exp['id']}_{m['id']}")
                                    if include:
                                        amt_i = st.number_input("Amount", min_value=0.0, step=0.01,
                                                                value=float(ex.get(m["id"], 0.0)),
                                                                key=f"cu_amt_edit_{exp['id']}_{m['id']}",
                                                                label_visibility="collapsed")
                                        new_selected[m["id"]] = amt_i

                        elif split_mode == "Percentage":
                            cols = st.columns(2)
                            total_amt = float(exp["amount"])
                            ex = {int(k): round((v/total_amt*100.0), 4) if total_amt>0 else 0.0 for k, v in exp["splits"].items()}
                            for i, m in enumerate(st.session_state.members):
                                with cols[i % 2]:
                                    include = m["id"] in ex
                                    include = st.checkbox(m["name"], include, key=f"pr_on_edit_{exp['id']}_{m['id']}")
                                    if include:
                                        pct_i = st.number_input("Percent", min_value=0.0, max_value=100.0, step=0.01,
                                                                value=float(ex.get(m["id"], 0.0)),
                                                                key=f"pr_pct_edit_{exp['id']}_{m['id']}",
                                                                label_visibility="collapsed")
                                        new_selected[m["id"]] = pct_i

                        left, right = st.columns([0.5,0.5])
                        with left:
                            save_btn = st.form_submit_button("💾 Save Changes", use_container_width=True)
                        with right:
                            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)

                    if cancel_btn:
                        st.session_state.edit_expense_id = None
                        st.rerun()

                    if save_btn:
                        if not new_desc or new_amount <= 0:
                            st.error("Fill all required fields.")
                        elif not new_selected:
                            st.error("Select at least one participant.")
                        else:
                            final_splits = {}
                            if split_mode == "Equal":
                                mids = list(new_selected.keys())
                                base = round(new_amount / len(mids), 2)
                                final_splits = {mid: base for mid in mids}
                                diff = round(new_amount - sum(final_splits.values()), 2)
                                final_splits[mids[-1]] += diff
                            elif split_mode == "Custom":
                                total = round(sum(new_selected.values()), 2)
                                if abs(total - new_amount) > 0.05:
                                    st.error(f"Custom amounts must add up to ₹{new_amount:.2f}. (Now: ₹{total:.2f})"); st.stop()
                                final_splits = {mid: round(v,2) for mid, v in new_selected.items()}
                            else:
                                total_pct = round(sum(new_selected.values()), 3)
                                if abs(total_pct - 100.0) > 0.05:
                                    st.error("Percentages must add up to ~100%."); st.stop()
                                for mid, pct in new_selected.items():
                                    final_splits[mid] = round((new_amount * pct) / 100.0, 2)
                                diff = round(new_amount - sum(final_splits.values()), 2)
                                last = next(reversed(final_splits))
                                final_splits[last] += diff

                            exp.update({
                                "description": new_desc.strip(),
                                "amount": round(float(new_amount), 2),
                                "category": new_cat[1],
                                "date": new_date.strftime("%Y-%m-%d"),
                                "payer": new_payer,
                                "splits": final_splits,
                                "split_type": split_mode
                            })
                            st.session_state.edit_expense_id = None
                            st.session_state.show_success = True
                            st.session_state.success_message = "✅ Expense updated."
                            st.rerun()
                else:
                    st.info("Pick an expense to edit.")
        else:
            st.info("No expenses yet.")

    # ------------------ BALANCES ------------------
    elif st.session_state.active_view == "💰 Balances":
        st.markdown("### Member Balances")
        if st.session_state.members and st.session_state.expenses:
            balances = calculate_balances()
            st.markdown('<div class="pane">', unsafe_allow_html=True)
            for m in st.session_state.members:
                bal = balances.get(m["id"], 0.0)
                c1, c2 = st.columns([0.7,0.3])
                with c1: st.markdown(f"**{m['name']}**")
                with c2:
                    if bal > 0.01:
                        st.markdown(f'<div class="balance-positive">Gets back ₹{bal:.2f}</div>', unsafe_allow_html=True)
                    elif bal < -0.01:
                        st.markdown(f'<div class="balance-negative">Owes ₹{abs(bal):.2f}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown("✅ Settled")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Add members and expenses to see balances.")

    # ------------------ SETTLE UP ------------------
    elif st.session_state.active_view == "🔄 Settle Up":
        st.markdown("### Settlement Center")
        if st.session_state.members and st.session_state.expenses:
            settlements = calculate_settlements()
            if settlements:
                total_transactions = len(settlements)
                total_amount = sum(s["amount"] for s in settlements)
                c1, c2 = st.columns([0.5,0.5])
                with c1: st.metric("Transactions Needed", total_transactions)
                with c2: st.metric("Total Amount to Transfer", f"₹{total_amount:.2f}")

                st.markdown("#### Smart Plan")
                st.markdown('<div class="pane">', unsafe_allow_html=True)
                m_map = member_map()
                for i, s in enumerate(settlements, 1):
                    to_upi = m_map.get(s["to_id"], {}).get("upi","")
                    upi_link = ""
                    if to_upi:
                        upi_link = f"upi://pay?pa={to_upi}&am={s['amount']:.2f}&tn=Expense%20Split"
                    st.markdown(
                        f"""
                        <div class="expense-card" style="border-left:4px solid #7aa2ff;">
                            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
                                <div><b>#{i}</b> &nbsp; {s['from']} → <b>{s['to']}</b></div>
                                <div style="display:flex;gap:8px;align-items:center;">
                                    <div style="font-weight:800;color:#7aa2ff">₹{s['amount']:.2f}</div>
                                    {'<a href="'+upi_link+'" target="_blank"><button style="padding:6px 10px;border-radius:8px;border:none;background:#22c55e;color:#0b0f1a;font-weight:800;cursor:pointer;">Pay UPI</button></a>' if to_upi else ''}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.success("🎉 Everyone is settled!")
        else:
            st.info("Add members and expenses to see settlement suggestions.")

    st.markdown("</div>", unsafe_allow_html=True)

