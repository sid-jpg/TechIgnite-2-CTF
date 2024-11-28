import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import pyrebase
import json

def init_firebase():
    """Initialize Firebase Admin SDK and Authentication"""
    if not firebase_admin._apps:
        try:
            # Load and format service account credentials
            service_account = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),  # Fix private key formatting
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
            print(f"Firebase initialization error: {str(e)}")
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
            st.error("Error initializing Firebase Authentication.")
            return None
