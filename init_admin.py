import firebase_admin
from firebase_admin import firestore
from firebase_init import get_db

def init_admin_collection():
    """Initialize the admins collection with a default admin user"""
    try:
        # Get Firestore database instance
        db = get_db()
        
        # Reference to admins collection
        admins_ref = db.collection('admins')
        
        # Check if admin already exists
        existing_admin = admins_ref.where('username', '==', 'admin').get()
        
        if not existing_admin:
            # Create default admin user
            admin_data = {
                'username': 'admin',
                'password': 'Admin!123'  # You should change this password
            }
            
            # Add admin to collection
            admins_ref.add(admin_data)
            print("Admin user created successfully!")
            print("Default credentials:")
            print("Username: admin")
            print("Password: admin123")
            print("\nPlease change these credentials after first login!")
        else:
            print("Admin user already exists!")
    except Exception as e:
        print(f"Error initializing admin collection: {str(e)}")

if __name__ == "__main__":
    init_admin_collection()
ing: