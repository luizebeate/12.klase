import sqlite3

def izveidot_savienojumu():
    conn = sqlite3.connect("atjaunosanas_idejas.db")
    conn.row_factory = sqlite3.Row
    return conn

def slegt_savienojumu(conn):
    conn.commit()
    conn.close()