import streamlit as st
from auth import show_restricted_access, logout, is_authenticated, login_required
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db
from components.ctf_page import show_ctf_page

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
        
        /* Form styling */
        .stTextInput > div > div {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid #00ff9d !important;
            color: #00ff9d !important;
        }
        
        .stTextInput > label {
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid #00ff9d !important;
            color: #00ff9d !important;
        }
        
        .stSelectbox > label {
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
        }
    </style>
""", unsafe_allow_html=True)

@login_required
def home_page():
    st.markdown('<h1 class="main-title">TechIgnite 2.O</h1>', unsafe_allow_html=True)
    
    # Team selection
    if "team_id" not in st.session_state:
        st.markdown("### 👥 Select Your Team")
        teams = [f"TEAM{i}" for i in range(1, 31)]
        team_id = st.selectbox("Choose your team", teams)
        if st.button("Confirm Team"):
            st.session_state.team_id = team_id
            st.experimental_rerun()
    else:
        show_ctf_page(db)
        
        # Add logout button
        if st.button("Logout"):
            logout()
            st.experimental_rerun()

# Main app
def main():
    if not is_authenticated():
        show_restricted_access()
    else:
        home_page()

if __name__ == "__main__":
    main()
