import { useState, useEffect } from 'react'

function App() {
  const [users, setUsers] = useState([])
  const [formData, setFormData] = useState({ vorname: '', nachname: '' })
  const [editingId, setEditingId] = useState(null)
  const [message, setMessage] = useState({ text: '', type: '' })

  const API_BASE = '/api'

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE}/users`)
      const data = await response.json()
      setUsers(data)
    } catch (error) {
      showMessage('Fehler beim Laden der Benutzer', 'error')
    }
  }

  const showMessage = (text, type) => {
    setMessage({ text, type })
    setTimeout(() => setMessage({ text: '', type: '' }), 3000)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.vorname || !formData.nachname) {
      showMessage('Bitte füllen Sie alle Felder aus', 'error')
      return
    }

    try {
      const url = editingId ? `${API_BASE}/users/${editingId}` : `${API_BASE}/users`
      const method = editingId ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        showMessage(
          editingId ? 'Benutzer erfolgreich aktualisiert' : 'Benutzer erfolgreich erstellt',
          'success'
        )
        setFormData({ vorname: '', nachname: '' })
        setEditingId(null)
        fetchUsers()
      } else {
        showMessage('Fehler beim Speichern', 'error')
      }
    } catch (error) {
      showMessage('Fehler beim Speichern', 'error')
    }
  }

  const handleEdit = (user) => {
    setFormData({ vorname: user.vorname, nachname: user.nachname })
    setEditingId(user.id)
  }

  const handleDelete = async (id) => {
    if (!confirm('Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE}/users/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        showMessage('Benutzer erfolgreich gelöscht', 'success')
        fetchUsers()
      } else {
        showMessage('Fehler beim Löschen', 'error')
      }
    } catch (error) {
      showMessage('Fehler beim Löschen', 'error')
    }
  }

  const handleCancel = () => {
    setFormData({ vorname: '', nachname: '' })
    setEditingId(null)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Benutzerverwaltung</h1>
        <p>Einfache Verwaltung von Benutzerdaten</p>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="form-container">
        <h2>{editingId ? 'Benutzer bearbeiten' : 'Neuen Benutzer hinzufügen'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="vorname">Vorname:</label>
            <input
              type="text"
              id="vorname"
              value={formData.vorname}
              onChange={(e) => setFormData({ ...formData, vorname: e.target.value })}
              placeholder="Vorname eingeben"
            />
          </div>
          <div className="form-group">
            <label htmlFor="nachname">Nachname:</label>
            <input
              type="text"
              id="nachname"
              value={formData.nachname}
              onChange={(e) => setFormData({ ...formData, nachname: e.target.value })}
              placeholder="Nachname eingeben"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            {editingId ? 'Aktualisieren' : 'Hinzufügen'}
          </button>
          {editingId && (
            <button type="button" onClick={handleCancel} className="btn btn-secondary">
              Abbrechen
            </button>
          )}
        </form>
      </div>

      <div className="users-table">
        <h2>Benutzer ({users.length})</h2>
        {users.length === 0 ? (
          <p style={{ padding: '20px' }}>Keine Benutzer vorhanden</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Vorname</th>
                <th>Nachname</th>
                <th>Aktionen</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id.substring(0, 8)}...</td>
                  <td>{user.vorname}</td>
                  <td>{user.nachname}</td>
                  <td>
                    <div className="actions">
                      <button
                        onClick={() => handleEdit(user)}
                        className="btn btn-success"
                      >
                        Bearbeiten
                      </button>
                      <button
                        onClick={() => handleDelete(user.id)}
                        className="btn btn-danger"
                      >
                        Löschen
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App