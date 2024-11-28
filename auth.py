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
            st.warning("Access restricted. Please contact administrator.")
            return
        return func(*args, **kwargs)
    return wrapper

def show_restricted_access():
    """Display restricted access message"""
    st.title("Restricted Access")
    st.warning("This is a private application. Please contact administrator for access.")

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
