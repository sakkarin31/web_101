from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']
        if not is_valid_user(entered_username, entered_password):
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_existing_user(username):
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        create_user(username, password_hash)
        flash('Registered successfully! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

def is_valid_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return True
    return False

def is_existing_user(username):
    return User.query.filter_by(username=username).first() is not None

def create_user(username, password_hash):
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
