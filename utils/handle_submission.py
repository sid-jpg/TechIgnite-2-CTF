import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def handle_flag_submission(db, team_id, qid, submitted_flag):
    """
    Handle flag submission and update solvedBy field if flag is correct
    Returns: (success, message)
    """
    try:
        # Get question document
        question_ref = db.collection('Questions').document(qid)
        question = question_ref.get()
        
        if not question.exists:
            return False, "Question not found"
        
        question_data = question.to_dict()
        correct_flag = question_data.get('Flag')
        
        # Simple direct comparison
        if submitted_flag != correct_flag:
            return False, "Incorrect flag"
            
        # If flag is correct, update solvedBy array
        solved_by = question_data.get('solvedBy', [])
        if team_id not in solved_by:
            solved_by.append(team_id)
            question_ref.update({
                'solvedBy': solved_by
            })
            
        return True, "Flag is correct!"
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, "Error processing submission"
