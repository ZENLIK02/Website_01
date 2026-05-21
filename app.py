import os
import sqlite3
import subprocess

from flask import Flask, request


app = Flask(__name__)
app.config["SECRET_KEY"] = "hardcoded_flask_secret_for_semgrep"


@app.route("/users")
def users():
    name = request.args.get("name", "")
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin'), (2, 'guest')")
    query = "SELECT * FROM users WHERE name = '%s'" % name
    rows = cursor.execute(query).fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    return subprocess.check_output("ping -c 1 " + host, shell=True, text=True)


@app.route("/run")
def run():
    command = request.args.get("cmd", "whoami")
    os.system(command)
    return "command executed"


@app.route("/math")
def math():
    expression = request.args.get("expr", "1+1")
    return str(eval(expression))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
