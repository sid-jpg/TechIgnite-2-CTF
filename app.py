import streamlit as st
from auth import show_restricted_access, logout, is_authenticated, login_required
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db

# Initialize Firebase
db = get_db()

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
        
        /* Main container styling */
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
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Title styling */
        .main-title {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            font-size: 2.5rem;
            border-bottom: 2px solid #00ff9d;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-title {
                font-size: 1.8rem;
                padding: 1rem 0;
            }
            
            .appview-container .main .block-container {
                padding: 1rem;
                margin: 0.5rem;
            }
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
            text-align: center;
        }
        
        /* Text elements */
        p, div, span {
            font-family: 'Courier New', monospace;
            color: #b3b3b3;
            text-align: center;
        }
        
        /* Components styling */
        .stButton > button {
            font-family: 'Orbitron', sans-serif !important;
            background: transparent !important;
            color: #00ff9d !important;
            border: 2px solid #00ff9d !important;
            border-radius: 5px !important;
            padding: 0.5rem 2rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2) !important;
            margin: 0 auto;
            display: block;
        }
        
        .stButton > button:hover {
            background: #00ff9d !important;
            color: #1a1a2e !important;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.4) !important;
            transform: translateY(-2px);
        }
    </style>
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
    
    # Display main title
    st.markdown('<h1 class="main-title">TechIgnite 2.O</h1>', unsafe_allow_html=True)
    
    if not is_authenticated():
        show_restricted_access()
    else:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h2>Welcome to TechIgnite CTF</h2>
                <p>Access the challenges through the navigation menu</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
