import streamlit as st
import hashlib
import json
import os

class AuthSystem:
    def __init__(self):
        self.users_file = "data/users.json"
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.users_file):
            # Create with a default test user
            default_users = {
                "test": {
                    'password': self._hash_password("test"),
                    'email': 'test@example.com',
                    'preferences': {
                        'default_location': 'bangalore',
                        'alert_types': ['ISS', 'Meteor', 'Aurora', 'Launch'],
                        'notification_method': 'email'
                    }
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    def _hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Register a new user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            'password': self._hash_password(password),
            'email': email,
            'preferences': {
                'default_location': 'bangalore',
                'alert_types': ['ISS', 'Meteor', 'Aurora', 'Launch'],
                'notification_method': 'email'
            }
        }
        
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            return True, "Registration successful"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, username, password):
        """Login user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, "No users registered yet"
        
        if username in users and users[username]['password'] == self._hash_password(password):
            return True, "Login successful"
        
        return False, "Invalid username or password"
    
    def get_user_preferences(self, username):
        """Get user preferences"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            return users.get(username, {}).get('preferences', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def update_user_preferences(self, username, preferences):
        """Update user preferences"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        
        if username in users:
            users[username]['preferences'] = preferences
            try:
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                return True
            except Exception:
                return False
        return False

# Global auth instance
auth_system = AuthSystem()