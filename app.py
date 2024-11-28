import streamlit as st
from auth import show_login, logout, is_authenticated, login_required
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db

# Initialize Firebase
db = get_db()

# Set page config
st.set_page_config(
    page_title="TechIgnite CTF",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.title("Navigation")
        if is_authenticated():
            if st.button("Home"):
                st.session_state.page = "home"
            if st.button("Challenges"):
                st.session_state.page = "challenges"
            if st.button("Leaderboard"):
                st.session_state.page = "leaderboard"
            if st.button("Profile"):
                st.session_state.page = "profile"
            if st.button("Logout"):
                logout()
                st.session_state.page = "home"
                st.experimental_rerun()
        else:
            if st.button("Home"):
                st.session_state.page = "home"
            if st.button("Login"):
                st.session_state.page = "login"

# Pages
def home_page():
    st.title("Welcome to TechIgnite CTF! 🚀")
    st.write("""
    ### About
    This is a Capture The Flag (CTF) platform where you can test and improve your cybersecurity skills.
    
    ### How to Play
    1. Create an account or login
    2. Browse available challenges
    3. Solve challenges and submit flags
    4. Earn points and compete on the leaderboard
    
    ### Get Started
    Login to start solving challenges!
    """)

@login_required
def challenges_page():
    st.title("Challenges 🎯")
    # Add your challenges implementation here
    st.write("Challenges coming soon!")

@login_required
def leaderboard_page():
    st.title("Leaderboard 🏆")
    # Add your leaderboard implementation here
    st.write("Leaderboard coming soon!")

@login_required
def profile_page():
    st.title("Profile 👤")
    user_info = st.session_state.get("user_info", {})
    st.write(f"Username: {user_info.get('email', 'N/A')}")
    # Add more profile information here

def login_page():
    show_login()

# Main app
def main():
    sidebar()
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "challenges":
        challenges_page()
    elif st.session_state.page == "leaderboard":
        leaderboard_page()
    elif st.session_state.page == "profile":
        profile_page()

if __name__ == "__main__":
    main()
