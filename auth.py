import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from functools import wraps
import time
import json

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        firebase_creds = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
            "universe_domain": st.secrets["firebase"]["universe_domain"]
        }
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error("Error initializing Firebase Admin SDK")
        print(f"Firebase Admin SDK error: {str(e)}")

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
    if "user_token" not in st.session_state:
        st.session_state["user_token"] = None

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
        print(f"Firebase config error: {str(e)}")
        return None

# Initialize Firebase Authentication
firebase_config = get_firebase_config()
if firebase_config:
    try:
        firebase = pyrebase.initialize_app(firebase_config)
        auth = firebase.auth()
    except Exception as e:
        st.error("Error initializing Firebase. Please check your configuration.")
        print(f"Firebase init error: {str(e)}")
        auth = None
else:
    auth = None

def verify_token(id_token):
    """Verify Firebase ID token and get user claims"""
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None

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
        
        # Sign in with email and password
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Get the ID token
        id_token = user['idToken']
        
        # Verify the token and get user claims
        decoded_token = verify_token(id_token)
        if decoded_token:
            st.session_state["authenticated"] = True
            st.session_state["user_info"] = user
            st.session_state["user_token"] = id_token
            
            # Store user role if available in custom claims
            if 'admin' in decoded_token.get('custom_claims', {}):
                st.session_state["user_role"] = 'admin'
            else:
                st.session_state["user_role"] = 'user'
                
            return "success"
        else:
            return "Invalid token"
            
    except Exception as e:
        error_message = str(e)
        print(f"Login error: {error_message}")
        
        if "INVALID_PASSWORD" in error_message:
            return "Invalid password"
        elif "EMAIL_NOT_FOUND" in error_message:
            return "Email not found"
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
            return "Too many attempts. Please try again later"
        else:
            return "Login failed. Please try again"

def logout():
    """Handle logout"""
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.session_state["user_role"] = None
    st.session_state["login_status"] = None
    st.session_state["user_token"] = None

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

def admin_required(func):
    """Decorator to require admin role for certain pages/functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("Please log in to access this page")
            show_login()
            return
        if st.session_state.get("user_role") != "admin":
            st.error("You don't have permission to access this page")
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
            background: rgba(30, 30, 30, 0.95);
            border-radius: 10px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #ffffff;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
            background: linear-gradient(45deg, #FF6B6B 30%, #FF8E53 90%);
            border: none;
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        .stTextInput>div>div>input {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
        }
        .stTextInput>div>div>input:focus {
            border-color: #FF6B6B;
            box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2);
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
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
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
