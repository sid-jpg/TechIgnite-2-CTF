import streamlit as st
import firebase_admin
from firebase_admin import firestore, auth
from functools import wraps
from firebase_init import get_db

# Initialize Firestore
db = get_db()

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = None

init_session_state()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def login_required(func):
    """Decorator to require login for certain pages"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            show_restricted_access()
            return
        return func(*args, **kwargs)
    return wrapper

def show_restricted_access():
    """Display restricted access message"""
    st.markdown("""
        <div style='
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin: 2rem auto;
            max-width: 600px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        '>
            <h1 style='
                font-family: "Orbitron", sans-serif;
                color: #00ff9d;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
                margin-bottom: 1rem;
            '>⚠️ Restricted Access</h1>
            <p style='
                font-family: "Courier New", monospace;
                color: #b3b3b3;
                margin-bottom: 1rem;
            '>This is a private application. Please contact administrator for access.</p>
            <div style='
                font-family: "Courier New", monospace;
                color: #00ff9d;
                background: rgba(0, 255, 157, 0.1);
                padding: 1rem;
                border-radius: 5px;
                margin-top: 1rem;
            '>Contact administrators for access credentials</div>
        </div>
    """, unsafe_allow_html=True)

def logout():
    """Handle logout"""
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.experimental_rerun()

def init_auth():
    """Initialize authentication state"""
    if not is_authenticated():
        show_restricted_access()

init_auth()
