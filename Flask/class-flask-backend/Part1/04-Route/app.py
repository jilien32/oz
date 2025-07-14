from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, This is Main Page!"

@app.route("/about")
def about():
    return "This is the about page!"

@app.route("/company")
def company():
    return "This is the company page!"

@app.route('/number/<int:number>')
def number(number):
    return f'Number: {number}'

@app.route('/user/<username>')
def user_profile(username):
    return f'UserName: {username}'

@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000/submit'
    data = 'test data'
    response = requests.post(url=url, data=data)
    return response.text

@app.route('/submit', methods=['GET', 'POST', 'PUT', 'DELETE'])
def submit():
    print(request.method)

    if request.method == 'GET':
        print("GET method")
    if request.method == 'POST':
        print("***POST method***", request.data)
    return Response("Sucessfully submitted", status=200)

if __name__ == "__main__":
    app.run()