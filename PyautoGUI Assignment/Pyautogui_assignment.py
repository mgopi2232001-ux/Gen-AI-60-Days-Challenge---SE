import time, json, sys
from pathlib import Path

import pyautogui as pag
import pyperclip
import keyboard
import pygetwindow as gw

# ================= USER CONFIG =================
CONTACT_NAME = "Taniya AJM"   # chat name to search
MESSAGE = "Good Mrng Taniya, This is an automated message sent using PyAutoGUI!"  # message to send
AUTO_SEND = True          # set to False for a safe dry run first

# ================= ADVANCED ====================
COORDS_FILE = Path(__file__).with_name("wa_desktop_coords.json")
LOAD_WAIT = 1.2
SEARCH_TYPE_DELAY = 0.06
RETRIES = 3
OPEN_CHAT_WAIT = 1.0      # wait after opening chat before clicking message box

pag.FAILSAFE = True  # move mouse to top-left corner to abort

# ================ UTIL =========================
def log(msg): print(f"[RPA] {msg}")

def save_coords(coords: dict):
    COORDS_FILE.write_text(json.dumps(coords, indent=2), encoding="utf-8")

def load_coords():
    if COORDS_FILE.exists():
        return json.loads(COORDS_FILE.read_text(encoding="utf-8"))
    return {}

def focus_whatsapp():
    # Try to focus the WhatsApp Desktop window by title
    titles = [t for t in gw.getAllTitles() if t and "whatsapp" in t.lower()]
    if titles:
        try:
            win = gw.getWindowsWithTitle(titles[0])[0]
            win.activate()
            time.sleep(0.6)
            return True
        except Exception:
            pass
    # Fallback: Alt+Tab nudge
    log("WhatsApp window not found reliably. Using Alt+Tab…")
    pag.hotkey('alt', 'tab'); time.sleep(0.8)
    return True

def type_slow(text, delay=0.05):
    for ch in text:
        pag.typewrite(ch)
        time.sleep(delay)

def paste(text):
    pyperclip.copy(text); time.sleep(0.05)
    pag.hotkey('ctrl', 'v')

def click_xy(pt):
    pag.moveTo(pt["x"], pt["y"], duration=0.15)
    pag.click()

# ================ CALIBRATION ==================
"""
Run: python script.py calibrate
Capture two points with F8:
1) MESSAGE_BOX – message input (bottom)
   (We no longer need SEARCH_BOX due to Ctrl+F.)
"""
def calibrate():
    log("Calibration started. Open WhatsApp Desktop.")
    coords = {}
    log("Hover over the MESSAGE input box (bottom) and press F8.")
    keyboard.wait('f8')
    x, y = pag.position()
    coords["MESSAGE_BOX"] = {"x": x, "y": y}
    log(f"Captured MESSAGE_BOX at {(x, y)}")
    time.sleep(0.4)
    save_coords(coords)
    log(f"Saved to {COORDS_FILE}. Calibration complete.")

# ================== CORE =======================
def open_chat_keyboard(name):
    """
    Focus global search via Ctrl+F, type name, force-select first result with ArrowDown+Enter.
    """
    # Always force focus to search
    pag.hotkey('ctrl', 'f'); time.sleep(0.15)
    # Clear any previous search text
    pag.hotkey('ctrl', 'a'); time.sleep(0.05); pag.press('backspace'); time.sleep(0.05)
    # Type the target name/number
    type_slow(name, SEARCH_TYPE_DELAY)
    time.sleep(0.5)
    # Force selecting first result explicitly
    pag.press('down'); time.sleep(0.1)
    pag.press('enter'); time.sleep(OPEN_CHAT_WAIT)

def send_message(coords, text, auto_send=True):
    click_xy(coords["MESSAGE_BOX"])
    time.sleep(0.1)
    paste(text)
    time.sleep(0.2)
    if auto_send:
        pag.press('enter')

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "calibrate":
        calibrate()
        return

    coords = load_coords()
    if not coords or "MESSAGE_BOX" not in coords:
        log("No coordinates found. Run calibration first:  python script.py calibrate")
        sys.exit(1)

    if not focus_whatsapp():
        log("Could not focus WhatsApp. Make sure it’s open.")
        sys.exit(2)

    time.sleep(LOAD_WAIT)

    for attempt in range(1, RETRIES + 1):
        try:
            log(f"Opening chat (keyboard): {CONTACT_NAME} (try {attempt}/{RETRIES})")
            open_chat_keyboard(CONTACT_NAME)
            send_message(coords, MESSAGE, AUTO_SEND)
            log("Done ✅")
            break
        except Exception as e:
            log(f"Attempt failed: {e}")
            time.sleep(1.0)

if __name__ == "__main__":
    main()
