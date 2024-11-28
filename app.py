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
    page_icon="🚀",
    layout="wide"
)

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.title("Navigation")
        if is_authenticated():
            if st.button("Profile"):
                st.session_state.page = "profile"
            if st.button("Logout"):
                logout()
                st.session_state.page = "home"
                st.experimental_rerun()

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
        
    sidebar()
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "profile":
        profile_page()

if __name__ == "__main__":
    main()
