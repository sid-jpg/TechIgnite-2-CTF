import sys
import pkg_resources
import firebase_admin
import streamlit as st

def check_python_version():
    print(f"Python Version: {sys.version}")
    required_version = "3.9.18"
    if sys.version.startswith("3.9"):
        print("✅ Python version is compatible")
    else:
        print("❌ Python version mismatch. Please use Python 3.9.x")

def check_packages():
    required_packages = {
        'streamlit': '1.24.0',
        'firebase-admin': '6.2.0',
        'pandas': '1.5.3',
        'numpy': '1.24.3'
    }
    
    for package, version in required_packages.items():
        try:
            installed = pkg_resources.get_distribution(package)
            if installed.version == version:
                print(f"✅ {package} version {version} is correctly installed")
            else:
                print(f"❌ {package} version mismatch. Required: {version}, Installed: {installed.version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} is not installed")

def check_firebase():
    try:
        if not firebase_admin._apps:
            cred = st.secrets["firebase"]
            firebase_admin.initialize_app(cred)
        print("✅ Firebase initialization successful")
    except Exception as e:
        print(f"❌ Firebase initialization failed: {str(e)}")

if __name__ == "__main__":
    print("=== Deployment Environment Check ===")
    check_python_version()
    print("\n=== Package Version Check ===")
    check_packages()
    print("\n=== Firebase Configuration Check ===")
    check_firebase()
