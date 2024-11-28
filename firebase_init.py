import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import pyrebase
import json
import os

def validate_firebase_config():
    """Validate Firebase configuration"""
    required_firebase_keys = [
        "type", "project_id", "private_key_id", "private_key", 
        "client_email", "client_id", "auth_uri", "token_uri",
        "auth_provider_x509_cert_url", "client_x509_cert_url"
    ]
    
    required_web_keys = [
        "apiKey", "authDomain", "projectId", "storageBucket",
        "messagingSenderId", "appId", "databaseURL"
    ]
    
    # Check Firebase Admin SDK config
    for key in required_firebase_keys:
        if key not in st.secrets.get("firebase", {}):
            raise ValueError(f"Missing required Firebase Admin SDK configuration: {key}")
            
    # Check Firebase Web config
    for key in required_web_keys:
        if key not in st.secrets.get("firebase_web", {}):
            raise ValueError(f"Missing required Firebase Web configuration: {key}")

def init_firebase():
    """Initialize Firebase Admin SDK and Authentication"""
    if not firebase_admin._apps:
        try:
            # Validate configuration
            validate_firebase_config()
            
            # Load and format service account credentials
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
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
            }
            
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(service_account)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully")
            
            # Initialize Firebase Authentication
            firebase_config = {
                "apiKey": st.secrets["firebase_web"]["apiKey"],
                "authDomain": st.secrets["firebase_web"]["authDomain"],
                "projectId": st.secrets["firebase_web"]["projectId"],
                "storageBucket": st.secrets["firebase_web"]["storageBucket"],
                "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
                "appId": st.secrets["firebase_web"]["appId"],
                "databaseURL": st.secrets["firebase_web"]["databaseURL"]
            }
            
            firebase = pyrebase.initialize_app(firebase_config)
            auth = firebase.auth()
            print("Firebase Authentication initialized successfully")
            
            return auth
            
        except Exception as e:
            error_msg = str(e)
            if "API key not valid" in error_msg:
                print("Invalid Firebase Web API Key. Please check your configuration.")
                st.error("Invalid Firebase Web API Key. Please update your configuration in .streamlit/secrets.toml")
            elif "private_key" in error_msg:
                print("Invalid Firebase Admin SDK private key. Please check your configuration.")
                st.error("Invalid Firebase Admin SDK private key. Please check your configuration.")
            else:
                print(f"Firebase initialization error: {error_msg}")
                st.error("Error initializing Firebase. Please check your configuration.")
            return None
    else:
        try:
            # If Firebase Admin is already initialized, just initialize Authentication
            firebase_config = {
                "apiKey": st.secrets["firebase_web"]["apiKey"],
                "authDomain": st.secrets["firebase_web"]["authDomain"],
                "projectId": st.secrets["firebase_web"]["projectId"],
                "storageBucket": st.secrets["firebase_web"]["storageBucket"],
                "messagingSenderId": st.secrets["firebase_web"]["messagingSenderId"],
                "appId": st.secrets["firebase_web"]["appId"],
                "databaseURL": st.secrets["firebase_web"]["databaseURL"]
            }
            
            firebase = pyrebase.initialize_app(firebase_config)
            auth = firebase.auth()
            print("Firebase Authentication initialized successfully")
            
            return auth
            
        except Exception as e:
            print(f"Firebase Authentication initialization error: {str(e)}")
            st.error("Error initializing Firebase Authentication. Please check your configuration.")
            return None
