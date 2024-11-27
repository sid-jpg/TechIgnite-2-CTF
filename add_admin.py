import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import streamlit as st

# Firebase Authentication Configuration
def get_firebase_config():
    return {
        "apiKey": st.secrets["firebase"]["api_key"],
        "authDomain": st.secrets["firebase"]["auth_domain"],
        "projectId": st.secrets["firebase"]["project_id"],
        "storageBucket": st.secrets["firebase"]["storage_bucket"],
        "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
        "appId": st.secrets["firebase"]["app_id"],
        "databaseURL": st.secrets["firebase"]["database_url"]
    }

def init_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        try:
            # Get credentials from Streamlit secrets
            firebase_creds = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
            }
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error("Error initializing Firebase. Please check your credentials.")
            st.stop()
    return firestore.client()

def create_admin_user():
    """Create admin user in Firebase Auth and Firestore"""
    # Initialize Firebase Auth
    firebase_config = get_firebase_config()
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    
    # Create user in Firebase Auth
    email = "admin@techiginitectf.com"
    password = "admin123"  # Change this to a secure password
    
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Created user: {email}")
        
        # Add admin role in Firestore
        db = init_firebase()
        db.collection('users').document(user['localId']).set({
            'email': email,
            'role': 'admin',
            'created_at': firestore.SERVER_TIMESTAMP
        })
        
        print(f"Added admin role for user: {email}")
        print("\nAdmin credentials:")
        print(f"Email: {email}")
        print(f"Password: {password}")
        
    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            print(f"User {email} already exists")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_admin_user()
