import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import pyrebase
import json
import os
import tempfile

def load_firebase_service_account():
    """Load Firebase Admin SDK service account"""
    try:
        # Try loading from secrets
        service_account = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
            "universe_domain": "googleapis.com"
        }
        
        # Write to temporary file
        temp_dir = tempfile.gettempdir()
        temp_service_account_path = os.path.join(temp_dir, 'firebase_service_account_temp.json')
        with open(temp_service_account_path, 'w') as f:
            json.dump(service_account, f)
        return temp_service_account_path
        
    except Exception as e:
        print(f"Error loading service account: {str(e)}")
        st.error("Error loading Firebase service account. Please check your configuration.")
        return None

def init_firebase():
    """Initialize Firebase with credentials from Streamlit secrets"""
    if not firebase_admin._apps:
        try:
            # Get Firebase credentials from Streamlit secrets
            firebase_creds = st.secrets["firebase"]
            
            # Create a temporary file to store the credentials
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(firebase_creds, f)
                temp_file_path = f.name
            
            try:
                # Initialize Firebase with the temporary credentials file
                cred = credentials.Certificate(temp_file_path)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized successfully")
                
                # Initialize Firestore
                db = firestore.client()
                print("Firestore initialized successfully")
                
                # Load Firebase web configuration from secrets
                firebase_config = {
                    "apiKey": st.secrets["firebase_web"]["apiKey"],
                    "authDomain": st.secrets["firebase_web"]["authDomain"],
                    "projectId": st.secrets["firebase_web"]["projectId"],
                    "storageBucket": st.secrets["firebase_web"]["storageBucket"],
                    "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
                    "appId": st.secrets["firebase_web"]["appId"],
                    "databaseURL": st.secrets["firebase_web"]["databaseURL"]
                }
                
                # Initialize Pyrebase
                firebase = pyrebase.initialize_app(firebase_config)
                auth = firebase.auth()
                print("Firebase Authentication initialized successfully")
                
                return auth
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
        except Exception as e:
            error_msg = str(e)
            print(f"Firebase initialization error: {error_msg}")
            if "API key not valid" in error_msg:
                st.error("Invalid Firebase Web API Key. Please check your configuration.")
            return None

def get_db():
    """Get Firestore database instance"""
    if not firebase_admin._apps:
        init_firebase()
    return firestore.client()

def verify_token(id_token):
    """Verify Firebase ID token"""
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None
