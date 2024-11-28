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
    return "user_info" in st.session_state

def login_required(func):
    """Decorator to require login for certain pages"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            show_restricted_access()
            return None
        return func(*args, **kwargs)
    return wrapper

def show_restricted_access():
    """Show restricted access message with cyberpunk styling"""
    st.markdown("""
        <div class="cyberpunk-container">
            <h1 class="glitch-text">Access Restricted 🔒</h1>
            <div class="cyberpunk-card error-card">
                <h3>Authentication Required</h3>
                <p class="warning-text">This is a restricted area. Access denied.</p>
                <div class="cyber-line"></div>
                <p class="info-text">Please contact the administrator for access.</p>
            </div>
        </div>
        
        <style>
            .error-card {
                border-color: #ff0066 !important;
                box-shadow: 0 0 20px rgba(255, 0, 102, 0.2) !important;
            }
            
            .warning-text {
                color: #ff0066 !important;
                font-size: 1.2em !important;
                margin: 1rem 0 !important;
            }
            
            .info-text {
                color: #00ff9d !important;
                font-size: 0.9em !important;
                opacity: 0.8 !important;
            }
            
            .cyber-line {
                height: 2px;
                background: linear-gradient(90deg, #ff0066, #00ff9d);
                margin: 1rem 0;
                position: relative;
            }
            
            .cyber-line::before {
                content: '';
                position: absolute;
                width: 10px;
                height: 10px;
                background: #ff0066;
                left: 0;
                top: -4px;
                transform: rotate(45deg);
            }
            
            .cyber-line::after {
                content: '';
                position: absolute;
                width: 10px;
                height: 10px;
                background: #00ff9d;
                right: 0;
                top: -4px;
                transform: rotate(45deg);
            }
            
            .glitch-text {
                position: relative;
                animation: glitch 3s infinite;
            }
            
            @keyframes glitch {
                0% {
                    text-shadow: 0.05em 0 0 #ff0066, -0.05em -0.025em 0 #00ff9d;
                }
                14% {
                    text-shadow: 0.05em 0 0 #ff0066, -0.05em -0.025em 0 #00ff9d;
                }
                15% {
                    text-shadow: -0.05em -0.025em 0 #ff0066, 0.025em 0.025em 0 #00ff9d;
                }
                49% {
                    text-shadow: -0.05em -0.025em 0 #ff0066, 0.025em 0.025em 0 #00ff9d;
                }
                50% {
                    text-shadow: 0.025em 0.05em 0 #ff0066, 0.05em 0 0 #00ff9d;
                }
                99% {
                    text-shadow: 0.025em 0.05em 0 #ff0066, 0.05em 0 0 #00ff9d;
                }
                100% {
                    text-shadow: -0.025em 0 0 #ff0066, -0.025em -0.025em 0 #00ff9d;
                }
            }
        </style>
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
