from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DATABASE = 'database.db'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
        ''')


        c.execute('''
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()

def add_image_column_if_not_exists():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("PRAGMA table_info(events)")
    columns = [column[1] for column in c.fetchall()]
    if 'image_filename' not in columns:
        c.execute("ALTER TABLE events ADD COLUMN image_filename TEXT")
        print("image filename collum added")
    else:
        print("image filename already exists")

    conn.commit()
    conn.close()

def add_is_published_column_if_not_exists():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("PRAGMA table_info(events)")
    columns = [col[1] for col in c.fetchall()]
    if 'is_published' not in columns:
        c.execute("ALTER TABLE events ADD COLUMN is_published INTEGER DEFAULT 0")
        print("העמודה is_published נוספה לטבלת events.")
    else:
        print("העמודה is_published כבר קיימת.")
    conn.commit()
    conn.close()

@app.route('/publish_event/<int:event_id>', methods=['POST'])
def publish_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_id FROM events WHERE id = ?", (event_id,))
    row = c.fetchone()
    if row and row['user_id'] == session['user_id']:
        c.execute("UPDATE events SET is_published = 1 WHERE id = ?", (event_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('public_timeline'))

@app.route('/public_timeline')
def public_timeline():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT events.*, users.username 
        FROM events
        JOIN users ON events.user_id = users.id
        WHERE events.is_published = 1
    ''')
    events = c.fetchall()
    conn.close()
    return render_template("public_timeline.html", events=events, username=session.get("username", "Guest"))



@app.route('/')
@app.route('/home')
def home():
    username = session.get('username', 'Guest')
    return render_template('home.html', username=username)


@app.route('/all_users')
def all_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()

    username = session.get('username')
    return render_template('all_users.html', users=users, username=username)



@app.route('/timeline')
def timeline():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE user_id = ? ORDER BY date', (session['user_id'],))
    events = c.fetchall()
    conn.close()

    return render_template('timeline.html', events=events, username=session.get("username", "Guest"))



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['is_admin'] = user[6]
            session['user_id'] = user[0]
            return redirect(url_for('home')) 
        
        return render_template('login.html', message="Invalid username or password")  

    return render_template('login.html')

    # GET request
    return render_template('login.html')

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('event_title')
        date = request.form.get('event_date')
        description = request.form.get('event_description')
        image = request.files.get('event_image')
        user_id = session.get('user_id')
        image_filename = None

        if not title or not date:
            return render_template('create_event.html', error='Title and date are required.')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            image_filename = unique_filename

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO events (user_id, title, description, date, image_filename)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, description, date, image_filename))
        conn.commit()
        conn.close()

        return redirect(url_for('timeline'))

    return render_template('create_event.html')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM events WHERE id = ? AND user_id = ?', (event_id, user_id))
    event = c.fetchone()

    if event:
        c.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('timeline'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not (first_name and last_name and email and username and password):
            return render_template('register.html', error='Please fill all fields.')

        conn = get_db_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        if c.fetchone():
            conn.close()
            return render_template('register.html', error='Username already exists.')

        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        if c.fetchone():
            conn.close()
            return render_template('register.html', error='Email already registered.')

        is_admin = 1 if username.lower() == 'admino' else 0

        c.execute('''
            INSERT INTO users (first_name, last_name, email, username, password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, username, password, is_admin))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    init_db()
    add_image_column_if_not_exists()
    add_is_published_column_if_not_exists()
    app.run(debug=True)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


