from flask import Flask, session, redirect, url_for, render_template, request


app = Flask(__name__)
with open('/run/secrets/flask_key') as f:
    key = f.readline().rstrip()
app.secret_key = key


def is_valid_login(password):
    with open('/run/secrets/web_login_password') as f:
        valid_password = f.readline().rstrip()
    return password == valid_password


@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in'] == True:
        return '<a href="/logout">Logout</a>'

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and is_valid_login(request.form['password']):
        session['logged_in'] = True
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
