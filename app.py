import streamlit as st
from auth import show_restricted_access, logout, is_authenticated, login_required
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db

# Initialize Firebase
db = get_db()

# Set page config
st.set_page_config(
    page_title="TechIgnite CTF",
    page_icon=" 🚩",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Hide sidebar and other default elements
st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        [data-testid="collapsedControl"] {
            display: none
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        header {visibility: hidden;}
        .appview-container .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Disable text selection */
        * {
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Custom styling */
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        h1, h2, h3 {
            color: #ffffff !important;
        }
        
        .stButton>button {
            background-color: #2e2e2e;
            color: #ffffff;
            border: 1px solid #3d3d3d;
        }
        
        .stButton>button:hover {
            background-color: #3d3d3d;
            border: 1px solid #4d4d4d;
        }
    </style>
    
    <script>
        // Disable right click
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
        document.onkeydown = function(e) {
            if (e.keyCode == 123 || 
                (e.ctrlKey && e.shiftKey && e.keyCode == 73) ||
                (e.ctrlKey && e.shiftKey && e.keyCode == 74) ||
                (e.ctrlKey && e.keyCode == 85)) {
                return false;
            }
        };
        
        // Disable view source
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'u') {
                e.preventDefault();
                return false;
            }
        });
        
        // Block developer tools
        function blockDevTools() {
            if(window.devtools.isOpen) {
                window.location.reload();
            }
        }
        
        // Additional security measures
        setInterval(function() {
            const all = document.getElementsByTagName("*");
            const devtools = /./;
            devtools.toString = function() {
                blockDevTools();
            }
            console.log(devtools);
        }, 1000);
        
        // Disable dragging
        document.addEventListener('dragstart', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Disable copy/paste
        document.addEventListener('copy', function(e) {
            e.preventDefault();
            return false;
        });
        
        document.addEventListener('paste', function(e) {
            e.preventDefault();
            return false;
        });
    </script>
""", unsafe_allow_html=True)

def home_page():
    if not is_authenticated():
        show_restricted_access()
    else:
        profile_page()

@login_required
def profile_page():
    st.title("User Profile 👤")
    user_info = st.session_state.get("user_info", {})
    
    # Display user information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### User Information")
        st.write(f"**Email:** {user_info.get('email', 'N/A')}")
        st.write(f"**User ID:** {user_info.get('uid', 'N/A')}")

# Main app
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "profile":
        profile_page()

if __name__ == "__main__":
    main()
