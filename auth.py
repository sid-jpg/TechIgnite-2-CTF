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
        cred = credentials.Certificate({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully")
    except Exception as e:
        print("Error initializing Firebase Admin SDK")
        st.error("Error initializing Firebase Admin SDK. Please check your configuration.")

# Initialize Firebase Authentication
try:
    firebase = pyrebase.initialize_app({
        "apiKey": st.secrets["firebase_web"]["apiKey"],
        "authDomain": st.secrets["firebase_web"]["authDomain"],
        "projectId": st.secrets["firebase_web"]["projectId"],
        "storageBucket": st.secrets["firebase_web"]["storageBucket"],
        "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
        "appId": st.secrets["firebase_web"]["appId"],
        "databaseURL": st.secrets["firebase_web"]["databaseURL"]
    })
    auth = firebase.auth()
    print("Firebase Authentication initialized successfully")
except Exception as e:
    print("Error initializing Firebase Authentication")
    st.error("Error initializing Firebase Authentication. Please check your configuration.")
    auth = None

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = None
    if "user_token" not in st.session_state:
        st.session_state["user_token"] = None
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

init_session_state()

def verify_token(id_token):
    """Verify Firebase ID token and get user claims"""
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print("Token verification error")
        return None

def login(email, password):
    """Handle login and return success/error message"""
    try:
        if not auth:
            return "Firebase authentication not initialized properly"

        # Sign in with email and password
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Get and verify ID token
        id_token = user.get('idToken')
        if not id_token:
            return "Authentication error: No token received"

        # Verify the token
        decoded_token = verify_token(id_token)
        if decoded_token:
            # Set session state
            st.session_state["authenticated"] = True
            st.session_state["user_info"] = {
                "email": decoded_token.get("email"),
                "uid": decoded_token.get("uid")
            }
            st.session_state["user_token"] = id_token
            
            # Check for admin claim
            claims = decoded_token.get("claims", {})
            if claims.get("admin", False):
                st.session_state["user_role"] = "admin"
            else:
                st.session_state["user_role"] = "user"
            
            return "success"
        else:
            return "Invalid authentication token"

    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            return "Invalid password"
        elif "EMAIL_NOT_FOUND" in error_message:
            return "Email not found"
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
            return "Too many attempts. Please try again later"
        else:
            return "Login failed. Please check your credentials and try again."

def logout():
    """Handle logout"""
    for key in ["authenticated", "user_info", "user_token", "user_role"]:
        if key in st.session_state:
            del st.session_state[key]
    init_session_state()

def login_required(func):
    """Decorator to require login for certain pages/functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authenticated", False):
            st.warning("Please log in to access this page")
            show_login()
            return
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """Decorator to require admin role for certain pages/functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authenticated", False):
            st.warning("Please log in to access this page")
            show_login()
            return
        if st.session_state.get("user_role") != "admin":
            st.error("You don't have permission to access this page")
            return
        return func(*args, **kwargs)
    return wrapper

def show_login():
    """Display login form"""
    with st.form("login_form"):
        st.markdown("### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if email and password:
                result = login(email, password)
                if result == "success":
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both email and password")

def init_auth():
    """Initialize authentication state"""
    if not is_authenticated():
        show_login()
    elif st.session_state.get("login_status") == "success":
        st.session_state["login_status"] = None

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_user_info():
    """Get current user information"""
    return st.session_state.get("user_info", None)

def get_firebase_config():
    """Get Firebase configuration from Streamlit secrets"""
    try:
        config = {
            "apiKey": st.secrets["firebase_web"]["apiKey"],
            "authDomain": st.secrets["firebase_web"]["authDomain"],
            "projectId": st.secrets["firebase_web"]["projectId"],
            "storageBucket": st.secrets["firebase_web"]["storageBucket"],
            "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
            "appId": st.secrets["firebase_web"]["appId"],
            "databaseURL": st.secrets["firebase_web"]["databaseURL"]
        }
        print("Firebase config loaded successfully")
        return config
    except Exception as e:
        st.error("Error loading Firebase configuration. Please check your secrets.toml file.")
        print("Firebase config error occurred")
        return None

init_auth()
