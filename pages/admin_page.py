import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from manage_db import get_db
from google.cloud.firestore import Query
from auth import login_required, logout

# Initialize Firebase
db = get_db()

# Initialize session state for auto-refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30

# Disable right click
st.markdown("""
    <script>
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || 
                (e.ctrlKey && e.shiftKey && e.key === 'I') || 
                (e.ctrlKey && e.shiftKey && e.key === 'J') || 
                (e.ctrlKey && e.key === 'U')) {
                e.preventDefault();
            }
        });
    </script>
""", unsafe_allow_html=True)

def get_team_stats():
    """Get team statistics from Firebase"""
    teams_ref = db.collection('Teams').stream()
    questions_ref = db.collection('Questions').stream()
    
    # Count total questions
    total_questions = len([q for q in questions_ref])
    
    team_data = []
    for team in teams_ref:
        data = team.to_dict()
        solved_questions = data.get('solvedQuestions', [])
        timestamp = data.get('timestamp')
        
        team_data.append({
            'TeamID': team.id,
            'Questions Solved': ', '.join(solved_questions) if solved_questions else 'None',
            'Total Solved': data.get('totalCount', 0),
            'Last Solve': timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'No solves yet',
            'Progress': f"{len(solved_questions)}/{total_questions} questions"
        })
    
    return pd.DataFrame(team_data)

def show_submission_history():
    """Show recent flag submission history"""
    submissions_ref = db.collection('Submissions').order_by(
        'timestamp', 
        direction=Query.DESCENDING
    ).limit(10).stream()
    
    submission_data = []
    for sub in submissions_ref:
        data = sub.to_dict()
        submission_data.append({
            'Team': data.get('teamId'),
            'Question': data.get('questionId'),
            'Status': ' Correct' if data.get('isCorrect') else ' Wrong',
            'Time': data.get('timestamp').strftime('%H:%M:%S')
        })
    
    return pd.DataFrame(submission_data)

@login_required
def render():
    st.markdown('<h1 style="text-align: center;"> CTF Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("Dashboard Controls")
        
        # Add logout button at the top
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.experimental_rerun()
            
        st.divider()  # Add a visual separator
        
        st.session_state.auto_refresh = st.checkbox("Auto Refresh", value=st.session_state.auto_refresh)
        if st.session_state.auto_refresh:
            st.session_state.refresh_interval = st.slider(
                "Refresh Interval (seconds)",
                min_value=5,
                max_value=60,
                value=st.session_state.refresh_interval
            )
        
        # Show last refresh time
        st.write(f"Last refreshed: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    # Auto refresh logic
    if st.session_state.auto_refresh:
        current_time = datetime.now()
        if (current_time - st.session_state.last_refresh).total_seconds() >= st.session_state.refresh_interval:
            st.session_state.last_refresh = current_time
            st.experimental_rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(" Team Progress")
        teams_df = get_team_stats()
        if not teams_df.empty:
            st.dataframe(
                teams_df.sort_values('Total Solved', ascending=False),
                use_container_width=True,
                height=400
            )
        else:
            st.info("No team data available")
    
    with col2:
        st.subheader(" Recent Submissions")
        submissions_df = show_submission_history()
        if not submissions_df.empty:
            st.dataframe(submissions_df, use_container_width=True)
        else:
            st.info("No submissions yet")
    
    # Solve distribution chart
    st.subheader(" Question Solve Distribution")
    questions_ref = db.collection('Questions').stream()
    question_data = []
    
    for q in questions_ref:
        data = q.to_dict()
        question_data.append({
            'Question': q.id,
            'Solves': len(data.get('solvedBy', []))
        })
    
    if question_data:
        q_df = pd.DataFrame(question_data)
        fig = px.bar(
            q_df,
            x='Question',
            y='Solves',
            title='Question Solve Distribution',
            color='Solves',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render()
