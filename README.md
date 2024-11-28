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

3. Configure Firebase Credentials
   - Copy `secrets_template.toml` to `.streamlit/secrets.toml`
   - Add your Firebase service account credentials to `.streamlit/secrets.toml`
   - Make sure to replace all placeholder values with your actual Firebase configuration

4. Run the application
```bash
streamlit run app.py
```

## Important Notes

- Never commit `.streamlit/secrets.toml` to version control
- Keep your Firebase service account key secure
- Use environment variables for production deployment

## Security Considerations

- Store sensitive credentials in `.streamlit/secrets.toml`
- Follow the template in `secrets_template.toml`
- Ensure `.gitignore` is properly configured
- Never expose Firebase credentials in public repositories

## License

MIT License
