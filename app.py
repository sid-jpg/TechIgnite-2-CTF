import streamlit as st
from firebase_init import init_firebase, verify_token
from auth import login_required, logout

# Initialize Firebase
if not firebase_admin._apps:
    try:
        auth = init_firebase()
        if auth:
            st.session_state.firebase_initialized = True
            st.session_state.auth = auth
        else:
            st.session_state.firebase_initialized = False
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {str(e)}")
        st.session_state.firebase_initialized = False

# Page config
st.set_page_config(
    page_title="TechIgnite CTF",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Welcome to TechIgnite CTF")
    
    # Check if user is logged in
    if 'user' not in st.session_state:
        st.write("Please log in to continue")
        return
    
    # Display user info
    user = st.session_state.user
    st.write(f"Welcome, {user['email']}")
    
    # Logout button
    if st.button("Logout"):
        logout()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
