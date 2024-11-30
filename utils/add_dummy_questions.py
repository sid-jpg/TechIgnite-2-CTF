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

def get_existing_question_structure(db):
    """Get structure of an existing question document"""
    try:
        questions_ref = db.collection('questions')
        # Try to get Q1 as a sample
        doc = questions_ref.document('Q1').get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Error getting existing question: {str(e)}")
        return None

def generate_dummy_question(question_num, template=None):
    """Generate dummy question data similar to existing structure"""
    categories = ['Web', 'Crypto', 'Forensics', 'OSINT', 'Reverse Engineering', 'Pwn']
    difficulties = ['Easy', 'Medium', 'Hard']
    
    data = {
        'id': f'Q{question_num}',
        'title': f'Challenge {question_num}',
        'description': f'This is a sample challenge description for Q{question_num}. Can you solve it?',
        'category': random.choice(categories),
        'difficulty': random.choice(difficulties),
        'points': random.choice([100, 200, 300, 400, 500]),
        'flag': f'FLAG{{dummy_flag_for_q{question_num}}}',
        'hints': [
            f'Hint 1 for Q{question_num}',
            f'Hint 2 for Q{question_num}'
        ],
        'files': [],
        'solved_by': [],
        'total_attempts': random.randint(0, 50),
        'successful_attempts': random.randint(0, 20),
        'created_at': firestore.SERVER_TIMESTAMP,
        'updated_at': firestore.SERVER_TIMESTAMP,
        'author': 'Admin',
        'is_active': True,
        'max_attempts': 0,  # 0 means unlimited
        'time_limit': None,
        'requirements': [],
        'tags': [f'tag{random.randint(1,5)}', f'tag{random.randint(6,10)}']
    }
    
    # If we have a template, ensure we match its structure
    if template:
        template_keys = template.keys()
        data = {k: v for k, v in data.items() if k in template_keys}
        for key in template_keys:
            if key not in data:
                data[key] = template[key]
    
    return data

def add_dummy_questions(db):
    """Add dummy questions from Q11 to Q37"""
    try:
        # Get existing question structure
        template = get_existing_question_structure(db)
        if template:
            print("Found existing question structure")
        else:
            print("No existing question found, using default structure")
        
        questions_ref = db.collection('questions')
        batch = db.batch()
        count = 0
        
        # Generate and add dummy questions
        for i in range(11, 38):
            question_id = f'Q{i}'
            doc_ref = questions_ref.document(question_id)
            
            # Generate dummy data
            data = generate_dummy_question(i, template)
            
            # Add to batch
            batch.set(doc_ref, data, merge=True)
            count += 1
            print(f"Added dummy question {question_id}")
            
            # Commit batch every 500 operations (Firestore limit)
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit any remaining operations
        if count % 500 != 0:
            batch.commit()
            
        print(f"\nSuccessfully added {count} dummy questions to database")
        return True
    except Exception as e:
        print(f"Error adding dummy questions: {str(e)}")
        return False

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    if not db:
        print("Failed to initialize Firebase. Exiting...")
        return
    
    # Add dummy questions
    print("\nAdding dummy questions...")
    if add_dummy_questions(db):
        print("\nDummy questions successfully added to database!")
    else:
        print("\nFailed to add dummy questions")

if __name__ == "__main__":
    main()
