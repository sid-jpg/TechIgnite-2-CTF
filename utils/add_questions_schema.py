import os
import sys

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

def get_flag_data():
    """Get flag data for each question"""
    return {
        'Q1': 'FLAG{base64_is_easy}',
        'Q2': 'FLAG{that_the_fosso}',
        'Q3': 'FLAG{FLAGSAMUELMORSEISCOOLBYTHEWAYILIKECHEES}',
        'Q4': 'FLAG{rgb(160, 50, 50)}',
        'Q5': 'FLAG{1:11}',
        'Q6': 'FLAG{266 kB}',
        'Q7': 'FLAG{galFeruceS}',
        'Q8': 'FLAG{00:00,01:10,12:21,21:12}',
        'Q9': 'FLAG{4,4}',
        'Q10': 'FLAG{Welcome To Tech-Ignite 2:0:)}',
        'Q11': 'FLAG{SeriousStory}',
        'Q12': 'FLAG{3274,0819}',
        'Q13': 'FLAG{192.168.2:99}',
        'Q14': 'FLAG{Breaking_it_is_easy}',
        'Q15': 'FLAG{Trojan_virus}',
        'Q16': 'FLAG{Eric_Evans}',
        'Q17': 'FLAG{10:30}',
        'Q18': 'FLAG{spaghettification}',
        'Q19': 'FLAG{CAPTURE}',
        'Q20': 'FLAG{brat}',
        'Q21': 'FLAG{omlebaconjuicebrewat}',
        'Q22': 'FLAG{oreosurf}',
        'Q23': 'FLAG{wowyouresosmart}',
        'Q24': 'FLAG{Capture it}',
        'Q25': "FLAG{Euclid's Algorithm}",
        'Q26': 'FLAG{welcome_geeks}',
        'Q27': 'FLAG{113}',
        'Q28': 'FLAG{1/200}',
        'Q29': 'FLAG{d0:50:99:82:33:6e}',
        'Q30': 'FLAG{https://github.com/cioaonk}',
        'Q31': 'FLAG{march_2}',
        'Q32': 'FLAG{osint_is_fun}',
        'Q33': 'FLAG{saintpeter}',
        'Q34': 'FLAG{seekandfind}',
        'Q35': 'FLAG{11:00}',
        'Q36': 'FLAG{cNi76bV2IVERlh97hP}',
        'Q37': 'FLAG{ringoffire}'
    }

def get_question_data(qid, flag):
    """Generate question data matching the schema"""
    return {
        'flag': flag,
        'qid': qid,
        'solvedBy': []
    }

def add_questions_to_database(db):
    """Add questions to the database"""
    try:
        questions_ref = db.collection('Questions')
        batch = db.batch()
        count = 0
        
        # Get flag data
        flags = get_flag_data()
        
        # Add questions
        for qid, flag in flags.items():
            doc_ref = questions_ref.document(qid)
            
            # Get question data
            data = get_question_data(qid, flag)
            
            # Add to batch
            batch.set(doc_ref, data, merge=True)
            count += 1
            print(f"Added question {qid} with flag: {flag}")
            
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
    print("\nAdding questions to database...")
    if add_questions_to_database(db):
        print("\nQuestions successfully added to database!")
    else:
        print("\nFailed to add questions")

if __name__ == "__main__":
    main()
