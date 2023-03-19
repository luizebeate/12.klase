import db_savienotajs as db


def sanemt_autora_id(autors_vards, autors_uzvards):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT ID FROM autori WHERE vards LIKE \"{autors_vards}%\" AND uzvards LIKE \"{autors_uzvards}%\""
    rezultats = conn.execute(vaicajums).fetchall()
    autora_id = []
    for katrs in rezultats:
        autora_id.append(katrs["ID"])
    return autora_id


def sanemt_gramatas_id(autora_id, nosaukums):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT id FROM iespieddarbs WHERE autora_ID = \"{autora_id}\" AND nosaukums LIKE \"%{nosaukums}%\" AND veida_ID = 1"
    rezultats = conn.execute(vaicajums).fetchall()
    gramatas_id = []
    for katrs in rezultats:
        gramatas_id.append(katrs["id"])
    return gramatas_id


def meklet_gramatu(autors_vards, autors_uzvards, nosaukums):
    visi_autora_id = sanemt_autora_id(autors_vards, autors_uzvards)
    atrastas_gramatas = {}
    for autora_id in visi_autora_id:
        gramatas_id = sanemt_gramatas_id(autora_id, nosaukums)
        if len(gramatas_id) > 0:
            atrastas_gramatas[autora_id] = gramatas_id
    return atrastas_gramatas


####

def meklet_periodiku(nosaukums, gads, numurs):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT id FROM iespieddarbs WHERE nosaukums LIKE \"%{nosaukums}%\" AND izd_gads LIKE \"%{gads}%\" AND numurs LIKE \"%{numurs}%\""
    rezultats = conn.execute(vaicajums).fetchall()
    atrasta_periodika = []
    for katrs in rezultats:
        atrasta_periodika.append(katrs["ID"])
    return atrasta_periodika


####
def izdevuma_info(izdevuma_id):
    vaicajums_izdevums = f"""
    SELECT izdeveji.izdeveja_nosaukums, autori.vards, autori.uzvards, iespieddarbs.nosaukums, iespieddarbs.izd_gads, iespieddarbs.numurs
    FROM izdeveji
    INNER JOIN iespieddarbs ON iespieddarbs.izdeveja_ID = izdeveji.id
    INNER JOIN autori ON iespieddarbs.autora_ID = autori.ID
    WHERE iespieddarbs.id = {izdevuma_id}
    """

    conn = db.izveidot_savienojumu()
    izdevums = conn.execute(vaicajums_izdevums).fetchone()

    return f"{izdevums['izdeveja_nosaukums']}, {izdevums['vards']}, {izdevums['uzvards']}, {izdevums['nosaukums']}, {izdevums['izd_gads']}, {izdevums['numurs']}"


####

def meklet_lasitaju(vards, uzvards, pers_kods):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT ID FROM lasitajs WHERE vards LIKE \"{vards}%\" AND uzvards LIKE \"{uzvards}%\" AND pers_kods LIKE \"{pers_kods}%\""
    rezultats = conn.execute(vaicajums).fetchone()
    try:
        lasitaja_id = rezultats["id"]
    except:
        lasitaja_id = -1
    finally:
        return lasitaja_id


def lasitaja_dati(lasitaja_id):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT vards, uzvards, pers_kods FROM lasitajs WHERE ID = \"{lasitaja_id}\""
    rezultats = conn.execute(vaicajums).fetchone()
    return rezultats


###
def rezultatu_tabula(atradumi):
    tabula = []
    if isinstance(atradumi, dict):
        conn = db.izveidot_savienojumu()
        for autors in atradumi:
            vaicajums = f"SELECT vards, uzvards FROM autori WHERE ID={autors}"
            atbilde_autors = conn.execute(vaicajums).fetchone()
            vards = atbilde_autors["vards"]
            uzvards = atbilde_autors["uzvards"]

            vaicajums_gramata = f"SELECT id, izdeveja_id, nosaukums, izd_gads FROM iespieddarbs WHERE autora_ID={autors}"
            atbilde_gramata = conn.execute(vaicajums_gramata).fetchall()

            for katra in atbilde_gramata:
                vaicajums_izdevnieciba = f"SELECT izdeveja_nosaukums FROM izdeveji WHERE id = {katra['izdeveja_id']}"
                atbilde_izdevnieciba = conn.execute(vaicajums_izdevnieciba).fetchone()

                rinda = [katra["id"], f"{vards} {uzvards}", katra["nosaukums"], katra["izd_gads"],
                         atbilde_izdevnieciba["izdeveja_nosaukums"], ""]
                tabula.append(rinda)
        conn.close()

    elif isinstance(atradumi, list):
        conn = db.izveidot_savienojumu()
        for katrs in atradumi:
            vaicajums_periodika = f"SELECT izdeveja_id, nosaukums, izd_gads, numurs FROM iespieddarbs WHERE id = {katrs}"
            atbilde_periodika = conn.execute(vaicajums_periodika).fetchone()

            vaicajums_izdevnieciba = f"SELECT izdeveja_nosaukums FROM izdeveji WHERE id = {atbilde_periodika['izdeveja_id']}"
            atbilde_izdevnieciba = conn.execute(vaicajums_izdevnieciba).fetchone()

            rinda = katrs, "", atbilde_periodika["nosaukums"], atbilde_periodika["izd_gads"], atbilde_izdevnieciba[
                "izdeveja_nosaukums"], atbilde_periodika["numurs"]
            tabula.append(rinda)

    return tabula
