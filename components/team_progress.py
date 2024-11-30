import streamlit as st
from firebase_admin import firestore
from utils.handle_submission import handle_flag_submission

def show_team_progress(db, team_id):
    """Show team's progress"""
    # Get team data
    team_ref = db.collection('Teams').document(team_id)
    team = team_ref.get()
    
    if not team.exists:
        st.error("Team not found!")
        return
        
    team_data = team.to_dict()
    questions_solved = team_data.get('questionsSolved', [])
    total_solved = team_data.get('totalCount', 0)
    
    # Display progress
    st.markdown(f"### 📊 Team Progress")
    st.markdown(f"**Team ID:** {team_id}")
    st.markdown(f"**Questions Solved:** {total_solved}")
    
    if questions_solved:
        st.markdown("**Solved Questions:**")
        # Create a grid layout for solved questions
        cols = st.columns(5)  # 5 questions per row
        for idx, qid in enumerate(sorted(questions_solved)):
            cols[idx % 5].markdown(f"✅ {qid}")
    else:
        st.info("No questions solved yet. Keep trying! 💪")

def handle_flag_submission_ui(db, team_id, qid, flag):
    """Handle flag submission and show UI feedback"""
    success, message = handle_flag_submission(db, team_id, qid, flag)
    
    if success:
        st.balloons()  # Show celebration animation
        st.success(message)
        # Update progress display
        show_team_progress(db, team_id)
    else:
        st.error(message)
