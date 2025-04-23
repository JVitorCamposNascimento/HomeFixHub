from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sqlite3
import os
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave segura
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Criar pasta para uploads
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Classe para usuário
class User(UserMixin):
    def __init__(self, id, email, is_admin):
        self.id = id
        self.email = email
        self.is_admin = is_admin

# Carregar usuário
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, email, is_admin FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, birthdate TEXT, email TEXT UNIQUE, password TEXT, photo_path TEXT, is_admin INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Página inicial (home)
@app.route('/')
def home():
    return render_template('home.html')

# Formulário de cadastro
@app.route('/cadastro')
def index():
    return render_template('form.html')

# Cadastro
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    birthdate = request.form['birthdate']
    email = request.form['email']
    password = request.form['password']
    photo = request.files['photo']

    # Validar data de nascimento
    try:
        datetime.strptime(birthdate, '%Y-%m-%d')
    except ValueError:
        return "Erro: Data de nascimento inválida. Use o formato AAAA-MM-DD."

    # Hashear a senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Salvar a foto
    photo_path = None
    if photo and photo.filename:
        filename = f"{email}_{photo.filename}"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        photo_path = f"uploads/{filename}"

    # Inserir no banco
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, birthdate, email, password, photo_path) VALUES (?, ?, ?, ?, ?)",
                  (name, birthdate, email, hashed_password, photo_path))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        return "Erro: Email já cadastrado."

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, email, password, is_admin FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            user_obj = User(user[0], user[1], user[3])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash("Email ou senha inválidos.")
    
    return render_template('login.html')

# Dashboard (página após login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Tela de administrador
@app.route('/admin')
@login_required
def admin():
    user = load_user(session.get('_user_id'))
    if not user.is_admin:
        flash("Acesso negado: apenas administradores.")
        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, name, birthdate, email, photo_path FROM users")
    users = c.fetchall()
    conn.close()
    
    return render_template('admin.html', users=users)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)