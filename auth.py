import streamlit as st
import firebase_admin
from firebase_admin import auth as firebase_auth
from functools import wraps
import time
from firebase_init import init_firebase

# Initialize Firebase Authentication
auth = init_firebase()

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

        print(f"Attempting login for {email}")
        # Sign in with email and password
        user = auth.sign_in_with_email_and_password(email, password)
        print("Successfully signed in with email/password")
        
        # Get and verify ID token
        id_token = user.get('idToken')
        if not id_token:
            print("No ID token received")
            return "Authentication error: No token received"

        print("Verifying token...")
        # Verify the token
        decoded_token = verify_token(id_token)
        if decoded_token:
            print("Token verified successfully")
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
                print("User role: admin")
            else:
                st.session_state["user_role"] = "user"
                print("User role: user")
            
            return "success"
        else:
            print("Token verification failed")
            return "Invalid authentication token"

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
            return f"Login failed: {error_message}"

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
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Generate a unique form key for each instance
    form_key = f"auth_login_form_{id(st.session_state)}"
    
    with st.form(key=form_key):  
        st.markdown("### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if email and password:
                with st.spinner("Logging in..."):
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

init_auth()
