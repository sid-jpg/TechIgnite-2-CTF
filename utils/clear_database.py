import os
import sys
import json

# Add parent directory to path to import firebase_init
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

def initialize_firebase():
    """Initialize Firebase with service account"""
    try:
        # Path to your service account file
        cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'firebase_credentials.json')
        
        if not os.path.exists(cred_path):
            print(f"Error: Firebase credentials file not found at {cred_path}")
            return None
        
        # Clean up any existing app
        for app in firebase_admin._apps.values():
            firebase_admin.delete_app(app)
            
        # Initialize Firebase
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Firebase initialization error: {str(e)}")
        return None

def test_database_access(db):
    """Test database access by writing and reading a document"""
    try:
        # Try to write a test document
        test_ref = db.collection('test_collection').document('test_doc')
        test_ref.set({
            'test_field': 'test_value',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("Successfully wrote test document")
        
        # Try to read it back
        doc = test_ref.get()
        if doc.exists:
            print("Successfully read test document:", doc.to_dict())
        
        # Delete the test document
        test_ref.delete()
        print("Successfully deleted test document")
        return True
    except Exception as e:
        print(f"Database access test failed: {str(e)}")
        return False

def list_all_documents(db, collection_name):
    """List all documents in a collection"""
    try:
        docs = db.collection(collection_name).stream()
        count = 0
        for doc in docs:
            print(f"Found document: {doc.id}")
            print(f"Data: {doc.to_dict()}")
            count += 1
        print(f"Total documents in {collection_name}: {count}")
    except Exception as e:
        print(f"Error listing documents in {collection_name}: {str(e)}")

def delete_collection(db, collection_name, batch_size=500):
    """Delete an entire collection in batches."""
    coll_ref = db.collection(collection_name)
    
    # First, list all documents
    print(f"\nListing documents in {collection_name}:")
    list_all_documents(db, collection_name)
    
    # Then delete them
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        try:
            print(f"Deleting document {doc.id} from {collection_name}")
            doc.reference.delete()
            deleted = deleted + 1
        except Exception as e:
            print(f"Error deleting document {doc.id}: {str(e)}")

    if deleted >= batch_size:
        return delete_collection(db, collection_name, batch_size)

    print(f"Successfully deleted {deleted} documents from collection: {collection_name}")
    return deleted

def clear_subcollections(db, collection_name):
    """Clear all subcollections within documents"""
    try:
        # Get all documents in the collection
        docs = db.collection(collection_name).stream()
        
        for doc in docs:
            # Get all subcollections for this document
            subcollections = doc.reference.collections()
            for subcoll in subcollections:
                delete_collection(db, f"{collection_name}/{doc.id}/{subcoll.id}")
                print(f"Cleared subcollection: {collection_name}/{doc.id}/{subcoll.id}")
    except Exception as e:
        print(f"Error clearing subcollections for {collection_name}: {str(e)}")

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    if not db:
        print("Failed to initialize Firebase. Exiting...")
        return
    
    # Test database access first
    print("\nTesting database access...")
    if not test_database_access(db):
        print("Database access test failed. Please check your credentials and permissions.")
        return
    
    # Collections to clear
    collections = [
        'users',
        'challenges',
        'submissions',
        'scores',
        'teams',
        'flags',
        'attempts',
        'user_submissions',
        'team_submissions',
        'settings',
        'logs'
    ]
    
    # Clear all collections and their subcollections
    for collection in collections:
        print(f"\nProcessing collection: {collection}")
        clear_subcollections(db, collection)
        delete_collection(db, collection)
        
        # Verify collection is empty
        print(f"\nVerifying {collection} is empty:")
        list_all_documents(db, collection)

    print("\nDatabase cleanup completed!")

if __name__ == "__main__":
    main()
