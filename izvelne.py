import db_savienotajs1 as db
import sqlite3

def mebelu_saraksts():
    conn = db.izveidot_savienojumu()
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM mebele").fetchall()

    mebeles = []

    for katrs in rezultati:
        mebeles.append(katrs["mebeles_nosaukums"])

    db.slegt_savienojumu(conn)
    return mebeles

def materialu_saraksts():
    conn = db.izveidot_savienojumu()
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM materials").fetchall()

    materiali = []

    for katrs in rezultati:
        materiali.append(katrs["materiala_nosaukums"])

    db.slegt_savienojumu(conn)
    return materiali


def tehniku_saraksts():
    conn = db.izveidot_savienojumu()
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM tehnika").fetchall()

    tehnikas = []

    for katrs in rezultati:
        tehnikas.append(katrs["tehnikas_nosaukums"])

    db.slegt_savienojumu(conn)
    return tehnikas


def stilu_saraksts():
    conn = db.izveidot_savienojumu()
    c = conn.cursor()
    rezultati = c.execute("SELECT * FROM stils").fetchall()

    stili = []

    for katrs in rezultati:
        stili.append(katrs["stila_nosaukums"])

    db.slegt_savienojumu(conn)
    return stili


# print(mebelu_saraksts())
# print(materialu_saraksts())
# print(tehniku_saraksts())
# print(stilu_saraksts())