import os
import sys
import docx
import re

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

def clean_question_id(text):
    """Clean question ID to be Firestore-compatible"""
    # Extract question number if it starts with Q
    match = re.match(r'Q(\d+)', text)
    if match:
        return f"Q{match.group(1)}"
    return "Q0"  # Default ID for non-standard questions

def read_flags_from_docx(file_path):
    """Read flags from the Word document"""
    try:
        doc = docx.Document(file_path)
        flags = {}
        
        # Process each paragraph
        for para in doc.paragraphs:
            text = para.text.strip()
            # Skip empty lines
            if not text:
                continue
                
            # Split by dot for question ID and get flag
            parts = text.split('.')
            if len(parts) >= 2:
                raw_id = '.'.join(parts[:-1]).strip()  # Join all parts except last as ID
                flag = parts[-1].strip()  # Last part is the flag
                
                # Clean up the question ID
                question_id = clean_question_id(raw_id)
                
                if question_id and flag:  # Only add if both ID and flag are non-empty
                    flags[question_id] = {
                        'original_id': raw_id,
                        'flag': flag
                    }
                    print(f"Found flag for question {question_id} (Original: {raw_id}): {flag}")
        
        return flags
    except Exception as e:
        print(f"Error reading Word document: {str(e)}")
        return None

def add_flags_to_database(db, flags):
    """Add flags to Firestore database"""
    try:
        questions_ref = db.collection('questions')
        batch = db.batch()
        count = 0
        
        for question_id, data in flags.items():
            doc_ref = questions_ref.document(question_id)
            batch.set(doc_ref, {
                'flag': data['flag'],
                'id': question_id,
                'original_id': data['original_id'],
                'timestamp': firestore.SERVER_TIMESTAMP
            }, merge=True)  # Use merge to update existing documents
            count += 1
            print(f"Added flag for question {question_id} (Original: {data['original_id']})")
            
            # Commit batch every 500 operations (Firestore limit)
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()
        
        # Commit any remaining operations
        if count % 500 != 0:
            batch.commit()
            
        print(f"\nSuccessfully added {count} flags to database")
        return True
    except Exception as e:
        print(f"Error adding flags to database: {str(e)}")
        return False

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    if not db:
        print("Failed to initialize Firebase. Exiting...")
        return
    
    # Path to the Word document
    doc_path = r"C:\Users\a2z\Desktop\CCTTFF\FinalFlags (1).docx"
    
    if not os.path.exists(doc_path):
        print(f"Error: Document not found at {doc_path}")
        return
    
    # Read flags from document
    print("\nReading flags from document...")
    flags = read_flags_from_docx(doc_path)
    
    if not flags:
        print("No flags found in document. Exiting...")
        return
    
    print(f"\nFound {len(flags)} flags in document")
    
    # Add flags to database
    print("\nAdding flags to database...")
    if add_flags_to_database(db, flags):
        print("\nFlags successfully added to database!")
    else:
        print("\nFailed to add flags to database")

if __name__ == "__main__":
    main()
