import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import pyrebase
import json
import os

def load_firebase_service_account():
    """Load Firebase Admin SDK service account"""
    try:
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
            "universe_domain": st.secrets["firebase"].get("universe_domain", "googleapis.com")
        }
        return service_account
    except Exception as e:
        print(f"Error loading service account: {str(e)}")
        st.error("Error loading Firebase service account. Please check your configuration.")
        return None

def init_firebase():
    """Initialize Firebase Admin SDK and Authentication"""
    global db  # For Firestore access
    
    try:
        # Load service account
        service_account = load_firebase_service_account()
        if not service_account:
            return None
            
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully")
        
        # Initialize Firestore
        db = firestore.client()
        print("Firestore initialized successfully")
        
        # Initialize Firebase Authentication
        firebase_config = {
            "apiKey": st.secrets["firebase_web"]["apiKey"],
            "authDomain": f"{service_account['project_id']}.firebaseapp.com",
            "projectId": service_account['project_id'],
            "storageBucket": f"{service_account['project_id']}.appspot.com",
            "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
            "appId": st.secrets["firebase_web"]["appId"],
            "databaseURL": f"https://{service_account['project_id']}-default-rtdb.firebaseio.com"
        }
        
        firebase = pyrebase.initialize_app(firebase_config)
        auth = firebase.auth()
        print("Firebase Authentication initialized successfully")
        
        return auth
            
    except Exception as e:
        error_msg = str(e)
        print(f"Firebase initialization error: {error_msg}")
        
        if "API key not valid" in error_msg:
            st.error("""
            Invalid Firebase Web API Key. Please check:
            1. Firebase Console > Project Settings > General
            2. Web API Key is correct and not restricted
            3. Firebase Authentication is enabled
            """)
        elif "private_key" in error_msg:
            st.error("""
            Invalid service account configuration. Please check:
            1. Firebase Console > Project Settings > Service Accounts
            2. Generate new private key if needed
            3. Update configuration in .streamlit/secrets.toml
            """)
        else:
            st.error(f"Firebase initialization error. Please check your configuration.")
        return None

def get_db():
    """Get Firestore database instance"""
    return db if 'db' in globals() else None

def verify_token(id_token):
    """Verify Firebase ID token"""
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None
