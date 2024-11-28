import streamlit as st
import pyrebase
from functools import wraps
import time

def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "login_status" not in st.session_state:
        st.session_state.login_status = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

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

def init_auth():
    """Initialize authentication state"""
    if not is_authenticated():
        show_login()
    elif st.session_state.login_status == 'success':
        st.session_state.login_status = None

def show_login():
    """Show login form"""
    st.markdown("""
    <style>
        /* Dark theme colors */
        :root {
            --bg-color: #1a1a1a;
            --card-bg: rgba(30, 30, 30, 0.95);
            --text-color: #e0e0e0;
            --input-bg: #2d2d2d;
            --input-border: #3d3d3d;
            --input-focus: #4a4a4a;
            --button-gradient: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%);
        }

        /* Login form styling */
        .login-form {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            margin: 2rem auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stTextInput > div > div > input {
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            color: var(--text-color);
            border-radius: 8px;
            padding: 0.75rem 1rem;
        }

        .stTextInput > div > div > input:focus {
            border-color: #ff4b4b;
            box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.15);
        }

        .stButton > button {
            background: var(--button-gradient);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.title("Login")
    
    # Show success/error messages if they exist
    if st.session_state.login_status == 'success':
        st.success("Login successful!")
        st.session_state.login_status = None
        st.experimental_rerun()
    elif st.session_state.login_status == 'error':
        st.error("Invalid credentials. Please try again.")
        st.session_state.login_status = None

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit and email and password:
            try:
                # Authenticate with Firebase
                user = auth.sign_in_with_email_and_password(email, password)
                
                # If we get here, authentication was successful
                st.session_state.authenticated = True
                st.session_state.user_info = user
                st.session_state.user_role = 'admin'  # Set admin role for all authenticated users
                st.session_state.login_status = 'success'
                st.experimental_rerun()
                
            except Exception as e:
                error_message = str(e)
                if "INVALID_PASSWORD" in error_message:
                    st.error("Invalid password. Please try again.")
                elif "EMAIL_NOT_FOUND" in error_message:
                    st.error("Email not found. Please check your email.")
                else:
                    st.error(f"Login failed: {error_message}")
                st.session_state.login_status = 'error'

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Handle logout"""
    if st.sidebar.button('Logout'):
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.user_role = None
        st.session_state.login_status = None
        st.experimental_rerun()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.authenticated

def login_required(func):
    """Decorator to require login for certain pages/functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            init_auth()
        else:
            return func(*args, **kwargs)
    return wrapper
