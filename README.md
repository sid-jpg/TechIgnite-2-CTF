# TechIgnite CTF Platform

A secure, real-time Capture The Flag (CTF) competition platform built with Streamlit and Firebase.

## Features

- Secure flag submission system
- Team-based competition
- Real-time admin dashboard
- Firebase authentication
- Responsive design
- Anti-debugging protections

## Local Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Firebase:
   - Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Email/Password authentication
   - Create a service account and download credentials
   - Add your credentials to Streamlit secrets (see below)

3. Configure Streamlit secrets:
   - Create `.streamlit/secrets.toml` using the template in `secrets_template.toml`
   - Add your Firebase credentials from the service account JSON
   - Add your Firebase web configuration

4. Run the application:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Fork this repository

2. Create a new app on [Streamlit Cloud](https://share.streamlit.io/)

3. Connect your forked repository

4. Add the following secrets in Streamlit Cloud settings:
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

   [firebase_web]
   apiKey = "your-api-key"
   authDomain = "your-project-id.firebaseapp.com"
   projectId = "your-project-id"
   storageBucket = "your-project-id.appspot.com"
   messagingSenderId = "your-sender-id"
   appId = "your-app-id"
   databaseURL = ""
   ```

5. Deploy! 

## Security Notes

- Never commit sensitive credentials to Git
- Keep your Firebase service account key secure
- Regularly rotate admin credentials
- Monitor authentication logs

## License

MIT License
