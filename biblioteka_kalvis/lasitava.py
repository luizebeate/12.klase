from datetime import datetime
import db_savienotajs as db


def izsniegt(lasitajs, izdevums, atdosanas_termins):
    datums = datetime.now().date()
    conn = db.izveidot_savienojumu()
    vertibas = (lasitajs, izdevums, datums, atdosanas_termins)
    vaicajums = f"INSERT INTO lasitava (lasitaja_id, izdevuma_id, izsniegsanas_datums, atdosanas_termins) VALUES (?, ?, ?, ?)"
    conn.execute(vaicajums, vertibas)
    izsnieguma_nr_vaicajums = f"SELECT id FROM lasitava WHERE ROWID IN ( SELECT max( ROWID ) FROM lasitava)"
    izsnieguma_nr = conn.execute(izsnieguma_nr_vaicajums).fetchone()
    db.slegt_savienojumu(conn)
    return izsnieguma_nr["id"]


def atdot(izsniegsanas_id):
    conn = db.izveidot_savienojumu()
    id_parbaude_vaicajums = f"SELECT id FROM lasitava WHERE id = {izsniegsanas_id}"
    id_parbaude = conn.execute(id_parbaude_vaicajums).fetchone()
    if id_parbaude:
        datums = datetime.now().date()
        vaicajums = f"UPDATE lasitava SET atdosanas_datums = \"{datums}\" WHERE id = {izsniegsanas_id}"
        conn.execute(vaicajums)
        izdzests = True
    else:
        izdzests = False
    db.slegt_savienojumu(conn)
    return izdzests


def aprekinat_kavejuma_naudu(izsniegsnas_id):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT atdosanas_termins, atdosanas_datums FROM lasitava WHERE id={izsniegsnas_id}"
    rezultats = conn.execute(vaicajums).fetchone()
    termins = datetime.strptime(rezultats["atdosanas_termins"], "%Y-%m-%d")
    faktiskais = datetime.strptime(rezultats["atdosanas_datums"], "%Y-%m-%d")
    nokavets = (faktiskais - termins).days
    if nokavets > 0:
        kavejuma_nauda = nokavets * 1.2
    else:
        kavejuma_nauda = 0
    return kavejuma_nauda
