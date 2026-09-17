import streamlit as st
import datetime
import os
import sys
import json

# Add the parent directory to sys.path so we can import tradingagents
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
except ImportError as e:
    st.error(f"Failed to import TradingAgentsGraph: {e}")
import os
import pyrebase
import streamlit as st

firebaseConfig = {
  "apiKey": "AIzaSyCNOxE5_0mXQYVG8t4IkUz50Qw8hyPTrSA",
  "authDomain": "intellitrade-82939.firebaseapp.com",
  "projectId": "intellitrade-82939",
  "storageBucket": "intellitrade-82939.firebasestorage.app",
  "messagingSenderId": "852041578558",
  "appId": "1:852041578558:web:9342a6d2c5884dfec5396f",
  "measurementId": "G-46PZN3EZ5T",
  "databaseURL": ""
}

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
except Exception as e:
    auth = None

logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")

st.set_page_config(
    page_title="IntelliTrade",
    page_icon=logo_path,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo(logo_path, size="large")

# Custom CSS for a sleek look
st.markdown("""
<style>
    /* Sleek Title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(#00d26a, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    /* Style the tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 4px;
        color: #fff;
        padding: 0 16px;
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117;
    }
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #1e1e24;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #333;
    }
    /* Button */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 106, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def render_auth_ui():
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        col_logo1, col_logo2, col_logo3 = st.columns([1, 1.5, 1])
        with col_logo2:
            st.image(logo_path, use_container_width=True)
            
        st.markdown("<h2 style='text-align: center; margin-top: 10px;'>Welcome to IntelliTrade</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Please sign in to access your AI trading agents.</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)
                
                if submitted:
                    if auth:
                        try:
                            user = auth.sign_in_with_email_and_password(email, password)
                            st.session_state['user'] = user
                            st.rerun()
                        except Exception as e:
                            if "INVALID_LOGIN_CREDENTIALS" in str(e):
                                st.error("Incorrect email or password.")
                            else:
                                st.error(f"Login failed: Make sure Email/Password Auth is enabled in your Firebase Console.")
                    else:
                        st.error("Firebase Auth is not initialized.")
                        
        with tab2:
            with st.form("signup_form"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                signup_submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if signup_submitted:
                    if auth:
                        try:
                            user = auth.create_user_with_email_and_password(new_email, new_password)
                            st.success(f"Account created for {new_username}! You can now log in.")
                        except Exception as e:
                            st.error(f"Signup failed: Make sure Email/Password Auth is enabled in your Firebase Console.")
                    else:
                        st.error("Firebase Auth is not initialized.")

if 'user' not in st.session_state:
    render_auth_ui()
    st.stop()

# --- Main App (Only runs if logged in) ---

col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_path, width=100)
with col2:
    st.markdown('<h1 class="main-title">IntelliTrade</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Autonomous AI Trading Analysis</p>', unsafe_allow_html=True)

if st.button("Log Out"):
    del st.session_state['user']
    st.rerun()

CONFIG_FILE = "ui_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config():
    keys_to_save = ["ticker", "asset_type", "llm_provider", "openai_key", "anthropic_key", "google_key"]
    data = {k: st.session_state[k] for k in keys_to_save if k in st.session_state}
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

if "config_loaded" not in st.session_state:
    saved_config = load_config()
    for k, v in saved_config.items():
        st.session_state[k] = v
    st.session_state["config_loaded"] = True

if "ticker" not in st.session_state: st.session_state["ticker"] = "AAPL"
if "asset_type" not in st.session_state: st.session_state["asset_type"] = "stock"
if "llm_provider" not in st.session_state: st.session_state["llm_provider"] = "openai"
if "openai_key" not in st.session_state: st.session_state["openai_key"] = ""
if "anthropic_key" not in st.session_state: st.session_state["anthropic_key"] = ""
if "google_key" not in st.session_state: st.session_state["google_key"] = ""

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3256/3256114.png", width=60)
    st.header("⚙️ Configuration")
    
    st.markdown("### Asset Details")
    ticker = st.text_input("Ticker Symbol", key="ticker", on_change=save_config, help="Enter the symbol you want to analyze (e.g., AAPL, BTC-USD)")
    trade_date = st.date_input("Trade Date", datetime.date.today() - datetime.timedelta(days=1))
    asset_type = st.selectbox("Asset Type", ["stock", "crypto"], key="asset_type", on_change=save_config)
    
    st.markdown("---")
    st.markdown("### 🧠 LLM Settings")
    llm_provider = st.selectbox("Provider", ["openai", "anthropic", "google"], key="llm_provider", on_change=save_config)
    
    if llm_provider == "openai":
        api_key = st.text_input("OpenAI API Key", type="password", key="openai_key", on_change=save_config)
        if api_key: os.environ["OPENAI_API_KEY"] = api_key
    elif llm_provider == "anthropic":
        api_key = st.text_input("Anthropic API Key", type="password", key="anthropic_key", on_change=save_config)
        if api_key: os.environ["ANTHROPIC_API_KEY"] = api_key
    elif llm_provider == "google":
        api_key = st.text_input("Google API Key", type="password", key="google_key", on_change=save_config)
        if api_key: os.environ["GOOGLE_API_KEY"] = api_key

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Analysis", type="primary")

if run_btn:
    if not ticker:
        st.error("⚠️ Please enter a ticker symbol to proceed.")
    else:
        # Display a nice status update
        status_box = st.info(f"⏳ **Running comprehensive analysis for {ticker} on {trade_date}...**\n\nThe AI agents are fetching data, reading news, running financials, and debating the best trading strategy. This may take a few minutes.")
        
        with st.spinner("AI Agents at work..."):
            try:
                # Properly configure provider and model names
                from tradingagents.default_config import DEFAULT_CONFIG
                run_config = DEFAULT_CONFIG.copy()
                run_config["llm_provider"] = llm_provider
                
                if llm_provider == "google":
                    run_config["deep_think_llm"] = "gemini-3.6-pro"
                    run_config["quick_think_llm"] = "gemini-3.6-flash"
                elif llm_provider == "anthropic":
                    run_config["deep_think_llm"] = "claude-3-7-sonnet-latest"
                    run_config["quick_think_llm"] = "claude-3-5-haiku-latest"
                elif llm_provider == "openai":
                    run_config["deep_think_llm"] = "gpt-4o"
                    run_config["quick_think_llm"] = "gpt-4o-mini"
                
                # Verify API key is present in environment
                key_name_map = {
                    "openai": "OPENAI_API_KEY",
                    "anthropic": "ANTHROPIC_API_KEY",
                    "google": "GOOGLE_API_KEY"
                }
                expected_key_env = key_name_map.get(llm_provider)
                if expected_key_env and not os.environ.get(expected_key_env):
                    st.error(f"🛑 Please provide your {llm_provider.capitalize()} API key in the sidebar before running the analysis.")
                    st.stop()
                
                graph = TradingAgentsGraph(config=run_config)
                
                # Initialize Progress UI
                progress_bar = st.progress(0, text="Initializing Agents...")
                
                # Estimated total steps in a typical full run
                TOTAL_STEPS = 9 
                current_step = [0] # Use list to modify inside callback closure
                
                def update_progress(chunk):
                    node_name = list(chunk.keys())[0] if chunk else "Unknown"
                    friendly_names = {
                        "market_data": "Fetching Market Data...",
                        "market_analyst": "Analyzing Broad Market...",
                        "sentiment_analyst": "Analyzing Market Sentiment...",
                        "news_analyst": "Reading Latest News...",
                        "fundamentals_analyst": "Reviewing Financial Fundamentals...",
                        "investment_debate": "Bull & Bear Agents Debating...",
                        "trader": "Formulating Trading Plan...",
                        "risk_management": "Risk Manager Reviewing Trade...",
                        "portfolio_manager": "Portfolio Manager Finalizing..."
                    }
                    display_text = friendly_names.get(node_name, f"Executing {node_name}...")
                    
                    current_step[0] = min(current_step[0] + 1, TOTAL_STEPS)
                    progress_pct = int((current_step[0] / TOTAL_STEPS) * 100)
                    progress_bar.progress(progress_pct, text=f"⏳ {display_text}")
                
                final_state, signal = graph.propagate(ticker, str(trade_date), asset_type, on_progress=update_progress)
                
                progress_bar.progress(100, text="✅ Analysis Complete!")
                status_box.empty()
                
                # Signal logic for colors
                signal_str = str(signal).upper()
                if "BUY" in signal_str or "OVERWEIGHT" in signal_str:
                    color = "green"
                    icon = "✅"
                elif "SELL" in signal_str or "UNDERWEIGHT" in signal_str:
                    color = "red"
                    icon = "🚨"
                else:
                    color = "orange"
                    icon = "⚖️"
                
                # Dashboard layout
                st.markdown(f"## {icon} Final Recommendation: <span style='color:{color}'>{signal}</span>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Asset", ticker.upper())
                col2.metric("Asset Type", asset_type.capitalize())
                col3.metric("Analysis Date", str(trade_date))
                
                st.markdown("---")
                st.markdown("### 📊 Agent Reports & Debate Logs")
                
                tabs = st.tabs(["🏛️ Market", "🎭 Sentiment", "📰 News", "🏦 Fundamentals", "🐂 Bull", "🐻 Bear", "📈 Trader", "🛡️ Risk Mgmt"])
                
                with tabs[0]: st.markdown(final_state.get("market_report", "*No market report generated.*"))
                with tabs[1]: st.markdown(final_state.get("sentiment_report", "*No sentiment report generated.*"))
                with tabs[2]: st.markdown(final_state.get("news_report", "*No news report generated.*"))
                with tabs[3]: st.markdown(final_state.get("fundamentals_report", "*No fundamentals report generated.*"))
                with tabs[4]: st.markdown(final_state.get("investment_debate_state", {}).get("bull_history", "*No bull history generated.*"))
                with tabs[5]: st.markdown(final_state.get("investment_debate_state", {}).get("bear_history", "*No bear history generated.*"))
                with tabs[6]: st.markdown(final_state.get("trader_investment_plan", "*No trader plan generated.*"))
                with tabs[7]: st.markdown(final_state.get("risk_debate_state", {}).get("judge_decision", "*No risk judge decision generated.*"))
                    
            except Exception as e:
                status_box.empty()
                st.error(f"❌ An error occurred: {e}")
                with st.expander("Show detailed error log"):
                    st.exception(e)
