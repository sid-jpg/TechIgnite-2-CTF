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
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        /* Hide default Streamlit elements */
        [data-testid="collapsedControl"] {
            display: none
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        header {visibility: hidden;}
        
        /* Cyberpunk theme */
        .stApp {
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
            color: #00ff9d;
        }
        
        .appview-container .main .block-container {
            padding: 2rem;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        }
        
        /* Title styling */
        h1 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
            margin-bottom: 2rem;
            border-bottom: 2px solid #00ff9d;
            padding-bottom: 1rem;
        }
        
        h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Button styling */
        .stButton>button {
            font-family: 'Orbitron', sans-serif !important;
            background: transparent;
            color: #00ff9d;
            border: 2px solid #00ff9d;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        }
        
        .stButton>button:hover {
            background: #00ff9d;
            color: #1a1a2e;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.4);
            transform: translateY(-2px);
        }
        
        /* Text styling */
        p, div {
            color: #b3b3b3;
            font-family: 'Courier New', monospace;
        }
        
        /* Disable text selection */
        * {
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Warning message styling */
        .stAlert {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #ff0000;
            color: #ff0000;
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Success message styling */
        .element-container div[data-testid="stMarkdownContainer"] div.stSuccess {
            background: rgba(0, 255, 157, 0.1);
            border: 1px solid #00ff9d;
            color: #00ff9d;
            border-radius: 5px;
            padding: 1rem;
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
    st.markdown("<h1>User Profile 👤</h1>", unsafe_allow_html=True)
    user_info = st.session_state.get("user_info", {})
    
    # Display user information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>User Information</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: rgba(0, 255, 157, 0.1); padding: 1rem; border-radius: 5px; border: 1px solid #00ff9d;'>
            <p style='color: #00ff9d; margin: 0.5rem 0;'><strong>Email:</strong> {user_info.get('email', 'N/A')}</p>
            <p style='color: #00ff9d; margin: 0.5rem 0;'><strong>User ID:</strong> {user_info.get('uid', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

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
