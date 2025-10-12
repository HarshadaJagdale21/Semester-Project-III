import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # your phpMyAdmin username
        password="",       # your phpMyAdmin password
        database="jarvis_users"
    )

def register_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        db.close()
        return False  # user exists
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    db.close()
    return True

def login_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()
    if user:
        return True
    else:
        return False
