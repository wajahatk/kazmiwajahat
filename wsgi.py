from os import environ, getenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template

app = Flask(__name__)
host = getenv('HOST')
port = environ.get('PORT')


@app.route("/", methods=['GET'])
def index():
    return make_response(render_template('index.html'), 200)

if __name__ == "__main__":
    app.run(host=host, port=port)