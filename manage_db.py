import firebase_admin
from firebase_admin import credentials, firestore
import argparse
from datetime import datetime
import streamlit as st

def init_firebase():
    """Initialize Firebase with credentials from service account"""
    if not firebase_admin._apps:
        try:
            # Use the centralized firebase initialization
            from firebase_init import init_firebase as init_firebase_auth
            auth = init_firebase_auth()
            if not auth:
                print("Failed to initialize Firebase Authentication")
                return None
            return firestore.client()
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")
            return None
    return firestore.client()

def get_db():
    """Get Firestore database instance"""
    if 'db' not in st.session_state:
        st.session_state.db = init_firebase()
    return st.session_state.db

def verify_flag(team_id, question_id, submitted_flag):
    """Verify a submitted flag and update stats if correct"""
    db = get_db()
    
    # Check if question exists and flag matches
    question_ref = db.collection('Questions').document(question_id)
    question_doc = question_ref.get()
    
    if not question_doc.exists:
        return False, "Question not found", None
    
    question_data = question_doc.to_dict()
    
    # Check if team has already solved this question
    team_ref = db.collection('Teams').document(team_id)
    team_doc = team_ref.get()
    
    if not team_doc.exists:
        return False, "Team not found", None
        
    team_data = team_doc.to_dict()
    if question_id in team_data.get('solvedQuestions', []):
        return False, "You've already solved this question!", None
        
    # Verify flag
    if question_data.get('flag') != submitted_flag:
        # Record wrong submission
        record_submission(team_id, question_id, False)
        return False, "Incorrect flag. Keep trying!", None
    
    # Update statistics for correct submission
    success = update_stats(team_id, question_id)
    if success:
        # Record successful submission
        record_submission(team_id, question_id, True)
        return True, " Congratulations! Flag captured successfully! ", question_data.get('points', 0)
    
    return False, "Error updating statistics", None

def update_stats(team_id, question_id):
    """Update team and question statistics after successful flag submission"""
    db = get_db()
    current_time = datetime.now()
    
    # Update team stats
    team_ref = db.collection('Teams').document(team_id)
    team_doc = team_ref.get()
    
    if not team_doc.exists:
        return False
    
    team_data = team_doc.to_dict()
    
    # Initialize if not exists
    if 'solvedQuestions' not in team_data:
        team_data['solvedQuestions'] = []
    if 'totalCount' not in team_data:
        team_data['totalCount'] = 0
    
    # Update team's solved questions and count
    if question_id not in team_data['solvedQuestions']:
        team_data['solvedQuestions'].append(question_id)
        team_data['totalCount'] = len(team_data['solvedQuestions'])
        team_data['timestamp'] = current_time
        team_ref.set(team_data)
        
        # Update question's solved_by list
        question_ref = db.collection('Questions').document(question_id)
        question_doc = question_ref.get()
        
        if question_doc.exists:
            question_data = question_doc.to_dict()
            if 'solvedBy' not in question_data:
                question_data['solvedBy'] = []
            
            if team_id not in question_data['solvedBy']:
                question_data['solvedBy'].append(team_id)
                question_ref.set(question_data)
        
        return True
    
    return False

def record_submission(team_id, question_id, is_correct):
    """Record submission details"""
    db = get_db()
    db.collection('Submissions').add({
        'teamId': team_id,
        'questionId': question_id,
        'timestamp': datetime.now(),
        'isCorrect': is_correct
    })

# Initialize database with teams and questions
def init_database():
    """Initialize database with teams and questions"""
    db = get_db()
    
    # Add teams
    teams = [
        {'teamId': f'TEAM{i}', 'solvedQuestions': [], 'totalCount': 0, 'timestamp': None}
        for i in range(1, 11)
    ]
    
    # Sample flags for questions
    flags = [
        'CTF{welcome_to_techignite}',
        'CTF{basic_crypto_solved}',
        'CTF{web_exploitation_master}',
        'CTF{reverse_engineering_pro}',
        'CTF{binary_analysis_expert}',
        'CTF{network_security_guru}',
        'CTF{forensics_investigator}',
        'CTF{pwn_master_flex}',
        'CTF{crypto_wizard_supreme}',
        'CTF{final_boss_defeated}'
    ]
    
    # Add questions
    questions = [
        {'qid': f'Q{i}', 'flag': flags[i-1], 'solvedBy': []}
        for i in range(1, 11)
    ]
    
    # Batch write teams
    for team in teams:
        team_ref = db.collection('Teams').document(team['teamId'])
        team_ref.set(team)
    
    # Batch write questions
    for question in questions:
        question_ref = db.collection('Questions').document(question['qid'])
        question_ref.set(question)
    
    print("Database initialized with teams and questions!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='Initialize database')
    
    args = parser.parse_args()
    
    if args.init:
        init_database()

if __name__ == "__main__":
    main()
