import streamlit as st
import pyrebase
from functools import wraps
import time

def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = None
    if "login_status" not in st.session_state:
        st.session_state["login_status"] = None
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

# Initialize session state at startup
init_session_state()

def get_firebase_config():
    """Get Firebase configuration from Streamlit secrets"""
    try:
        return {
            "apiKey": st.secrets["firebase_web"]["apiKey"],
            "authDomain": st.secrets["firebase_web"]["authDomain"],
            "projectId": st.secrets["firebase_web"]["projectId"],
            "storageBucket": st.secrets["firebase_web"]["storageBucket"],
            "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
            "appId": st.secrets["firebase_web"]["appId"],
            "databaseURL": st.secrets["firebase_web"]["databaseURL"]
        }
    except Exception as e:
        st.error("Error loading Firebase configuration. Please check your secrets.toml file.")
        print(f"Firebase config error: {str(e)}")  # For debugging
        return None

# Initialize Firebase Authentication
firebase_config = get_firebase_config()
if firebase_config:
    try:
        firebase = pyrebase.initialize_app(firebase_config)
        auth = firebase.auth()
    except Exception as e:
        st.error("Error initializing Firebase. Please check your configuration.")
        print(f"Firebase init error: {str(e)}")  # For debugging
        auth = None
else:
    auth = None

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_user_info():
    """Get current user information"""
    return st.session_state.get("user_info", None)

def login(email, password):
    """Handle login and return success/error message"""
    try:
        if auth is None:
            return "Firebase authentication not initialized properly"
        
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["authenticated"] = True
        st.session_state["user_info"] = user
        return "success"
    except Exception as e:
        print(f"Login error: {str(e)}")  # For debugging
        return "Invalid email or password"

def logout():
    """Handle logout"""
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.session_state["user_role"] = None
    st.session_state["login_status"] = None

def login_required(func):
    """Decorator to require login for certain pages/functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("Please log in to access this page")
            show_login()
            return
        return func(*args, **kwargs)
    return wrapper

def show_login():
    """Show login form"""
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
            background: linear-gradient(45deg, #FF6B6B 30%, #FF8E53 90%);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-header">Login</h1>', unsafe_allow_html=True)
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if email and password:
                result = login(email, password)
                if result == "success":
                    st.session_state["login_status"] = "success"
                    st.experimental_rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both email and password")
        
        st.markdown('</div>', unsafe_allow_html=True)

def init_auth():
    """Initialize authentication state"""
    if not is_authenticated():
        show_login()
    elif st.session_state.get("login_status") == "success":
        st.session_state["login_status"] = None
