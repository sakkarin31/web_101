from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        enter_username = request.form['username']
        enter_password = request.form['password']
        if not is_valid_user(enter_username, enter_password):
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def is_valid_user(username, password):
    return username == 'wwww' and password == '123123'

if __name__ == '__main__':
    app.run(debug=True)
