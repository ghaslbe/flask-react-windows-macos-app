"""
Test script to verify the application works before building exe
"""
import sqlite3
import os
import tempfile
import requests
import threading
import time
from app_exe import app, init_db, DATABASE

def test_database():
    """Test database operations"""
    print("Testing database operations...")
    
    # Initialize database
    init_db()
    
    # Test connection
    with sqlite3.connect(DATABASE) as conn:
        # Insert test user
        user_id = "test-123"
        conn.execute('INSERT INTO users (id, vorname, nachname) VALUES (?, ?, ?)',
                     (user_id, 'Test', 'User'))
        conn.commit()
        
        # Retrieve user
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        assert user is not None, "User not found"
        assert user[1] == 'Test', "Wrong vorname"
        assert user[2] == 'User', "Wrong nachname"
        
        # Clean up
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
    
    print("✓ Database operations working")

def test_flask_app():
    """Test Flask app in a separate thread"""
    print("Testing Flask application...")
    
    # Start Flask in a thread
    def run_app():
        app.run(host='127.0.0.1', port=5001, debug=False)
    
    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = 'http://127.0.0.1:5001'
    
    try:
        # Test home page
        response = requests.get(f'{base_url}/')
        assert response.status_code == 200, f"Home page failed: {response.status_code}"
        assert 'Benutzerverwaltung' in response.text, "Home page content incorrect"
        
        # Test API - get users
        response = requests.get(f'{base_url}/api/users')
        assert response.status_code == 200, f"Get users failed: {response.status_code}"
        users = response.json()
        assert isinstance(users, list), "Users endpoint should return list"
        
        # Test API - create user
        user_data = {'vorname': 'API', 'nachname': 'Test'}
        response = requests.post(f'{base_url}/api/users', json=user_data)
        assert response.status_code == 201, f"Create user failed: {response.status_code}"
        created_user = response.json()
        user_id = created_user['id']
        
        # Test API - update user
        update_data = {'vorname': 'Updated', 'nachname': 'User'}
        response = requests.put(f'{base_url}/api/users/{user_id}', json=update_data)
        assert response.status_code == 200, f"Update user failed: {response.status_code}"
        
        # Test API - delete user
        response = requests.delete(f'{base_url}/api/users/{user_id}')
        assert response.status_code == 200, f"Delete user failed: {response.status_code}"
        
        print("✓ Flask application working")
        return True
        
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("Testing User Management Application")
    print("=" * 50)
    
    try:
        test_database()
        flask_success = test_flask_app()
        
        print("\n" + "=" * 50)
        if flask_success:
            print("✅ All tests passed! Application is ready for EXE build.")
        else:
            print("❌ Some tests failed. Please check the Flask application.")
        print("=" * 50)
        
        return flask_success
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        print("=" * 50)
        return False

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)