from flask import Flask
app = Flask(__name__)

@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201

