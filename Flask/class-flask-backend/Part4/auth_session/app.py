from flask import Flask, render_template, request, redirect, session, flash
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'flask-secret-key' # 실제로 배포시에는 .env or yaml
app.config['PERMANENT_SESSION_LIFETIME']= timedelta(days=7) # 세션에 기간이 생김

# admin user
users = {
    'john': 'pw123',
    'leo': 'pw123'
}

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        session.permanent = True
        return redirect('/secret')
    else:
        flash("Invalid username or password")
        return redirect('/')
    
@app.route('/secret')
def secret():
    if 'username' in session:
        return render_template('secret.html')
    else:
        return redirect('/')
    
# 로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)