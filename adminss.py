import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db
import time

# Initialize Firestore
db = get_db()

def init_session_state():
    """Initialize session state variables"""
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False
    if "admin_info" not in st.session_state:
        st.session_state["admin_info"] = None

def verify_admin_credentials(username, password):
    """Verify admin credentials against Firestore"""
    try:
        admins_ref = db.collection('admins')
        query = admins_ref.where('username', '==', username).where('password', '==', password).stream()
        return any(admin for admin in query)
    except Exception as e:
        st.error(f"Authentication error occurred. Please try again.")
        return False

def admin_login():
    """Handle admin login"""
    st.title("Admin Dashboard Login")
    
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if verify_admin_credentials(username, password):
                st.session_state["admin_authenticated"] = True
                st.session_state["admin_info"] = {"username": username}
                st.success("Login successful!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

def show_admin_dashboard():
    """Display admin dashboard"""
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state.admin_info['username']}!")

    if st.button("Logout"):
        st.session_state["admin_authenticated"] = False
        st.session_state["admin_info"] = None
        st.experimental_rerun()

    # Add your admin dashboard components here
    with st.expander("Manage Challenges"):
        st.write("Add challenge management functionality here")
        
    with st.expander("User Management"):
        st.write("Add user management functionality here")
        
    with st.expander("Statistics"):
        st.write("Add statistics and analytics here")

def main():
    init_session_state()
    
    if not st.session_state["admin_authenticated"]:
        admin_login()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    main()
