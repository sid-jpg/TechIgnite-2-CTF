import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from manage_db import verify_flag, update_stats, get_db
from auth import login_required

# Get database instance
db = get_db()

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --bg-color: #1a1a1a;
        --card-bg: rgba(30, 30, 30, 0.95);
        --text-color: #e0e0e0;
        --input-bg: #2d2d2d;
        --input-border: #3d3d3d;
        --input-focus: #4a4a4a;
        --button-gradient: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%);
        --shadow-color: rgba(0, 0, 0, 0.3);
    }

    /* Modern form styling */
    .submission-form {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 2.5rem 3rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px var(--shadow-color);
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Form title */
    .form-title {
        text-align: center;
        margin-bottom: 2rem;
        color: var(--text-color);
        font-size: 1.8rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 1px solid var(--input-border);
        background: var(--input-bg);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff4b4b;
        box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.15);
        background: var(--input-focus);
    }
    
    /* Labels */
    .stTextInput > label {
        color: var(--text-color);
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Submit button */
    .stButton > button {
        width: 100%;
        margin-top: 1.5rem;
        padding: 0.75rem 0;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        background: var(--button-gradient);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25);
        filter: brightness(1.1);
    }
    
    /* Success/Error messages */
    .stAlert {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 8px;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--text-color);
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Placeholder text */
    input::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }
    
    /* Dark theme background */
    .stApp {
        background: var(--bg-color);
    }
</style>
""", unsafe_allow_html=True)

# Additional security for flag protection
st.markdown("""
    <script>
        // Obfuscate and protect flag data
        (function() {
            // Override JSON.stringify to prevent flag exposure
            const originalStringify = JSON.stringify;
            JSON.stringify = function(obj) {
                if (obj && typeof obj === 'object') {
                    const sanitized = {...obj};
                    if ('flag' in sanitized) {
                        sanitized.flag = '[PROTECTED]';
                    }
                    return originalStringify(sanitized);
                }
                return originalStringify(obj);
            };
            
            // Prevent debugging and console usage
            setInterval(() => {
                const startTime = performance.now();
                debugger;
                const endTime = performance.now();
                if (endTime - startTime > 100) {
                    window.location.reload();
                }
            }, 1000);
            
            // Clear and disable console
            console.clear();
            console.debug = console.info = console.log = console.warn = console.error = function() {};
            
            // Prevent flag extraction from memory
            window.addEventListener('beforeunload', function() {
                localStorage.clear();
                sessionStorage.clear();
            });
        })();
        
        // Additional anti-debugging
        (() => {
            function block() {
                if (window.outerHeight - window.innerHeight > 200 || 
                    window.outerWidth - window.innerWidth > 200) {
                    document.body.innerHTML = 'Security violation detected!';
                }
            }
            setInterval(block, 500);
        })();
    </script>
""", unsafe_allow_html=True)

@login_required
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

def show_user_page():
    st.markdown("""
        <div class="cyberpunk-container">
            <h1 class="glitch-text">User Dashboard <span class="icon">🎮</span></h1>
            
            <div class="cyberpunk-grid">
                <div class="cyberpunk-card">
                    <h3>Challenge Progress</h3>
                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress" style="width: 60%"></div>
                        </div>
                        <p class="progress-text">60% Complete</p>
                    </div>
                </div>
                
                <div class="cyberpunk-card">
                    <h3>Active Challenges</h3>
                    <ul class="cyber-list">
                        <li class="active">Binary Exploitation</li>
                        <li class="completed">Web Security</li>
                        <li>Cryptography</li>
                    </ul>
                </div>
            </div>
            
            <div class="cyberpunk-stats">
                <div class="stat-card">
                    <span class="stat-value">1337</span>
                    <span class="stat-label">Total Points</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">5</span>
                    <span class="stat-label">Challenges Solved</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">#42</span>
                    <span class="stat-label">Global Rank</span>
                </div>
            </div>
        </div>
        
        <style>
            .cyberpunk-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin: 2rem 0;
            }
            
            .progress-container {
                margin: 1rem 0;
            }
            
            .progress-bar {
                height: 10px;
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid var(--neon-green);
                border-radius: 5px;
                overflow: hidden;
            }
            
            .progress {
                height: 100%;
                background: linear-gradient(90deg, var(--neon-green), var(--neon-blue));
                box-shadow: 0 0 10px var(--neon-green);
            }
            
            .progress-text {
                color: var(--neon-green) !important;
                text-align: right;
                margin-top: 0.5rem;
                font-size: 0.9em;
            }
            
            .cyber-list {
                list-style: none;
                padding: 0;
                margin: 1rem 0;
            }
            
            .cyber-list li {
                padding: 0.5rem 1rem;
                margin: 0.5rem 0;
                border: 1px solid var(--neon-green);
                border-radius: 3px;
                color: var(--text-gray);
                position: relative;
            }
            
            .cyber-list li::before {
                content: '>';
                color: var(--neon-green);
                margin-right: 0.5rem;
            }
            
            .cyber-list li.active {
                border-color: var(--neon-pink);
                color: var(--neon-pink);
            }
            
            .cyber-list li.completed {
                border-color: var(--neon-green);
                color: var(--neon-green);
            }
            
            .cyberpunk-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }
            
            .stat-card {
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid var(--neon-green);
                padding: 1rem;
                text-align: center;
                border-radius: 5px;
                position: relative;
                overflow: hidden;
            }
            
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, var(--neon-green), transparent);
            }
            
            .stat-value {
                display: block;
                font-size: 2em;
                color: var(--neon-green);
                font-family: 'Orbitron', sans-serif;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                color: var(--text-gray);
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            @keyframes pulse {
                0% {
                    box-shadow: 0 0 10px var(--neon-green);
                }
                50% {
                    box-shadow: 0 0 20px var(--neon-green);
                }
                100% {
                    box-shadow: 0 0 10px var(--neon-green);
                }
            }
            
            .stat-card:hover {
                animation: pulse 2s infinite;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
    show_user_page()
