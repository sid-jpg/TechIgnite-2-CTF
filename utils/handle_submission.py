import firebase_admin
from firebase_admin import credentials, firestore

def handle_flag_submission(db, team_id, qid, submitted_flag):
    """
    Handle flag submission and update solvedBy field if flag is correct
    Returns: (success, message)
    """
    try:
        # Convert qid to uppercase and ensure it starts with Q
        qid = qid.strip().upper()
        if not qid.startswith('Q'):
            qid = 'Q' + qid
            
        # Get question document
        question_ref = db.collection('Questions').document(qid)
        question = question_ref.get()
        
        if not question.exists:
            print(f"Question {qid} not found")
            return False, "Question not found"
        
        # Get the flag from database
        question_data = question.to_dict()
        correct_flag = question_data.get('Flag')  # Capital F!
        
        print(f"Debug Info:")
        print(f"Question ID: {qid}")
        print(f"Submitted Flag: '{submitted_flag}'")
        print(f"Correct Flag: '{correct_flag}'")
        
        # Direct string comparison without any modifications
        if submitted_flag != correct_flag:
            print("Flags don't match!")
            return False, "Incorrect flag. Keep trying!"
            
        print("Flags match! Updating solvedBy...")
        
        # Update solvedBy array
        solved_by = question_data.get('solvedBy', [])
        if team_id not in solved_by:
            solved_by.append(team_id)
            question_ref.update({
                'solvedBy': solved_by
            })
            
            # Update team's progress
            team_ref = db.collection('Teams').document(team_id)
            team = team_ref.get()
            if team.exists:
                team_data = team.to_dict()
                questions_solved = team_data.get('questionsSolved', [])
                if qid not in questions_solved:
                    questions_solved.append(qid)
                    questions_solved.sort()  # Keep questions sorted
                    team_ref.update({
                        'questionsSolved': questions_solved,
                        'totalCount': len(questions_solved)
                    })
            
        return True, "Flag is correct! 🎉"
        
    except Exception as e:
        print(f"Error in handle_flag_submission: {str(e)}")
        return False, "Error processing submission"
