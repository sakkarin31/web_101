from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
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
    error = None
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        if is_existing_user(entered_username):
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            hashed_password = generate_password_hash(entered_password, method='sha256')
            create_user(entered_username, hashed_password)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

def is_valid_user(username, password):
    return username == 'wwww' and password == '123123'

def is_existing_user(username):
    return username == 'wwww'

def create_user(username, password):
    pass

if __name__ == '__main__':
    app.run(debug=True)
