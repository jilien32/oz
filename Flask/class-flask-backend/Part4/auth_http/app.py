from flask import Flask, render_template
# pip install flask-httpauth
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    'admin': 'secret',
    'guest': 'pw123'
}

@app.route('/')
def index():
    return render_template('index.html')

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    
@app.route('/protected')
@auth.login_required
def protected():
    return render_template('secret.html')

if __name__ == "__main__":
    app.run(debug=True)