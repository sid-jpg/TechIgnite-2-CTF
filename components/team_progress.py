import streamlit as st
from firebase_admin import firestore

def show_team_progress(db, team_id):
    """Show team's progress including solved questions and total count"""
    try:
        # Get team data
        team_doc = db.collection('Teams').document(team_id).get()
        if not team_doc.exists:
            st.error(f"Team {team_id} not found!")
            return
        
        team_data = team_doc.to_dict()
        total_solved = team_data.get('totalCount', 0)
        questions_solved = team_data.get('questionsSolved', [])
        
        # Display progress
        st.subheader("🏆 Team Progress")
        
        # Show total count with a large number
        st.metric("Questions Solved", total_solved)
        
        # Show solved questions
        if questions_solved:
            st.write("✅ Solved Questions:")
            # Sort questions by ID
            questions_solved.sort()
            # Create a grid of solved questions
            cols = st.columns(5)
            for idx, qid in enumerate(questions_solved):
                with cols[idx % 5]:
                    st.success(qid)
        else:
            st.info("No questions solved yet. Keep trying! 💪")
            
    except Exception as e:
        st.error(f"Error loading team progress: {str(e)}")

def handle_flag_submission_ui(db, team_id, qid, flag):
    """Handle flag submission with UI feedback"""
    from utils.handle_submission import handle_flag_submission
    
    with st.spinner("Verifying flag..."):
        success, message = handle_flag_submission(db, team_id, qid, flag)
        
    if success:
        # Show success message with animation
        st.balloons()  # Show celebration animation
        st.success(message)
    else:
        # Show error message
        st.error(message)
        
    # Refresh team progress
    show_team_progress(db, team_id)
