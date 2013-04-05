import os
from cql.apivalues import ProgrammingError
from flask import Flask, request
from flask import jsonify
from cql import connect
from thrift.transport.TTransport import TTransportException


app = Flask(__name__)

cassandra_server = os.environ.get("TSURU_CASSANDRA_SERVER")
cassandra_port = os.environ.get("TSURU_CASSANDRA_PORT")

@app.route("/resources", methods=["POST"])
def add_instance():
    keyspace = None
    if request.method == 'POST' and 'name' in request.form:
        keyspace = request.form.get('name')
        try:
            conn = connect(host=cassandra_server, port=cassandra_port)
            cursor = conn.cursor()
            cql_command = "CREATE KEYSPACE {0} WITH strategy_class = 'SimpleStrategy' AND strategy_options:replication_factor=3;"
            cursor.execute(cql_command.format(keyspace))
        except (ProgrammingError, TTransportException), e:
            return jsonify({'error':e.message}), 500
        return "", 201
    else:
        return "", 204


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
    try:
        conn = connect(host=cassandra_server, port=cassandra_port)
        cursor = conn.cursor()
        cql_command = "DROP KEYSPACE {0}".format(name)
        cursor.execute(cql_command)
    except (ProgrammingError, TTransportException), e:
        return jsonify({'error':e.message}), 500

    return "", 200

@app.route("/resources/<name>", methods=["POST"])
def bind(name):
    out = jsonify(SOMEVAR="somevalue")
    return out, 201

@app.route("/resources/<name>/hostname/<host>", methods=["DELETE"])
def unbind(name, host):
    return "", 200


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    return "", 204

if __name__ == "__main__":
    app.run()