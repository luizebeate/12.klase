import izvelne
import sqlite3
import db_savienotajs1 as db

visas_mebeles = izvelne.mebelu_saraksts()
visi_materiali = izvelne.materialu_saraksts()
visas_tehnikas = izvelne.tehniku_saraksts()
visi_stili = izvelne.stilu_saraksts()

izveleta_mebele = "Galds"
izvelets_materials = "Koks"
izveleta_tehnika = "Dekupēšana"
izvelets_stils = "Klasiskais"

def izveleta_konkreta_mebele(izveleta_mebele):
    conn = db.izveidot_savienojumu()

    vaicajums = f"SELECT ID FROM mebele WHERE mebeles_nosaukums = \"{izveleta_mebele}\""
    rezultats = conn.execute(vaicajums).fetchone()
    izveletas_mebeles_id = rezultats["ID"]

    db.slegt_savienojumu(conn)
    return izveletas_mebeles_id
#print(izveleta_konkreta_mebele())

def izvelets_konkrets_materials(izvelets_materials):
    conn = db.izveidot_savienojumu()

    vaicajums = f"SELECT ID FROM materials WHERE materiala_nosaukums = \"{izvelets_materials}\""
    rezultats = conn.execute(vaicajums).fetchone()
    izvelets_materials_id = rezultats["ID"]

    db.slegt_savienojumu(conn)
    return izvelets_materials_id

#print(izvelets_konkrets_materials())

def izveleta_konkreta_tehnika(izveleta_tehnika):
    conn = db.izveidot_savienojumu()

    vaicajums = f"SELECT ID FROM tehnika WHERE tehnikas_nosaukums = \"{izveleta_tehnika}\""
    rezultats = conn.execute(vaicajums).fetchone()
    izveleta_tehnika_id = rezultats["ID"]

    db.slegt_savienojumu(conn)
    return izveleta_tehnika_id

#print(izveleta_konkreta_tehnika())

def izvelets_konkrets_stils(izvelets_stils):
    conn = db.izveidot_savienojumu()

    vaicajums = f"SELECT ID FROM stils WHERE stila_nosaukums = \"{izvelets_stils}\""
    rezultats = conn.execute(vaicajums).fetchone()
    izvelets_stils_id = rezultats["ID"]

    db.slegt_savienojumu(conn)
    return izvelets_stils_id

#print(izvelets_konkrets_stils())

def izveleta_konkreta_ideja(izveleta_mebele, izvelets_materials, izveleta_tehnika, izvelets_stils):
    conn = db.izveidot_savienojumu()

    izveletas_mebeles_id = izveleta_konkreta_mebele(izveleta_mebele)
    izvelets_materials_id = izvelets_konkrets_materials(izvelets_materials)
    izveleta_tehnika_id = izveleta_konkreta_tehnika(izveleta_tehnika)
    izvelets_stils_id = izvelets_konkrets_stils(izvelets_stils)
    vaicajums = f"""
                SELECT apraksts_ID FROM idejas WHERE mebele_id = {izveletas_mebeles_id}
                AND materials_id = {izvelets_materials_id}
                AND tehnika_id = {izveleta_tehnika_id} 
                AND stils_id = {izvelets_stils_id}
                """
    rezultats = conn.execute(vaicajums).fetchall()
    izveleto_ideju_id = []
    for katrs in rezultats:
        izveleto_ideju_id.append(katrs["apraksts_ID"])

    db.slegt_savienojumu(conn)
    if izveleto_ideju_id[0] == None:
        izveleto_ideju_id[0] = 0

    return izveleto_ideju_id[0]

#print(izveleta_konkreta_mebele(izveleta_mebele))

def izveleta_konkreta_ideja_apraksts():
    conn = db.izveidot_savienojumu()

    izveleto_ideju_id = izveleta_konkreta_ideja()
    apraksti = []
    for katrs in izveleto_ideju_id:
        vaicajums = f"SELECT teksts FROM apraksti WHERE ID = {katrs}"
        rezultats = conn.execute(vaicajums).fetchone()
        apraksti.append(rezultats["teksts"])

    db.slegt_savienojumu(conn)
    return apraksti

def test_izveleta_konkreta_ideja_apraksts(id):
    conn = db.izveidot_savienojumu()

    apraksti = []

    vaicajums = f"SELECT teksts FROM apraksti WHERE ID = {id}"
    rezultats = conn.execute(vaicajums).fetchone()
    apraksti.append(rezultats["teksts"])

    db.slegt_savienojumu(conn)
    return apraksti
