import sqlite3
import uuid
import os
import sys
import threading
import webbrowser
import time
import platform
import tempfile
import atexit
import socket
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

# Try to import system tray functionality
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("System Tray nicht verfügbar. Installieren Sie: pip install pystray Pillow")

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

# Lock file to prevent multiple instances
LOCK_FILE = None

def create_lock_file():
    """Create a lock file to prevent multiple instances"""
    global LOCK_FILE
    app_name = "benutzerverwaltung_tray"
    
    # Use system temp directory for lock file
    temp_dir = tempfile.gettempdir()
    lock_path = os.path.join(temp_dir, f"{app_name}.lock")
    
    try:
        # Try to create lock file
        if os.path.exists(lock_path):
            # Check if process is still running
            try:
                with open(lock_path, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process exists (cross-platform)
                if platform.system() == "Windows":
                    import psutil
                    if psutil.pid_exists(pid):
                        return False
                else:
                    try:
                        os.kill(pid, 0)  # Signal 0 just checks if process exists
                        return False
                    except OSError:
                        pass  # Process doesn't exist
                
                # Remove stale lock file
                os.remove(lock_path)
            except (ValueError, IOError):
                # Invalid lock file, remove it
                try:
                    os.remove(lock_path)
                except OSError:
                    pass
        
        # Create new lock file
        with open(lock_path, 'w') as f:
            f.write(str(os.getpid()))
        
        LOCK_FILE = lock_path
        
        # Register cleanup function
        atexit.register(cleanup_lock_file)
        
        return True
        
    except Exception as e:
        print(f"⚠️  Warnung: Lock-File konnte nicht erstellt werden: {e}")
        return True  # Continue anyway

def cleanup_lock_file():
    """Remove lock file on exit"""
    global LOCK_FILE
    if LOCK_FILE and os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
        except OSError:
            pass

def find_available_port(start_port=5000, max_tries=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_tries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except socket.error:
            sock.close()
            continue
    return None

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
        .status-bar {
            background: #007bff;
            color: white;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
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
        .connection-warning {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: #dc3545;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            z-index: 9999;
            display: none;
        }
        .connection-warning.show {
            display: block;
        }
        body.connection-lost {
            margin-top: 60px;
        }
    </style>
</head>
<body>
    <div id="connection-warning" class="connection-warning">
        ⚠️ Verbindung zum Server verloren! Die Anwendung wurde möglicherweise beendet.
    </div>
    <div id="root">
        <div class="container">
            <div class="header">
                <h1>Benutzerverwaltung</h1>
                <p>Einfache Verwaltung von Benutzerdaten</p>
            </div>
            <div class="status-bar">
                🖥️ Server läuft auf http://127.0.0.1:5000 | 📁 Daten: ~/Documents/Benutzerverwaltung/ | 🔍 System Tray für Kontrolle
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
        
        // Connection monitoring
        let connectionLost = false;
        
        function checkConnection() {
            fetch('/api/health')
                .then(response => {
                    if (response.ok) {
                        if (connectionLost) {
                            // Connection restored
                            document.getElementById('connection-warning').classList.remove('show');
                            document.body.classList.remove('connection-lost');
                            connectionLost = false;
                        }
                    } else {
                        showConnectionWarning();
                    }
                })
                .catch(error => {
                    showConnectionWarning();
                });
        }
        
        function showConnectionWarning() {
            if (!connectionLost) {
                document.getElementById('connection-warning').classList.add('show');
                document.body.classList.add('connection-lost');
                connectionLost = true;
            }
        }
        
        // Start heartbeat check every 5 seconds
        setInterval(checkConnection, 5000);
        
        // Initial connection check
        checkConnection();
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for frontend connectivity monitoring"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

def create_tray_icon():
    """Load custom icon for the system tray"""
    # Get the directory where the app is located
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        base_dir = sys._MEIPASS
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to load custom icon files in order of preference
    icon_files = [
        "icons/icon_modern_32x32.png",
        "icons/icon_modern_24x24.png", 
        "icons/icon_modern_16x16.png",
        "icons/icon_database_32x32.png",
        "icons/icon_gear_32x32.png"
    ]
    
    for icon_file in icon_files:
        icon_path = os.path.join(base_dir, icon_file)
        if os.path.exists(icon_path):
            try:
                print(f"📱 Verwende Icon: {icon_file}")
                return Image.open(icon_path)
            except Exception as e:
                print(f"⚠️  Fehler beim Laden von {icon_file}: {e}")
                continue
    
    print("⚠️  Kein Custom-Icon gefunden, erstelle Fallback-Icon")
    # Fallback: Create a simple colored circle icon
    width = height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle with white "U" for User management
    draw.ellipse([4, 4, width-4, height-4], fill=(0, 123, 255, 255), outline=(0, 86, 179, 255), width=2)
    
    # Draw "U" letter (simplified)
    center_x, center_y = width // 2, height // 2
    # Simple U shape with rectangles
    draw.rectangle([center_x-8, center_y-12, center_x-4, center_y+8], fill=(255, 255, 255, 255))
    draw.rectangle([center_x+4, center_y-12, center_x+8, center_y+8], fill=(255, 255, 255, 255))  
    draw.rectangle([center_x-4, center_y+4, center_x+4, center_y+8], fill=(255, 255, 255, 255))
    
    return image

def open_browser():
    """Open browser after a delay to ensure server is running"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def show_startup_progress():
    """Show startup progress with simple console output"""
    steps = [
        "🔧 Initialisiere Anwendung...",
        "🗃️  Prüfe Datenbank...",
        "🌐 Starte Web-Server...",
        "🖥️  Bereite System Tray vor...",
        "🚀 Öffne Browser...",
        "✅ Bereit!"
    ]
    
    for i, step in enumerate(steps):
        print(f"[{i+1}/{len(steps)}] {step}")
        time.sleep(0.3)
    
    print("━" * 50)

def quit_app(icon, item):
    """Quit the application"""
    cleanup_lock_file()
    icon.stop()
    os._exit(0)

def open_app(icon, item):
    """Open the app in browser"""
    # Try to find the port from the running app
    for port in range(5000, 5010):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('127.0.0.1', port))
            sock.close()
            webbrowser.open(f'http://127.0.0.1:{port}')
            return
        except socket.error:
            sock.close()
            continue
    # Fallback
    webbrowser.open('http://127.0.0.1:5000')

def setup_tray():
    """Setup system tray icon"""
    if not TRAY_AVAILABLE:
        return None
    
    icon_image = create_tray_icon()
    
    menu = pystray.Menu(
        item('Benutzerverwaltung öffnen', open_app, default=True),
        item('Datenbank-Ordner', lambda: webbrowser.open(f'file://{os.path.dirname(DATABASE)}')),
        pystray.Menu.SEPARATOR,
        item('Beenden', quit_app)
    )
    
    icon = pystray.Icon("benutzerverwaltung", icon_image, "Benutzerverwaltung", menu)
    return icon

def run_flask(port=5000):
    """Run Flask server"""
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("🚀 Benutzerverwaltung mit System Tray")
    print("=" * 50)
    
    # Check for multiple instances
    if not create_lock_file():
        print("❌ Eine Instanz der Anwendung läuft bereits!")
        print("   Prüfen Sie das System Tray für das laufende Programm.")
        input("Drücken Sie Enter zum Beenden...")
        sys.exit(1)
    
    # Find available port
    port = find_available_port(5000)
    if port is None:
        print("❌ Kein verfügbarer Port gefunden (5000-5009)!")
        cleanup_lock_file()
        input("Drücken Sie Enter zum Beenden...")
        sys.exit(1)
    
    # Show startup progress
    show_startup_progress()
    
    # Initialize database
    init_db()
    print(f"📁 Datenbank: {DATABASE}")
    
    if not TRAY_AVAILABLE:
        print("⚠️  System Tray nicht verfügbar. Installieren Sie: pip install pystray Pillow")
        print("   Die Anwendung läuft im Konsolenmodus.")
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: run_flask(port), daemon=True)
    flask_thread.start()
    
    # Wait a moment for server to start
    time.sleep(0.5)
    
    # Start browser
    threading.Thread(target=lambda: (time.sleep(1.5), webbrowser.open(f'http://127.0.0.1:{port}')), daemon=True).start()
    
    # Setup and run system tray (this blocks until quit)
    if TRAY_AVAILABLE:
        try:
            print("📱 System Tray aktiv - Rechtsklick für Optionen")
            print(f"🌐 Browser: http://127.0.0.1:{port}")
            print("🛑 Zum Beenden: Rechtsklick Tray → Beenden")
            
            tray_icon = setup_tray()
            if tray_icon:
                tray_icon.run()
            else:
                print("❌ Tray-Icon konnte nicht erstellt werden")
                input("Drücken Sie Enter zum Beenden...")
        except Exception as e:
            print(f"❌ Tray-Fehler: {e}")
            input("Drücken Sie Enter zum Beenden...")
    else:
        # Fallback without tray
        print(f"🌐 Browser: http://127.0.0.1:{port}")
        print("🛑 Zum Beenden: Ctrl+C")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Anwendung beendet.")
            cleanup_lock_file()
            os._exit(0)