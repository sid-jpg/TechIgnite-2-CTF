import firebase_admin
from firebase_admin import credentials, firestore
import time
import streamlit as st

def init_firebase():
    """Initialize Firebase with credentials from Streamlit secrets"""
    if not firebase_admin._apps:
        try:
            # Get Firebase credentials from Streamlit secrets
            firebase_creds = st.secrets["firebase"]
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")
            return None
    return firestore.client()

def delete_collection(coll_ref, batch_size=100):
    """Delete a collection by batches to avoid timeout"""
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.to_dict()}")
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def delete_all_collections():
    """Delete all collections in the database"""
    db = init_firebase()
    if db is None:
        print("Failed to initialize Firebase. Exiting.")
        return
    collections = db.collections()
    
    print("Starting database cleanup...")
    for collection in collections:
        print(f"\nDeleting collection: {collection.id}")
        delete_collection(collection)
        time.sleep(1)  # Small delay to avoid rate limiting
    print("\nDatabase cleanup completed!")

if __name__ == "__main__":
    delete_all_collections()
