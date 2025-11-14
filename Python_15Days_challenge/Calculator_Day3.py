# CLASSY GLASSMORPHIC CALCULATOR WITH FULL KEYBOARD + NUMPAD SUPPORT
import streamlit as st
import math
from collections import deque
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="🧮 Classy Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================
# GLOBAL STYLES – FULL NEW UI
# =========================
st.markdown("""
    <style>
    /* Global background */
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        background: radial-gradient(circle at top, #0b1220 0, #020617 45%, #000 100%);
    }

    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        background: radial-gradient(circle at top, #0b1220 0, #020617 45%, #000 100%);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
    }

    .main {
        padding: 24px 12px !important;
        max-width: 420px !important;
        margin: 0 auto !important;
    }

    .block-container {
        padding: 24px 16px 28px 16px !important;
        max-width: 420px !important;
        margin: 0 auto !important;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Calculator Card */
    .calc-card {
        position: relative;
        width: 100%;
        box-sizing: border-box;
        border-radius: 28px;
        padding: 18px 16px 22px 16px;
        background:
            linear-gradient(135deg, rgba(15,23,42,0.96), rgba(15,23,42,0.85)),
            radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 60%),
            radial-gradient(circle at bottom right, rgba(52,211,153,0.15), transparent 55%);
        box-shadow:
            0 24px 60px rgba(0,0,0,0.9),
            0 0 0 1px rgba(148,163,184,0.12);
        backdrop-filter: blur(26px);
        border: 1px solid rgba(148,163,184,0.35);
    }

    /* Subtle glowing orb */
    .calc-orb {
        position: absolute;
        top: -40px;
        right: -30px;
        width: 90px;
        height: 90px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(56,189,248,0.35), transparent 70%);
        filter: blur(6px);
        opacity: 0.7;
        pointer-events: none;
    }

    /* Fake status pill */
    .status-pill {
        width: 64px;
        height: 6px;
        border-radius: 999px;
        background: linear-gradient(90deg, #4b5563, #9ca3af);
        margin: 0 auto 10px auto;
        opacity: 0.8;
    }

    .calc-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }

    .calc-title {
        font-size: 16px;
        font-weight: 500;
        color: #e5e7eb;
        opacity: 0.9;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    .calc-subtitle {
        font-size: 11px;
        color: #9ca3af;
        opacity: 0.85;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    /* Display area */
    .display-wrap {
        margin-top: 6px;
        margin-bottom: 14px;
        padding: 10px 10px 14px 10px;
        border-radius: 22px;
        background:
            radial-gradient(circle at top, rgba(148,163,184,0.20), transparent 70%),
            linear-gradient(180deg, rgba(15,23,42,0.95), rgba(15,23,42,0.98));
        box-shadow:
            inset 0 0 0 1px rgba(148,163,184,0.18),
            0 14px 28px rgba(15,23,42,0.9);
    }

    .display-expression {
        color: #9ca3af;
        font-size: 14px;
        min-height: 22px;
        max-height: 42px;
        overflow: hidden;
        text-overflow: ellipsis;
        word-wrap: break-word;
        word-break: break-all;
        text-align: right;
        margin-bottom: 4px;
        font-family: "SF Mono", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }

    .display-result {
        color: #e5e7eb;
        font-size: 32px;
        font-weight: 500;
        text-align: right;
        min-height: 32px;
        line-height: 1.1;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
    }

    /* Grid tweaks */
    .stColumns {
        gap: 6px !important;
    }

    .stColumn {
        padding: 0 !important;
    }

    /* Base button style (numbers / normal) */
    .stButton > button {
        height: 56px !important;
        margin: 4px 0 !important;
        padding: 0 !important;
        border-radius: 18px !important;
        border: none !important;
        width: 100% !important;
        cursor: pointer;
        font-size: 19px !important;
        font-weight: 400 !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
        color: #e5e7eb !important;
        background:
            radial-gradient(circle at top, #111827, #020617) !important;
        box-shadow:
            0 10px 18px rgba(0,0,0,0.85),
            0 0 0 1px rgba(31,41,55,0.9);
        transition: all 0.08s ease-out;
    }

    /* Operator / highlight buttons */
    .stButton > button[kind="primary"] {
        background:
            radial-gradient(circle at top, #22c55e, #0f766e) !important;
        color: #ecfdf5 !important;
        box-shadow:
            0 12px 22px rgba(16,185,129,0.55),
            0 0 0 1px rgba(45,212,191,0.75);
    }

    .stButton > button:active {
        transform: scale(0.96) translateY(1px);
        box-shadow:
            0 4px 10px rgba(0,0,0,0.9),
            0 0 0 1px rgba(31,41,55,0.9);
        filter: brightness(0.95);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
    }

    h3 {
        margin: 8px 0 !important;
        font-size: 15px !important;
        color: #e5e7eb !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    p {
        margin: 0 !important;
        font-size: 12px !important;
        color: #cbd5f5 !important;
    }

    hr {
        margin: 10px 0 !important;
        border-color: #1f2933 !important;
    }

    .history-box {
        background: rgba(15,23,42,0.9);
        border-radius: 14px;
        padding: 8px;
        max-height: 100px;
        overflow-y: auto;
        border: 1px solid rgba(55,65,81,0.9);
        box-shadow: 0 10px 26px rgba(0,0,0,0.85);
    }

    .history-item {
        padding: 3px 6px;
        margin: 2px 0;
        background: rgba(30,64,175,0.25);
        border-left: 2px solid #38bdf8;
        font-family: "SF Mono", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 10px;
        border-radius: 4px;
        color: #e5e7eb;
    }

    .stExpander {
        border-radius: 16px !important;
        border: 1px solid rgba(30,64,175,0.7) !important;
        background: radial-gradient(circle at top left, rgba(37,99,235,0.35), rgba(15,23,42,0.98)) !important;
        box-shadow: 0 10px 24px rgba(15,23,42,0.95);
    }

    .st-expanderHeader, .st-expanderHeader p {
        color: #e5e7eb !important;
    }

    .footer-text {
        text-align: center;
        color: #9ca3af;
        margin-top: 8px;
        font-size: 11px;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    .keycaps-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
    }

    .keycap {
        border-radius: 999px;
        padding: 3px 10px;
        border: 1px solid rgba(148,163,184,0.6);
        font-size: 11px;
        color: #e5e7eb;
        background: rgba(15,23,42,0.9);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# JS KEYBOARD HANDLER (with NUMPAD)
# =========================
keyboard_handler = """
<div id="keyboard-listener" style="outline: none; position: absolute; left: -9999px;"></div>
<script>
function handleCalculatorKeyboard(event) {
    const key = event.key;
    const code = event.code;
    let mappedKey = key;

    // Map Numpad keys
    if (code && code.startsWith('Numpad')) {
        const np = code.replace('Numpad', '');
        if (np >= '0' && np <= '9') {
            mappedKey = np;
        } else if (np === 'Add') {
            mappedKey = '+';
        } else if (np === 'Subtract') {
            mappedKey = '-';
        } else if (np === 'Multiply') {
            mappedKey = '*';
        } else if (np === 'Divide') {
            mappedKey = '/';
        } else if (np === 'Decimal') {
            mappedKey = '.';
        } else if (np === 'Enter') {
            mappedKey = 'Enter';
        }
    }

    const buttons = document.querySelectorAll('button');
    let targetBtn = null;

    if (mappedKey >= '0' && mappedKey <= '9') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === mappedKey);
    } else if (mappedKey === '+') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '+');
    } else if (mappedKey === '-' || mappedKey === '−') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '−');
    } else if (mappedKey === '*') {
        event.preventDefault();
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '×');
    } else if (mappedKey === '/') {
        event.preventDefault();
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '÷');
    } else if (mappedKey === '.') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '.');
    } else if (mappedKey === '%') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '%');
    } else if (mappedKey === '^') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '^');
    } else if (mappedKey === '(') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '(');
    } else if (mappedKey === ')') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === ')');
    } else if (mappedKey === 'Enter' || mappedKey === '=') {
        event.preventDefault();
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '=');
    } else if (mappedKey === 'Backspace') {
        event.preventDefault();
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === '←');
    } else if (mappedKey === 'c' || mappedKey === 'C') {
        targetBtn = Array.from(buttons).find(btn => btn.textContent.trim() === 'C');
    }

    if (targetBtn) {
        targetBtn.click();
        targetBtn.style.transform = 'scale(0.96) translateY(1px)';
        setTimeout(() => {
            targetBtn.style.transform = 'scale(1) translateY(0)';
        }, 80);
    }
}

