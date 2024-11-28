# TechIgnite CTF Platform

A secure Capture The Flag (CTF) platform built with Streamlit and Firebase.

## 🚀 Features
- Secure Authentication System
- Admin Dashboard
- User Management
- Challenge Management
- Real-time Scoring
- Secure File Handling

## 🛠️ Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Firebase Configuration**
   - Copy `config_template.py` to `config.py`
   - Fill in your Firebase credentials in `config.py`
   - Place your Firebase service account JSON file in the project root
   - Update the path in `firebase_init.py`

3. **Streamlit Configuration**
   - Create `.streamlit/secrets.toml` from the template
   - Add your Firebase configuration

4. **Initialize Admin**
   ```bash
   python init_admin.py
   ```
   - Default admin credentials:
     - Username: admin
     - Password: admin123
   - **Important**: Change these credentials after first login!

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 🔒 Security Notes
- Never commit sensitive credentials to version control
- Change default admin credentials immediately
- Keep your service account key secure
- Regularly update dependencies
- Monitor authentication logs

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
