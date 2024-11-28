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

def login_user(email, password):
    """Handle user login"""
    try:
        user = auth.get_user_by_email(email)
        st.session_state["authenticated"] = True
        st.session_state["user_info"] = {
            "email": email,
            "uid": user.uid
        }
        return "Login successful"
    except Exception as e:
        print(f"Login error: {str(e)}")
        return "Invalid credentials"

def login_required(func):
    """Decorator to require login for certain pages"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("Please log in to access this page")
            show_login()
            return
        return func(*args, **kwargs)
    return wrapper

def show_login():
    """Display login form"""
    st.markdown("""
    <h2 style='text-align: center;'>Login</h2>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if email and password:
                result = login_user(email, password)
                if "successful" in result:
                    st.success(result)
                    st.experimental_rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both email and password")

def logout():
    """Handle logout"""
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.experimental_rerun()

def init_auth():
    """Initialize authentication state"""
    if not is_authenticated():
        show_login()
    elif st.session_state.get("login_status") == "success":
        st.session_state["login_status"] = None

init_auth()
