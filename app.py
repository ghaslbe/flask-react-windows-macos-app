import sqlite3
import uuid
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='dist', template_folder='dist')
CORS(app)

DATABASE = 'users.db'

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

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)