import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handle_flag_submission(db, team_id: str, qid: str, flag: str) -> Tuple[bool, str]:
    """
    Handle flag submission with exact matching
    
    Args:
        db: Firestore database instance
        team_id: Team ID submitting the flag
        qid: Question ID (e.g., 'Q1')
        flag: Flag string exactly as submitted
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        # Log submission attempt
        logger.debug(f"Flag submission attempt - Team: {team_id}, QID: {qid}, Flag: {flag}")
        
        # Clean up question ID only (preserve flag exactly as is)
        qid = qid.strip().upper()
        if not qid.startswith('Q'):
            qid = 'Q' + qid
            
        # Get question document
        question_ref = db.collection('Questions').document(qid)
        question = question_ref.get()
        
        # Validate question exists
        if not question.exists:
            logger.warning(f"Question {qid} not found")
            return False, f"Question {qid} not found"
            
        # Get question data
        q_data = question.to_dict()
        
        # Check if team already solved
        if team_id in q_data.get('solvedBy', []):
            logger.info(f"Team {team_id} already solved {qid}")
            return False, "You have already solved this question!"
            
        # Get correct flag
        correct_flag = q_data.get('Flag')
        if not correct_flag:
            logger.error(f"No flag found for question {qid}")
            return False, "Internal error: No flag found for this question"
            
        # Log flag comparison details
        logger.debug(f"Flag comparison - Submitted: '{flag}' (len: {len(flag)}), Correct: '{correct_flag}' (len: {len(correct_flag)})")
        
        # Exact flag comparison
        if flag != correct_flag:
            logger.info(f"Incorrect flag submitted for {qid}")
            return False, "Incorrect flag"
            
        # Update question's solvedBy array
        question_ref.update({
            'solvedBy': db.field_path('solvedBy').arrayUnion([team_id])
        })
        
        # Update team's progress
        team_ref = db.collection('Teams').document(team_id)
        team_ref.update({
            'questionsSolved': db.field_path('questionsSolved').arrayUnion([qid]),
            'totalCount': db.field_path('totalCount').increment(1)
        })
        
        logger.info(f"Team {team_id} successfully solved {qid}")
        return True, "Correct flag! Question solved!"
        
    except Exception as e:
        logger.error(f"Error in handle_flag_submission: {str(e)}", exc_info=True)
        return False, f"Internal error: {str(e)}"
