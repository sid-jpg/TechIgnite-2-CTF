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
    """Generate question data with appropriate structure"""
    categories = {
        11: 'Web', 12: 'Crypto', 13: 'Network', 14: 'Forensics', 15: 'Malware',
        16: 'Software Development', 17: 'OSINT', 18: 'Science', 19: 'Steganography', 20: 'Misc',
        21: 'Crypto', 22: 'OSINT', 23: 'Misc', 24: 'Steganography', 25: 'Algorithm',
        26: 'Web', 27: 'Math', 28: 'Science', 29: 'Network', 30: 'OSINT',
        31: 'OSINT', 32: 'OSINT', 33: 'OSINT', 34: 'Steganography', 35: 'OSINT',
        36: 'Crypto', 37: 'OSINT'
    }
    
    descriptions = {
        11: "Decode this story carefully",
        12: "Find the hidden message in this image",
        13: "Network analysis challenge",
        14: "Breaking it is rather easy",
        15: "Analyze the malicious code",
        16: "Software architecture question",
        17: "Find the time from social media",
        18: "Black hole physics",
        19: "Hidden in plain sight",
        20: "Can you find the word?",
        21: "Breakfast recipe encoded",
        22: "Social media investigation",
        23: "Solve this riddle",
        24: "Image analysis required",
        25: "Classic algorithm challenge",
        26: "Web exploitation",
        27: "Mathematical sequence",
        28: "Physics calculation",
        29: "MAC address analysis",
        30: "GitHub investigation",
        31: "Date investigation",
        32: "Social media OSINT",
        33: "Location finding",
        34: "Hidden message challenge",
        35: "Time investigation",
        36: "Complex encryption",
        37: "Fire investigation"
    }
    
    points = {
        11: 200, 12: 250, 13: 300, 14: 150, 15: 400,
        16: 250, 17: 200, 18: 350, 19: 200, 20: 150,
        21: 300, 22: 250, 23: 200, 24: 250, 25: 400,
        26: 200, 27: 300, 28: 350, 29: 300, 30: 250,
        31: 200, 32: 250, 33: 300, 34: 250, 35: 200,
        36: 400, 37: 300
    }
    
    data = {
        'category': categories.get(question_num, 'Misc'),
        'description': descriptions.get(question_num, f'Challenge description for Q{question_num}'),
        'difficulty': 'Medium',
        'id': f'Q{question_num}',
        'points': points.get(question_num, 200),
        'solved_by': [],
        'title': f'Challenge {question_num}',
        'total_attempts': 0,
        'type': categories.get(question_num, 'Misc')
    }
    
    return data

def add_questions_to_database(db):
    """Add questions Q11 to Q37 to the database"""
    try:
        questions_ref = db.collection('Questions')
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
            print(f"Added question {question_id} - {data['title']} ({data['category']})")
            
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
