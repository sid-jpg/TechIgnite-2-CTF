import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import pyrebase
import json
import os

# Firebase configuration for web app
firebase_config = {
    "apiKey": "AIzaSyAhlJ-zEZgDuEO5yTGLI19fV6ELto62OEs",
    "authDomain": "techiginitectf.firebaseapp.com",
    "projectId": "techiginitectf",
    "storageBucket": "techiginitectf.firebasestorage.app",
    "messagingSenderId": "1009814637785",
    "appId": "1:1009814637785:web:2ce461d0624a5b905bc2c8",
    "databaseURL": ""  # Add empty databaseURL for Pyrebase compatibility
}

def get_db():
    """Initialize Firebase and return Firestore client"""
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        try:
            # Get Firebase credentials from Streamlit secrets
            firebase_config = dict(st.secrets["firebase"])
            
            # Initialize Firebase
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            
        except Exception as e:
            st.error(f"Error initializing Firebase: {str(e)}")
            st.error("Please make sure you have set up your Firebase credentials in .streamlit/secrets.toml")
            return None
    
    return firestore.client()

def verify_token(id_token):
    """Verify Firebase ID token"""
    try:
        if not firebase_admin._apps:
            get_db()
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None

# Initialize Firebase on module load
get_db()
