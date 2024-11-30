import firebase_admin
from firebase_admin import credentials, firestore

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
        
        # Get the flag and clean it the same way as in setup_database.py
        question_data = question.to_dict()
        correct_flag = question_data.get('Flag')
        
        # Clean submitted flag the same way as stored flag
        submitted_flag = str(submitted_flag).strip()
        submitted_flag = submitted_flag.replace('\n', '').replace('\r', '')
        
        # Direct comparison
        if submitted_flag != correct_flag:
            return False, "Incorrect flag. Keep trying!"
            
        # If flag is correct, update solvedBy array
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
                    team_ref.update({
                        'questionsSolved': questions_solved,
                        'totalCount': len(questions_solved)
                    })
            
        return True, "Flag is correct! 🎉"
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, "Error processing submission"
