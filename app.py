from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/users/<user_id>')
def get_users(user_id):
    return jsonify({
        'user_id': user_id,
        'name': 'John Doe',
        'age': 29
    })

if __name__ == '__main__':
    app.run()
