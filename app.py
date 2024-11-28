import streamlit as st
from auth import show_restricted_access, logout, is_authenticated, login_required
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db
import os

# Initialize Firebase
db = get_db()

# Set page config
st.set_page_config(
    page_title="TechIgnite CTF",
    page_icon=" 🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load cyberpunk styles
with open(os.path.join(os.path.dirname(__file__), 'styles', 'cyberpunk.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Security Scripts
st.markdown("""
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
    st.markdown("""
        <div class="cyberpunk-container">
            <h1 class="glitch-text">User Profile <span class="icon">👤</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state.get("user_info", {})
    
    # Display user information in a cyberpunk card
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="cyberpunk-card">
                <h3>User Information</h3>
                <div class="info-container">
                    <p><span class="label">Email:</span> {}</p>
                    <p><span class="label">User ID:</span> {}</p>
                </div>
            </div>
        """.format(
            user_info.get('email', 'N/A'),
            user_info.get('uid', 'N/A')
        ), unsafe_allow_html=True)

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
