import os
import sys
import random
from datetime import datetime, timedelta

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

def get_question_data(question_num):
    """Generate question data matching the existing structure"""
    data = {
        'flag': f'FLAG{{dummy_flag_for_q{question_num}}}',
        'id': f'Q{question_num}',
        'original_id': f'Q{question_num}',
        'timestamp': firestore.SERVER_TIMESTAMP
    }
    return data

def add_questions_to_database(db):
    """Add questions Q11 to Q37 to the database"""
    try:
        questions_ref = db.collection('questions')  # Note: collection name is 'questions' not 'Questions'
        batch = db.batch()
        count = 0
        
        # Add questions Q11 to Q37
        for i in range(11, 38):
            question_id = f'Q{i}'
            doc_ref = questions_ref.document(question_id)
            
            # Get question data
            data = get_question_data(i)
            
            # Add to batch
            batch.set(doc_ref, data, merge=True)
            count += 1
            print(f"Added question {question_id}")
            
            # Commit batch every 500 operations (Firestore limit)
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit any remaining operations
        if count % 500 != 0:
            batch.commit()
            
        print(f"\nSuccessfully added {count} questions to database")
        return True
    except Exception as e:
        print(f"Error adding questions: {str(e)}")
        return False

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    if not db:
        print("Failed to initialize Firebase. Exiting...")
        return
    
    # Add questions
    print("\nAdding questions Q11-Q37...")
    if add_questions_to_database(db):
        print("\nQuestions successfully added to database!")
    else:
        print("\nFailed to add questions")

if __name__ == "__main__":
    main()
