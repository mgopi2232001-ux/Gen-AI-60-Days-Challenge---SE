import streamlit as st

# Page configuration
st.set_page_config(
    page_title="User Information Form",
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Function to get age-appropriate motivational quote
def get_motivational_quote(age):
    """Returns a motivational quote based on age"""
    quotes = {
        "teens": [
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "You are never too young to make a difference. Start where you are, use what you have.",
            "Your potential is limitless. Every expert was once a beginner.",
            "Dream big, work hard, stay focused, and surround yourself with good people."
        ],
        "twenties": [
            "Your twenties are your selfish years. It's the time to make mistakes and figure out who you are.",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Take risks now. Do something bold. You won't regret it.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        ],
        "thirties": [
            "In your 30s, you start to understand that success is not about perfection, but progress.",
            "The best time to plant a tree was 20 years ago. The second best time is now.",
            "You are the architect of your own life. Build something beautiful.",
            "Wisdom comes from experience. Experience comes from making mistakes. - Mark Twain"
        ],
        "forties": [
            "At 40, you realize that the most important investment you can make is in yourself.",
            "Life begins at 40. It's when you truly know who you are and what you want.",
            "The older you get, the more you realize that kindness is synonymous with happiness.",
            "Your 40s are about refinement, not reinvention. You know what works."
        ],
        "fifties_plus": [
            "Age is just a number. It's the attitude you bring to life that matters.",
            "The wisdom of years is the greatest gift. Share it generously.",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            "Life's most beautiful moments come when you realize how much you've grown."
        ]
    }
    
    if age < 20:
        category = "teens"
    elif age < 30:
        category = "twenties"
    elif age < 40:
        category = "thirties"
    elif age < 50:
        category = "forties"
    else:
        category = "fifties_plus"
    
    import random
    return random.choice(quotes[category])

# Custom CSS with classy, sophisticated color palette
st.markdown("""
    <style>
    /* Elegant background - soft cream with subtle gradient */
    .main {
        background: linear-gradient(135deg, #F5F5DC 0%, #FAF0E6 25%, #FFF8DC 50%, #FDF5E6 75%, #F5F5DC 100%);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* Streamlit app background */
    .stApp {
        background: linear-gradient(135deg, #F5F5DC 0%, #FAF0E6 25%, #FFF8DC 50%, #FDF5E6 75%, #F5F5DC 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Elegant form container - white with subtle shadow */
    .stApp > div > div > div > div {
        background-color: #FFFFFF;
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
        border: 1px solid rgba(139, 69, 19, 0.1);
    }
    
    /* Classy title - deep navy with elegant styling */
    h1 {
        color: #1a1a2e;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Subheader - burgundy accent */
    h3 {
        color: #8B4513;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 1rem;
    }
    
    /* Elegant button - deep navy with gold accent */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #FFD700;
        font-weight: 600;
        padding: 0.9rem;
        border-radius: 12px;
        border: 2px solid #FFD700;
        transition: all 0.3s;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(26, 26, 46, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 26, 46, 0.4);
        border-color: #FFA500;
    }
    
    /* Elegant text input - navy border */
    .stTextInput>div>div>input {
        border: 2px solid #1a1a2e;
        border-radius: 8px;
        padding: 0.6rem;
        transition: all 0.3s;
        background-color: #FFFFFF;
        color: #1a1a2e;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8B4513;
        box-shadow: 0 0 12px rgba(139, 69, 19, 0.3);
        outline: none;
    }
    
    /* Label styling - dark for readability */
    label {
        color: #1a1a2e !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Elegant slider */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #8B4513 0%, #A0522D 50%, #CD853F 100%);
    }
    
    /* Caption styling - burgundy */
    .stCaption {
        color: #8B4513;
        font-weight: 500;
        font-size: 1rem;
    }
    
    /* Elegant greeting popup */
    .greeting-popup {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.25);
        margin: 1.5rem 0;
        border-left: 5px solid #FFD700;
    }
    
    .greeting-popup h2 {
        color: #FFD700;
        margin-bottom: 1rem;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .greeting-popup h3 {
        color: #FFD700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .greeting-popup p {
        color: #FFFFFF;
        font-size: 1.15rem;
        margin: 0.8rem 0;
        line-height: 1.6;
    }
    
    .greeting-popup .quote {
        background: rgba(255, 215, 0, 0.1);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
        margin-top: 1rem;
        font-style: italic;
        color: #FFF8DC;
    }
    
    /* Warning and info messages - readable colors */
    .stWarning {
        background: linear-gradient(135deg, #FFF8DC 0%, #FFE4B5 100%);
        border-left: 5px solid #FF8C00;
        color: #8B4513;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #E6F3FF 0%, #CCE6FF 100%);
        border-left: 5px solid #1a1a2e;
        color: #1a1a2e;
    }
    
    /* Footer styling - elegant and subtle */
    .footer {
        text-align: center;
        color: #8B4513;
        padding: 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Divider styling */
    hr {
        border: none;
        border-top: 2px solid #8B4513;
        opacity: 0.3;
        margin: 1.5rem 0;
    }
    
    /* Ensure all text is readable */
    p, span, div {
        color: #1a1a2e;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.markdown("<h1>👋 Welcome to User Information Form</h1>", unsafe_allow_html=True)
st.markdown("---")

# Create form
with st.form("user_info_form", clear_on_submit=False):
    st.subheader("📝 Please enter your information")
    
    # Name input
    name = st.text_input(
        "**Your Name**",
        placeholder="Enter your name here...",
        help="Please enter your full name"
    )
    
    # Age slider
    age = st.slider(
        "**Your Age**",
        min_value=1,
        max_value=100,
        value=25,
        help="Drag the slider to select your age"
    )
    
    # Display selected age
    st.markdown(f'<p class="stCaption">Selected age: <strong style="color: #8B4513;">{age} years</strong></p>', unsafe_allow_html=True)
    
    # Submit button
    submitted = st.form_submit_button("🚀 Submit", use_container_width=True)

# Display greeting as popup after form submission
if submitted:
    if name.strip():
        # Get motivational quote based on age
        quote = get_motivational_quote(age)
        
        # Show greeting in a properly formatted popup
        greeting_html = f"""
        <div class="greeting-popup">
            <h2>✨ Hello {name}! 👋</h2>
            <p>You are <strong>{age} years old</strong>! 🎂</p>
            <p>Nice to meet you! 😊</p>
            <h3>💫 A Thought for Your Journey</h3>
            <div class="quote">
                <p style="margin: 0; font-size: 1.1rem;">"{quote}"</p>
            </div>
            <p style="margin-top: 1rem; color: #FFD700; font-weight: 600;">Keep growing and inspiring! 🌟</p>
        </div>
        """
        st.markdown(greeting_html, unsafe_allow_html=True)
        
        # Add celebratory balloons
        st.balloons()
        
    else:
        st.warning("⚠️ Please enter your name before submitting!")
        st.info(f"Your age ({age} years) has been recorded. Please add your name and submit again.")

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">Made with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)
