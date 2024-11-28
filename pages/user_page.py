import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from manage_db import verify_flag, update_stats, get_db

# Get database instance
db = get_db()

# Apply consistent cyberpunk styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        /* Main container styling */
        .stApp {
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
            color: #00ff9d;
        }
        
        .appview-container .main .block-container {
            padding: 2rem;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
        }
        
        h1 {
            border-bottom: 2px solid #00ff9d;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        
        /* Text elements */
        p, div, span {
            font-family: 'Courier New', monospace;
            color: #b3b3b3;
        }
        
        /* Input fields */
        .stTextInput > div > div {
            background-color: rgba(0, 255, 157, 0.1) !important;
            border: 1px solid #00ff9d !important;
            border-radius: 5px;
            color: #00ff9d !important;
        }
        
        .stTextInput > div > div > input {
            color: #00ff9d !important;
            font-family: 'Courier New', monospace !important;
        }
        
        /* Buttons */
        .stButton > button {
            font-family: 'Orbitron', sans-serif !important;
            background: transparent !important;
            color: #00ff9d !important;
            border: 2px solid #00ff9d !important;
            border-radius: 5px !important;
            padding: 0.5rem 2rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2) !important;
        }
        
        .stButton > button:hover {
            background: #00ff9d !important;
            color: #1a1a2e !important;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.4) !important;
            transform: translateY(-2px);
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            background-color: rgba(0, 255, 157, 0.1) !important;
            border: 1px solid #00ff9d !important;
            border-radius: 5px;
        }
        
        .stSelectbox > div > div > div {
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
        }
        
        /* Radio buttons */
        .stRadio > div {
            background-color: transparent !important;
            border: none !important;
        }
        
        .stRadio label {
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
        }
        
        /* Checkboxes */
        .stCheckbox > div > label {
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
        }
        
        /* Data frames */
        .dataframe {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid #00ff9d !important;
            border-radius: 5px;
            font-family: 'Courier New', monospace !important;
        }
        
        .dataframe th {
            background-color: rgba(0, 255, 157, 0.1) !important;
            color: #00ff9d !important;
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .dataframe td {
            color: #b3b3b3 !important;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: rgba(0, 255, 157, 0.1) !important;
            border: 1px solid #00ff9d !important;
            color: #00ff9d !important;
            border-radius: 5px;
        }
        
        /* Success message */
        .element-container div[data-testid="stMarkdownContainer"] div.stSuccess {
            background: rgba(0, 255, 157, 0.1) !important;
            border: 1px solid #00ff9d !important;
            color: #00ff9d !important;
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Error message */
        .element-container div[data-testid="stMarkdownContainer"] div.stError {
            background: rgba(255, 0, 0, 0.1) !important;
            border: 1px solid #ff0000 !important;
            color: #ff0000 !important;
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: rgba(0, 255, 157, 0.1);
            border: 1px solid #00ff9d;
            border-radius: 5px;
            color: #00ff9d;
            font-family: 'Orbitron', sans-serif;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 255, 157, 0.2);
        }
        
        /* Code blocks */
        .stCodeBlock {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid #00ff9d !important;
            border-radius: 5px;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #00ff9d !important;
        }
        
        /* Metric */
        [data-testid="stMetricValue"] {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff9d !important;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
        }
        
        /* Cards */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

def render():
    st.title("CTF Challenge Submission")
    
    with st.container():
        st.markdown('<div class="submission-form">', unsafe_allow_html=True)
        
        # Form title with icon
        st.markdown('''
            <p class="form-title">
                🚩 Submit Flag
            </p>
        ''', unsafe_allow_html=True)
        
        # Form inputs
        team_id = st.text_input("Team ID", key="team_id", placeholder="Enter your Team ID")
        question_id = st.text_input("Question ID", key="question_id", placeholder="Enter Question ID")
        flag = st.text_input("Flag", key="flag", placeholder="Enter flag in format: FLAG{...}")

        # Submit button
        if st.button("Submit Flag", use_container_width=True):
            if not team_id or not question_id or not flag:
                st.error("Please fill in all fields")
            else:
                # Verify flag
                success, message, points = verify_flag(team_id, question_id, flag)
                if success:
                    st.balloons()
                    st.success(f"🎉 {message}")
                else:
                    if "already solved" in message.lower():
                        st.warning("🔄 Already submitted! You've solved this question before.")
                    else:
                        st.error(f"❌ {message}")
                # Update team statistics
                if success:
                    update_stats(team_id, question_id)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show team progress if team_id is provided
        if team_id:
            show_team_progress(db, team_id)

def show_team_progress(db, team_id):
    """Show team's progress"""
    if team_id:
        team_ref = db.collection('Teams').document(team_id)
        team_doc = team_ref.get()
        
        if team_doc.exists:
            team_data = team_doc.to_dict()
            solved_questions = team_data.get('solvedQuestions', [])
            total_count = team_data.get('totalCount', 0)
            
            st.markdown(f"### Your Progress")
            st.write(f"Total Questions Solved: {total_count}")
            if solved_questions:
                st.write("Solved Questions:")
                st.write(", ".join(solved_questions))
            else:
                st.write("No questions solved yet. Keep trying!")
        else:
            st.warning("Team not found. Please check your team ID.")

if __name__ == "__main__":
    render()
