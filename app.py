import sqlite3
from flask import Flask


def izveidot_savienojumu():
    conn = sqlite3.connect("citati-db.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug = True)
