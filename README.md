# TechIgnite CTF Platform

A Streamlit-based Cybersecurity Competition Platform with Firebase integration.

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/techignite-ctf.git
cd techignite-ctf
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Firebase Setup
   1. Go to [Firebase Console](https://console.firebase.google.com)
   2. Create a new project or select existing project
   3. Enable Authentication:
      - Go to Authentication > Sign-in method
      - Enable Email/Password provider
   4. Get Admin SDK credentials:
      - Go to Project Settings > Service accounts
      - Click "Generate new private key"
      - Save the JSON file securely
   5. Get Web API credentials:
      - Go to Project Settings > General
      - Under "Your apps", click web icon (</>) to add a web app
      - Register app and get configuration
   6. Configure credentials:
      - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
      - Update Firebase Admin SDK credentials from the downloaded JSON
      - Update Web API credentials from the Firebase console
      - Ensure all placeholders are replaced with actual values

4. Run the application
```bash
streamlit run app.py
```

## Configuration Troubleshooting

### Common Issues:

1. Invalid API Key:
   - Check Web API key in Firebase Console
   - Ensure API key is not restricted
   - Verify apiKey in `.streamlit/secrets.toml`

2. Authentication Failed:
   - Verify all credentials in `.streamlit/secrets.toml`
   - Check if Firebase Authentication is enabled
   - Ensure private key is properly formatted

3. Initialization Errors:
   - Verify project ID matches in both Admin SDK and Web configs
   - Check if all required fields are present in `.streamlit/secrets.toml`
   - Ensure databaseURL is correct

## Security Best Practices

- Never commit `.streamlit/secrets.toml` to version control
- Keep your Firebase service account key secure
- Use environment variables for production deployment
- Regularly rotate credentials
- Monitor Firebase Console for unusual activity
- Set up proper Firebase Security Rules

## Development Guidelines

1. Local Development:
   - Use separate Firebase project for development
   - Keep development credentials separate
   - Test with minimal privileges first

2. Production Deployment:
   - Use production Firebase project
   - Set up proper security rules
   - Enable monitoring and logging
   - Use secure environment variables

## License

MIT License
