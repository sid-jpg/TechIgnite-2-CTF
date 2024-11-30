import os
import sys
import pandas as pd

# Add parent directory to path to import firebase_init
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import firebase_admin
from firebase_admin import credentials, firestore

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

def clear_collection(db, collection_name):
    """Delete all documents in a collection"""
    try:
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()
        print(f"Cleared collection: {collection_name}")
    except Exception as e:
        print(f"Error clearing collection {collection_name}: {str(e)}")

def clear_database(db):
    """Clear all collections"""
    collections = ['Questions', 'Teams', 'submissions']
    for collection in collections:
        clear_collection(db, collection)
    print("\nDatabase cleared successfully!")

def setup_questions(db):
    """Setup Questions collection from Excel file"""
    try:
        # Read Excel file
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Flagss.xlsx')
        
        # Read Excel with all cells as strings to prevent truncation
        df = pd.read_excel(excel_path, dtype=str)
        
        # Clean the dataframe
        df = df.dropna()  # Remove rows with NaN values
        df = df[df[df.columns[0]].str.strip().str.len() > 0]  # Remove rows with empty qid
        
        # Add questions to database
        batch = db.batch()
        count = 0
        
        for _, row in df.iterrows():
            qid = str(row[0]).strip()  # First column is qid
            flag = str(row[1]).strip()  # Second column is flag
            
            # Skip if qid or flag is empty
            if not qid or not flag:
                continue
                
            # Clean up the qid and flag
            qid = qid.replace(' ', '')  # Remove any spaces
            flag = flag.replace('\n', '').replace('\r', '')  # Remove newlines
                
            doc_ref = db.collection('Questions').document(qid)
            batch.set(doc_ref, {
                'qid': qid,
                'Flag': flag,
                'solvedBy': []
            })
            
            count += 1
            print(f"Added question {qid} with flag: {flag}")
            
            # Commit batch every 500 operations
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit remaining operations
        if count % 500 != 0:
            batch.commit()
            
        print(f"\nAdded {count} questions to database")
    except Exception as e:
        print(f"Error setting up questions: {str(e)}")
        import traceback
        traceback.print_exc()

def setup_teams(db):
    """Setup Teams collection"""
    try:
        batch = db.batch()
        
        # Add 30 teams
        for i in range(1, 31):
            team_id = f"TEAM{i}"
            doc_ref = db.collection('Teams').document(team_id)
            batch.set(doc_ref, {
                'teamid': team_id,
                'totalCount': 0,
                'questionsSolved': []
            })
            print(f"Added team {team_id}")
            
            # Commit batch every 500 operations
            if i % 500 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit remaining operations
        batch.commit()
        print("\nAdded 30 teams to database")
    except Exception as e:
        print(f"Error setting up teams: {str(e)}")

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    if not db:
        print("Failed to initialize Firebase. Exiting...")
        return
    
    # Clear database
    print("\nClearing database...")
    clear_database(db)
    
    # Setup Questions
    print("\nSetting up Questions collection...")
    setup_questions(db)
    
    # Setup Teams
    print("\nSetting up Teams collection...")
    setup_teams(db)
    
    print("\nDatabase setup completed!")

if __name__ == "__main__":
    main()