document.addEventListener('keydown', handleCalculatorKeyboard, true);
</script>
"""
components.html(keyboard_handler, height=0)

# =========================
# CALCULATOR LOGIC (same core logic)
# =========================
class Calculator:
    def __init__(self):
        self.operators = "+-*/%^"
        self.priority = {'+': 0, '-': 0, '*': 1, '/': 1, '%': 1, '^': 2}
    
    def tokenize(self, expression):
        tokens = []
        current_number = ""
        
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(float(current_number))
                    current_number = ""
                if char in self.operators or char in '()':
                    tokens.append(char)
                elif char == ' ':
                    continue
        
        if current_number:
            tokens.append(float(current_number))
        
        return tokens
    
    def apply_operator(self, op, operand1, operand2):
        if op == '+':
            return operand1 + operand2
        elif op == '-':
            return operand1 - operand2
        elif op == '*':
            return operand1 * operand2
        elif op == '/':
            if operand2 == 0:
                raise ValueError("÷ by 0")
            return operand1 / operand2
        elif op == '%':
            if operand2 == 0:
                raise ValueError("Mod by 0")
            return operand1 % operand2
        elif op == '^':
            return operand1 ** operand2
        return 0
    
    def evaluate(self, expression):
        if not expression or expression.strip() == "":
            return 0
        
        try:
            tokens = self.tokenize(expression)
            if not tokens:
                return 0
            
            while '(' in tokens:
                start = -1
                for i, token in enumerate(tokens):
                    if token == '(':
                        start = i
                    elif token == ')':
                        inner_expr = tokens[start+1:i]
                        result = self._evaluate_simple(inner_expr)
                        tokens = tokens[:start] + [result] + tokens[i+1:]
                        break
            
            return self._evaluate_simple(tokens)
        
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def _evaluate_simple(self, tokens):
        output = deque()
        operators = deque()
        
        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token in self.operators:
                while (operators and operators[-1] != '(' and 
                       operators[-1] in self.operators and
                       self.priority.get(operators[-1], -1) >= self.priority.get(token, -1)):
                    output.append(operators.pop())
                operators.append(token)
        
        while operators:
            output.append(operators.pop())
        
        stack = deque()
        for token in output:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid")
                b = stack.pop()
                a = stack.pop()
                result = self.apply_operator(token, a, b)
                stack.append(result)
        
        return stack[0] if stack else 0

# =========================
# SESSION STATE
# =========================
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

calculator = Calculator()

# =========================
# MAIN CALCULATOR UI
# =========================
with st.container():
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.markdown('<div class="calc-orb"></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-pill"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="calc-header-row">
            <div>
                <div class="calc-title">Calculator</div>
                <div class="calc-subtitle">Glassmode · Keyboard & Numpad ready</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # DISPLAY
    st.markdown('<div class="display-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="display-expression">{st.session_state.display}</div>',
        unsafe_allow_html=True
    )
    if st.session_state.last_result is not None:
        st.markdown(
            f'<div class="display-result">{st.session_state.last_result}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="display-result">0</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 0: AC, C, √, ← (top function row) ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("AC", key="btn_ac", use_container_width=True, type="primary"):
            st.session_state.display = "0"
            st.session_state.last_result = None
            st.session_state.history = []
            st.rerun()
    with cols[1]:
        if st.button("C", key="btn_c", use_container_width=True, type="primary"):
            st.session_state.display = "0"
            st.session_state.last_result = None
            st.rerun()
    with cols[2]:
        if st.button("√", key="btn_sqrt", use_container_width=True, type="primary"):
            try:
                result = calculator.evaluate(st.session_state.display)
                result = math.sqrt(result)
                st.session_state.last_result = round(result, 10)
                st.session_state.display = str(st.session_state.last_result)
                st.rerun()
            except Exception:
                st.session_state.last_result = None
    with cols[3]:
        if st.button("←", key="btn_backspace", use_container_width=True, type="primary"):
            if len(st.session_state.display) > 0:
                st.session_state.display = st.session_state.display[:-1]
                if st.session_state.display == "":
                    st.session_state.display = "0"
            st.rerun()

    # --- ROW 1: 7, 8, 9, ÷ ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("7", key="btn_7", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "7"
            st.rerun()
    with cols[1]:
        if st.button("8", key="btn_8", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "8"
            st.rerun()
    with cols[2]:
        if st.button("9", key="btn_9", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "9"
            st.rerun()
    with cols[3]:
        if st.button("÷", key="btn_div", use_container_width=True, type="primary"):
            st.session_state.display += "/"
            st.rerun()

    # --- ROW 2: 4, 5, 6, × ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("4", key="btn_4", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "4"
            st.rerun()
    with cols[1]:
        if st.button("5", key="btn_5", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "5"
            st.rerun()
    with cols[2]:
        if st.button("6", key="btn_6", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "6"
            st.rerun()
    with cols[3]:
        if st.button("×", key="btn_mul", use_container_width=True, type="primary"):
            st.session_state.display += "*"
            st.rerun()

    # --- ROW 3: 1, 2, 3, − ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("1", key="btn_1", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "1"
            st.rerun()
    with cols[1]:
        if st.button("2", key="btn_2", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "2"
            st.rerun()
    with cols[2]:
        if st.button("3", key="btn_3", use_container_width=True):
            st.session_state.display = ("" if st.session_state.display == "0" else st.session_state.display) + "3"
            st.rerun()
    with cols[3]:
        if st.button("−", key="btn_sub", use_container_width=True, type="primary"):
            st.session_state.display += "-"
            st.rerun()

    # --- ROW 4: 0, ., %, + ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("0", key="btn_0", use_container_width=True):
            if st.session_state.display != "0":
                st.session_state.display += "0"
            st.rerun()
    with cols[1]:
        if st.button(".", key="btn_dot", use_container_width=True):
            # Basic protection: avoid multiple dots in a "chunk"
            if "." not in str(st.session_state.display).split()[-1]:
                st.session_state.display += "."
            st.rerun()
    with cols[2]:
        if st.button("%", key="btn_mod", use_container_width=True, type="primary"):
            st.session_state.display += "%"
            st.rerun()
    with cols[3]:
        if st.button("+", key="btn_add", use_container_width=True, type="primary"):
            st.session_state.display += "+"
            st.rerun()

    # --- ROW 5: ^, (, ), = ---
    cols = st.columns(4, gap="small")
    with cols[0]:
        if st.button("^", key="btn_pow", use_container_width=True, type="primary"):
            st.session_state.display += "^"
            st.rerun()
    with cols[1]:
        if st.button("(", key="btn_open", use_container_width=True):
            st.session_state.display += "("
            st.rerun()
    with cols[2]:
        if st.button(")", key="btn_close", use_container_width=True):
            st.session_state.display += ")"
            st.rerun()
    with cols[3]:
        if st.button("=", key="btn_equals", use_container_width=True, type="primary"):
            try:
                result = calculator.evaluate(st.session_state.display)
                st.session_state.last_result = round(result, 10)
                st.session_state.history.append(
                    f"{st.session_state.display} = {st.session_state.last_result}"
                )
                st.session_state.display = str(st.session_state.last_result)
                st.rerun()
            except Exception:
                st.session_state.last_result = None

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HISTORY
# =========================
st.markdown("---")
st.markdown("### 📋 History")

if st.session_state.history:
    history_html = ""
    for item in reversed(st.session_state.history[-6:]):
        history_html += f'<div class="history-item">{item}</div>'
    st.markdown(f'<div class="history-box">{history_html}</div>', unsafe_allow_html=True)
else:
    st.info("No calculations yet", icon="💡")

# =========================
# SHORTCUTS
# =========================
st.markdown("---")
with st.expander("⌨️ Keyboard & Numpad Shortcuts"):
    st.markdown("""
    **Numbers**  
    • `0–9` or `Numpad 0–9`  

    **Operators**  
    • `+` / `Numpad +` – Add  
    • `-` / `Numpad -` – Subtract  
    • `*` / `Numpad *` – Multiply  
    • `/` / `Numpad /` – Divide  
    • `%` – Modulo  
    • `^` – Power  

    **Other**  
    • `.` or `Numpad .` – Decimal  
    • `Enter` / `Numpad Enter` / `=` – Equals  
    • `Backspace` – Delete last char  
    • `C` – Clear display  
    """)

    st.markdown("""
    <div class="keycaps-row">
        <div class="keycap">7 8 9 /</div>
        <div class="keycap">4 5 6 *</div>
        <div class="keycap">1 2 3 -</div>
        <div class="keycap">0 . +</div>
        <div class="keycap">Enter / =</div>
        <div class="keycap">Backspace</div>
        <div class="keycap">C</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<p class='footer-text'>✅ Classy glass calculator • Full keyboard & numpad support</p>",
    unsafe_allow_html=True
)
