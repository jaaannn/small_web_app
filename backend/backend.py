from flask import Flask, request, jsonify, g
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database/users.db'
PORT = os.environ['PORT']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Run init_db() manually once to initialize your database, or automate it as needed


@app.route('/user', methods=['POST'])
def save_user():
    user_data = request.json
    db = get_db()
    try:
        db.execute('INSERT INTO users (name, lastName, username) VALUES (?, ?, ?)',
                   [user_data['name'], user_data['lastName'], user_data['username']])
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

    return jsonify({"message": "User saved successfully"}), 201


@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    db = get_db()
    deleted = db.execute('DELETE FROM users WHERE username = ?', [username])
    db.commit()
    if deleted.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/users', methods=['GET'])
def list_users():
    db = get_db()
    cursor = db.execute('SELECT name, lastName, username FROM users')
    users = cursor.fetchall()

    # Convert the rows into a list of dicts to make them JSON serializable
    users_list = [dict(user) for user in users]

    return jsonify(users_list)

if __name__ == '__main__':
    if os.path.isfile("database/users.db"):
        print("database found")
    else:
        init_db()
    app.run(host='0.0.0.0', port=5000)
