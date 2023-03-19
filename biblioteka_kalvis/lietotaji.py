import uuid
import hashlib
import db_savienotajs as db
from datetime import datetime

kategorijas_combolist = ["lasītājs", "darbinieks"]


class Lasitajs:
    def __init__(self, vards, uzvards, pers_kods, talrunis, reg_datums):
        self.vards = vards
        self.uzvards = uzvards
        self.pers_kods = pers_kods
        self.talrunis = talrunis
        self.reg_datums = reg_datums


class Darbinieks(Lasitajs):
    def __init__(self, vards, uzvards, pers_kods, talrunis, reg_datums, parole):
        super().__init__(vards, uzvards, pers_kods, talrunis, reg_datums)
        parole_bin = str.encode(parole)
        parole_hash = hashlib.md5(parole_bin)
        self.parole = parole_hash.hexdigest()


def saglabat_db(lietotajs):
    conn = db.izveidot_savienojumu()

    dati_dict = lietotajs.__dict__
    lietotaja_tips = lietotajs.__class__.__name__.lower()
    print(lietotaja_tips)
    lietotaja_id = str(uuid.uuid4())
    dati_dict["id"] = lietotaja_id

    if lietotaja_tips == "darbinieks":
        conn.execute(
            "INSERT INTO darbinieks VALUES (:id, :vards, :uzvards, :pers_kods, :talrunis, :reg_datums, :parole)",
            dati_dict)
        db.slegt_savienojumu(conn)

    elif lietotaja_tips == "lasitajs":
        conn.execute("INSERT INTO lasitajs VALUES (:id, :vards, :uzvards, :pers_kods, :talrunis, :reg_datums)",
                     dati_dict)
        db.slegt_savienojumu(conn)


def parbaude(lietotajs, parole):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT pers_kods, parole FROM darbinieks WHERE pers_kods=\"{lietotajs}\""
    atbilde = conn.execute(vaicajums).fetchone()
    parole_bin = str.encode(parole)
    parole_hash = hashlib.md5(parole_bin)
    parole_md5 = parole_hash.hexdigest()
    if lietotajs == atbilde["pers_kods"] and parole_md5 == atbilde["parole"]:
        return True
    else:
        return False
