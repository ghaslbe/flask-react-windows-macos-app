import sqlite3
import uuid
import os
import sys
import threading
import webbrowser
import time
import platform
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

def get_database_path():
    """Get the appropriate database path for the current OS"""
    app_name = "Benutzerverwaltung"
    
    # Get user's home directory
    home_dir = os.path.expanduser("~")
    
    if platform.system() == "Windows":
        # Windows: %USERPROFILE%\Documents\Benutzerverwaltung\users.db
        data_dir = os.path.join(home_dir, "Documents", app_name)
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Documents/Benutzerverwaltung/users.db
        data_dir = os.path.join(home_dir, "Documents", app_name)
    else:  # Linux
        # Linux: ~/.local/share/Benutzerverwaltung/users.db
        data_dir = os.path.join(home_dir, ".local", "share", app_name)
    
    # Create directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    return os.path.join(data_dir, "users.db")

DATABASE = get_database_path()

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                vorname TEXT NOT NULL,
                nachname TEXT NOT NULL
            )
        ''')
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# HTML Template (embedded to avoid file dependencies)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benutzerverwaltung</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .form-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn:hover {
            opacity: 0.8;
        }
        .users-table {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .table tr:hover {
            background-color: #f5f5f5;
        }
        .actions {
            display: flex;
            gap: 5px;
        }
        .message {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div id="root">
        <div class="container">
            <div class="header">
                <h1>Benutzerverwaltung</h1>
                <p>Einfache Verwaltung von Benutzerdaten</p>
            </div>
            <div id="message"></div>
            <div class="form-container">
                <h2 id="form-title">Neuen Benutzer hinzufügen</h2>
                <form id="user-form">
                    <div class="form-group">
                        <label for="vorname">Vorname:</label>
                        <input type="text" id="vorname" placeholder="Vorname eingeben" required>
                    </div>
                    <div class="form-group">
                        <label for="nachname">Nachname:</label>
                        <input type="text" id="nachname" placeholder="Nachname eingeben" required>
                    </div>
                    <button type="submit" class="btn btn-primary" id="submit-btn">Hinzufügen</button>
                    <button type="button" id="cancel-btn" class="btn btn-secondary" style="display: none;">Abbrechen</button>
                </form>
            </div>
            <div class="users-table">
                <h2 id="users-count">Benutzer</h2>
                <div id="users-list"></div>
            </div>
        </div>
    </div>

    <script>
        let editingId = null;
        
        const API_BASE = '/api';
        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="message ${type}">${text}</div>`;
            setTimeout(() => {
                messageDiv.innerHTML = '';
            }, 3000);
        }
        
        async function fetchUsers() {
            try {
                const response = await fetch(`${API_BASE}/users`);
                const users = await response.json();
                displayUsers(users);
            } catch (error) {
                showMessage('Fehler beim Laden der Benutzer', 'error');
            }
        }
        
        function displayUsers(users) {
            const countElement = document.getElementById('users-count');
            const listElement = document.getElementById('users-list');
            
            countElement.textContent = `Benutzer (${users.length})`;
            
            if (users.length === 0) {
                listElement.innerHTML = '<p style="padding: 20px">Keine Benutzer vorhanden</p>';
                return;
            }
            
            let html = '<table class="table"><thead><tr><th>ID</th><th>Vorname</th><th>Nachname</th><th>Aktionen</th></tr></thead><tbody>';
            
            users.forEach(user => {
                html += `
                    <tr>
                        <td>${user.id.substring(0, 8)}...</td>
                        <td>${user.vorname}</td>
                        <td>${user.nachname}</td>
                        <td>
                            <div class="actions">
                                <button onclick="editUser('${user.id}', '${user.vorname}', '${user.nachname}')" class="btn btn-success">Bearbeiten</button>
                                <button onclick="deleteUser('${user.id}')" class="btn btn-danger">Löschen</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            listElement.innerHTML = html;
        }
        
        function editUser(id, vorname, nachname) {
            editingId = id;
            document.getElementById('vorname').value = vorname;
            document.getElementById('nachname').value = nachname;
            document.getElementById('form-title').textContent = 'Benutzer bearbeiten';
            document.getElementById('submit-btn').textContent = 'Aktualisieren';
            document.getElementById('cancel-btn').style.display = 'inline-block';
        }
        
        function cancelEdit() {
            editingId = null;
            document.getElementById('user-form').reset();
            document.getElementById('form-title').textContent = 'Neuen Benutzer hinzufügen';
            document.getElementById('submit-btn').textContent = 'Hinzufügen';
            document.getElementById('cancel-btn').style.display = 'none';
        }
        
        async function deleteUser(id) {
            if (!confirm('Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?')) {
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/users/${id}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    showMessage('Benutzer erfolgreich gelöscht', 'success');
                    fetchUsers();
                } else {
                    showMessage('Fehler beim Löschen', 'error');
                }
            } catch (error) {
                showMessage('Fehler beim Löschen', 'error');
            }
        }
        
        document.getElementById('user-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const vorname = document.getElementById('vorname').value;
            const nachname = document.getElementById('nachname').value;
            
            if (!vorname || !nachname) {
                showMessage('Bitte füllen Sie alle Felder aus', 'error');
                return;
            }
            
            const url = editingId ? `${API_BASE}/users/${editingId}` : `${API_BASE}/users`;
            const method = editingId ? 'PUT' : 'POST';
            
            try {
                const response = await fetch(url, {
                    method,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ vorname, nachname })
                });
                
                if (response.ok) {
                    showMessage(
                        editingId ? 'Benutzer erfolgreich aktualisiert' : 'Benutzer erfolgreich erstellt',
                        'success'
                    );
                    cancelEdit();
                    fetchUsers();
                } else {
                    showMessage('Fehler beim Speichern', 'error');
                }
            } catch (error) {
                showMessage('Fehler beim Speichern', 'error');
            }
        });
        
        document.getElementById('cancel-btn').addEventListener('click', cancelEdit);
        
        // Load users on page load
        fetchUsers();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'vorname' not in data or 'nachname' not in data:
        return jsonify({'error': 'Vorname und Nachname sind erforderlich'}), 400
    
    user_id = str(uuid.uuid4())
    conn = get_db_connection()
    conn.execute('INSERT INTO users (id, vorname, nachname) VALUES (?, ?, ?)',
                 (user_id, data['vorname'], data['nachname']))
    conn.commit()
    conn.close()
    
    return jsonify({'id': user_id, 'vorname': data['vorname'], 'nachname': data['nachname']}), 201

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or 'vorname' not in data or 'nachname' not in data:
        return jsonify({'error': 'Vorname und Nachname sind erforderlich'}), 400
    
    conn = get_db_connection()
    result = conn.execute('UPDATE users SET vorname = ?, nachname = ? WHERE id = ?',
                          (data['vorname'], data['nachname'], user_id))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        return jsonify({'error': 'Benutzer nicht gefunden'}), 404
    
    return jsonify({'id': user_id, 'vorname': data['vorname'], 'nachname': data['nachname']})

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    result = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        return jsonify({'error': 'Benutzer nicht gefunden'}), 404
    
    return jsonify({'message': 'Benutzer gelöscht'})

def open_browser():
    """Open browser after a delay to ensure server is running"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    init_db()
    print("Starte Benutzerverwaltung...")
    print(f"Datenbank-Speicherort: {DATABASE}")
    print("Die Anwendung öffnet sich automatisch in Ihrem Browser...")
    print("Zum Beenden drücken Sie Ctrl+C")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask server
    app.run(host='127.0.0.1', port=5000, debug=False)