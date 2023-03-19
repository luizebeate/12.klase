import sqlite3

def bez_rindam():
    conn = sqlite3.connect("citatu-db.db")
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM citati").fetchall()
    print(rezultati)

    for katrs in rezultati:
        print(katrs[1], katrs[2])

def ar_rindam():
    conn = sqlite3.connect("citatu-db.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM citati").fetchall()
    print(rezultati)

    for katrs in rezultati:
        print(katrs["autors"], katrs["teksts"])

# bez_rindam()
ar_rindam()