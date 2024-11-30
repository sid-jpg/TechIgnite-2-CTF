import streamlit as st
from components.team_progress import show_team_progress, handle_flag_submission_ui

def show_ctf_page(db):
    """Display the CTF challenges page"""
    st.markdown("<h1>🚩 CTF Challenges</h1>", unsafe_allow_html=True)
    
    # Get team ID from session
    team_id = st.session_state.get("team_id")
    if not team_id:
        st.error("Please select your team first!")
        return
    
    # Show team progress
    show_team_progress(db, team_id)
    
    # Flag submission form
    st.markdown("### 🎯 Submit Flag")
    with st.form("flag_submission"):
        qid = st.text_input("Question ID", placeholder="Enter question ID (e.g., Q1)")
        flag = st.text_input("Flag", placeholder="Enter flag exactly as is (e.g., FLAG{...})")
        submitted = st.form_submit_button("Submit Flag")
        
        if submitted:
            if not qid or not flag:
                st.error("Please enter both Question ID and Flag!")
            else:
                # Handle submission without any flag modification
                handle_flag_submission_ui(db, team_id, qid, flag)
                
    # Show available questions
    st.markdown("### 📝 Available Questions")
    questions = db.collection('Questions').get()
    
    # Create columns for questions
    cols = st.columns(3)
    for idx, q in enumerate(questions):
        q_data = q.to_dict()
        with cols[idx % 3]:
            solved = team_id in q_data.get('solvedBy', [])
            status = "✅" if solved else "❌"
            st.markdown(f"""
                <div style='background: rgba(0, 255, 157, 0.1); 
                           padding: 1rem; 
                           border-radius: 5px; 
                           border: 1px solid #00ff9d;
                           margin-bottom: 1rem;
                           text-align: center;'>
                    <h4 style='color: #00ff9d; margin: 0;'>{q_data['qid']}</h4>
                    <p style='color: #b3b3b3; margin: 0.5rem 0;'>Status: {status}</p>
                </div>
            """, unsafe_allow_html=True)
