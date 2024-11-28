import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import pyrebase
import json
import os

def debug_firebase_config():
    """Debug Firebase configuration without exposing sensitive data"""
    web_config = st.secrets.get("firebase_web", {})
    
    # Check if config exists
    if not web_config:
        st.error("Firebase Web configuration is missing")
        return False
        
    # Check required fields
    required_fields = ["apiKey", "authDomain", "projectId", "storageBucket", "messagingSenderId", "appId", "databaseURL"]
    missing_fields = [field for field in required_fields if not web_config.get(field)]
    
    if missing_fields:
        st.error(f"Missing required Firebase Web configuration fields: {', '.join(missing_fields)}")
        return False
        
    # Validate format of fields
    if not web_config.get("projectId") in web_config.get("authDomain", ""):
        st.error("Project ID does not match authDomain")
        return False
        
    if not web_config.get("projectId") in web_config.get("storageBucket", ""):
        st.error("Project ID does not match storageBucket")
        return False
    
    return True

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
            # Debug configuration
            if not debug_firebase_config():
                return None
                
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
            
            # Print config for debugging (without sensitive data)
            print(f"Initializing Firebase with project: {firebase_config['projectId']}")
            print(f"Auth Domain: {firebase_config['authDomain']}")
            print(f"Storage Bucket: {firebase_config['storageBucket']}")
            
            firebase = pyrebase.initialize_app(firebase_config)
            auth = firebase.auth()
            print("Firebase Authentication initialized successfully")
            
            return auth
            
        except Exception as e:
            error_msg = str(e)
            if "API key not valid" in error_msg:
                print("Invalid Firebase Web API Key. Please check your configuration.")
                st.error("""
                Invalid Firebase Web API Key. Please:
                1. Go to Firebase Console
                2. Open Project Settings
                3. Under 'General' tab, find your Web API Key
                4. Update the apiKey in .streamlit/secrets.toml
                """)
            elif "private_key" in error_msg:
                print("Invalid Firebase Admin SDK private key. Please check your configuration.")
                st.error("""
                Invalid Firebase Admin SDK private key. Please:
                1. Go to Firebase Console
                2. Open Project Settings
                3. Go to 'Service accounts' tab
                4. Generate new private key
                5. Update the private_key in .streamlit/secrets.toml
                """)
            else:
                print(f"Firebase initialization error: {error_msg}")
                st.error(f"Error initializing Firebase: {error_msg}")
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
