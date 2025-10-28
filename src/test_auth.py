import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import auth_system

def test_auth():
    print("🧪 Testing Authentication System...")
    
    # Test registration
    success, message = auth_system.register_user("testuser", "testpass", "test@example.com")
    print(f"Registration: {success} - {message}")
    
    # Test login with correct credentials
    success, message = auth_system.login_user("testuser", "testpass")
    print(f"Login (correct): {success} - {message}")
    
    # Test login with wrong credentials
    success, message = auth_system.login_user("testuser", "wrongpass")
    print(f"Login (wrong): {success} - {message}")
    
    # Test getting preferences
    prefs = auth_system.get_user_preferences("testuser")
    print(f"Preferences: {prefs}")

if __name__ == "__main__":
    test_auth()