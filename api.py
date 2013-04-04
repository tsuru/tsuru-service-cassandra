from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201

@app.route("/resources/<name>", methods=["POST"])
def bind(name):
    out = jsonify(SOMEVAR="somevalue")
    return out, 201
