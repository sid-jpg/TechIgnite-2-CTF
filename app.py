import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from pages.user_page import render as render_user
from pages.admin_page import render as render_admin
from auth import show_login, login_required, admin_required, get_user_info, logout
import json

# Initialize Firebase
if not firebase_admin._apps:
    try:
        # Get Firebase credentials from Streamlit secrets
        firebase_creds = st.secrets["firebase"]
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
        st.session_state.firebase_initialized = True
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {str(e)}")
        st.session_state.firebase_initialized = False

# Page configuration
st.set_page_config(
    page_title="TechIgnite CTF Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --bg-color: #1a1a1a;
        --card-bg: rgba(30, 30, 30, 0.95);
        --text-color: #e0e0e0;
        --accent-color: #ff4b4b;
    }

    /* Main container */
    .stApp {
        background: var(--bg-color);
        color: var(--text-color);
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        font-size: 1.1rem;
        color: var(--text-color);
        opacity: 0.8;
    }

    /* Admin toggle button */
    .admin-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: transparent;
        border: none;
        color: var(--text-color);
        opacity: 0.6;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.5rem;
    }

    .admin-toggle:hover {
        opacity: 1;
        transform: scale(1.1);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeIn 0.5s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# Disable developer tools and add anti-debugging
st.markdown("""
    <script>
        // Disable right click
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
        
        // Disable keyboard shortcuts for developer tools
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || 
                (e.ctrlKey && e.shiftKey && e.key === 'I') || 
                (e.ctrlKey && e.shiftKey && e.key === 'J') || 
                (e.ctrlKey && e.key === 'U') ||
                (e.ctrlKey && e.key === 'S')) {
                e.preventDefault();
            }
        });
        
        // Anti-debugging techniques
        (function(){
            function detect() {
                const d = new Date();
                const start = d.getTime();
                debugger;
                const end = new Date().getTime();
                if ((end - start) > 100) {
                    window.location.reload();
                }
            }
            
            // Check periodically
            setInterval(detect, 1000);
            
            // Detect DevTools
            const checkDevTools = function() {
                const widthThreshold = window.outerWidth - window.innerWidth > 160;
                const heightThreshold = window.outerHeight - window.innerHeight > 160;
                if(widthThreshold || heightThreshold) {
                    document.body.innerHTML = 'Developer tools detected! Access denied.';
                }
            };
            
            setInterval(checkDevTools, 1000);
            
            // Prevent view source
            document.onkeydown = function(e) {
                if (e.ctrlKey && 
                    (e.key === 'u' || 
                     e.key === 's' ||
                     e.key === 'i' ||
                     e.key === 'j' ||
                     e.key === 'c')) {
                    return false;
                }
            };
        })();
        
        // Clear console
        console.clear();
        Object.defineProperty(console, '_commandLineAPI', { get: function() { 
            throw 'Console access disabled.';
        }});
    </script>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'admin_view' not in st.session_state:
        st.session_state.admin_view = False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'firebase_initialized' not in st.session_state:
        st.session_state.firebase_initialized = False

    st.title("🚀 TechIgnite CTF Platform")
    
    # Show user info and logout button if authenticated
    if st.session_state.get("authenticated", False):
        user_info = get_user_info()
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"Welcome, {user_info['email']}!")
            if st.session_state.get("user_role") == "admin":
                st.write("🔑 Admin Access")
        with col2:
            if st.button("Logout"):
                logout()
                st.experimental_rerun()
    else:
        show_login()

    # Header
    st.markdown('''
        <div class="main-header animate-in">
            <h1 class="main-title">TechIgnite CTF</h1>
            <p class="subtitle">Hack. Learn. Win. 🏆</p>
        </div>
    ''', unsafe_allow_html=True)

    # Admin toggle button
    st.markdown('''
        <button class="admin-toggle" onclick="handleAdminToggle()">👤</button>
        <script>
            function handleAdminToggle() {
                window.parent.postMessage({type: 'admin_toggle'}, '*');
            }
        </script>
    ''', unsafe_allow_html=True)

    # Handle admin toggle
    if st.session_state.admin_view:
        if not st.session_state.authenticated:
            auth.login()
        else:
            render_admin()
    else:
        render_user()

if __name__ == "__main__":
    main()
