from os import environ, getenv
from flask import Flask, make_response

app = Flask(__name__)
host = getenv('HOST')
port = environ.get('PORT')

@app.route("/", methods=['GET'])
def index():
    return make_response('Up and running...', 200)

if __name__ == "__main__":
    app.run(host=host, port=port)