import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def handle_flag_submission(db, team_id, qid, submitted_flag):
    """
    Handle flag submission and update all relevant collections
    Returns: (success, message)
    """
    try:
        # Start a transaction
        transaction = db.transaction()

        @transaction.transaction
        def update_in_transaction(transaction):
            # Get question document
            question_ref = db.collection('Questions').document(qid)
            question = question_ref.get(transaction=transaction)
            
            if not question.exists:
                return False, "Question not found"
            
            question_data = question.to_dict()
            
            # Check if team has already solved this question
            if team_id in question_data.get('solvedBy', []):
                return False, "Your team has already solved this question!"
            
            # Verify flag
            if submitted_flag != question_data.get('Flag'):
                return False, "Incorrect flag. Try again!"
            
            # Get team document
            team_ref = db.collection('Teams').document(team_id)
            team = team_ref.get(transaction=transaction)
            
            if not team.exists:
                return False, "Team not found"
            
            team_data = team.to_dict()
            
            # Update question's solvedBy array
            solved_by = question_data.get('solvedBy', [])
            solved_by.append(team_id)
            transaction.update(question_ref, {
                'solvedBy': solved_by
            })
            
            # Update team's data
            questions_solved = team_data.get('questionsSolved', [])
            questions_solved.append(qid)
            transaction.update(team_ref, {
                'questionsSolved': questions_solved,
                'totalCount': len(questions_solved) + 1
            })
            
            # Add to submissions collection
            submission_ref = db.collection('submissions').document()
            transaction.set(submission_ref, {
                'teamid': team_id,
                'qid': qid,
                'timestamp': datetime.now()
            })
            
            return True, "Congratulations! Flag is correct!"
        
        # Execute transaction
        success, message = update_in_transaction(transaction)
        return success, message
    
    except Exception as e:
        return False, f"Error processing submission: {str(e)}"
