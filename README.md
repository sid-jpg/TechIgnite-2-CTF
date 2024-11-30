# TechIgnite CTF Platform

A secure Capture The Flag (CTF) platform built with Streamlit and Firebase.

## 🚀 Features
- Secure Authentication System
- Team-based CTF Platform
- Real-time Flag Submission
- Progress Tracking
- Question Management
- Secure Credential Handling

## 🛠️ Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Firebase Configuration**
   - Create a Firebase project at https://console.firebase.google.com/
   - Generate a new service account key from Project Settings > Service Accounts
   - Create `.streamlit/secrets.toml` with your Firebase credentials:
     ```toml
     [firebase]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "your-private-key-id"
     private_key = "your-private-key"
     client_email = "your-client-email"
     client_id = "your-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "your-cert-url"
     ```

3. **Initialize Database**
   - Place your questions Excel file in the project root
   - Run the database setup script:
     ```bash
     python utils/setup_database.py
     ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📊 Database Structure

### Collections
1. **Questions**
   - `qid`: Question ID (e.g., Q1)
   - `Flag`: The correct flag
   - `solvedBy`: List of teams who solved it

2. **Teams**
   - `teamid`: Team identifier
   - `totalCount`: Number of questions solved
   - `questionsSolved`: List of solved question IDs

3. **Submissions**
   - Tracks all flag submissions with timestamps

## 🔒 Security Notes
- Never commit secrets.toml or any credentials to version control
- Keep your Firebase service account key secure
- Regularly rotate credentials
- Monitor authentication logs
- Use environment-specific secrets in production

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
