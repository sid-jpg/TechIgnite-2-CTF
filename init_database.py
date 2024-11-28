import firebase_admin
from firebase_admin import credentials, firestore
import json
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

# Initialize Firebase
db = init_firebase()
if db is None:
    print("Failed to initialize Firebase. Exiting.")
    exit(1)

def init_database():
    # Sample data for demonstration
    sample_teams = [
        {
            "team_id": "team1",
            "total_ques_solved": 0,
            "ques_id": []
        },
        {
            "team_id": "team2",
            "total_ques_solved": 0,
            "ques_id": []
        }
    ]

    sample_questions = [
        {
            "q_id": "q1",
            "Flag": "flag{this_is_question_1}",
            "solved_by": []
        },
        {
            "q_id": "q2",
            "Flag": "flag{this_is_question_2}",
            "solved_by": []
        }
    ]

    # Initialize Teams collection
    teams_ref = db.collection('Teams')
    for team in sample_teams:
        doc_ref = teams_ref.document(team["team_id"])
        doc_ref.set({
            "total_ques_solved": team["total_ques_solved"],
            "ques_id": team["ques_id"]
        })
        print(f"Added team: {team['team_id']}")

    # Initialize Questions collection
    questions_ref = db.collection('Questions')
    for question in sample_questions:
        doc_ref = questions_ref.document(question["q_id"])
        doc_ref.set({
            "Flag": question["Flag"],
            "solved_by": question["solved_by"]
        })
        print(f"Added question: {question['q_id']}")

def clear_database():
    # Delete all documents in Teams collection
    teams_ref = db.collection('Teams')
    for doc in teams_ref.stream():
        doc.reference.delete()
        print(f"Deleted team: {doc.id}")

    # Delete all documents in Questions collection
    questions_ref = db.collection('Questions')
    for doc in questions_ref.stream():
        doc.reference.delete()
        print(f"Deleted question: {doc.id}")

if __name__ == "__main__":
    # First clear the existing data
    print("Clearing existing data...")
    clear_database()
    
    # Then initialize with new data
    print("\nInitializing database with sample data...")
    init_database()
    print("\nDatabase initialization complete!")
