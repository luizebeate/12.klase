import db_savienotajs1 as db
from datetime import datetime
import hashlib

class Darbinieks:
    def __init__(self, vards, uzvards, pers_kods, talrunis, reg_datums, parole):
        self.vards = vards
        self.uzvards = uzvards
        self.pers_kods = pers_kods
        self.talrunis = talrunis
        self.reg_datums = reg_datums
        parole_bin = str.encode(parole)
        parole_hash = hashlib.md5(parole_bin)
        self.parole = parole_hash.hexdigest()

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
        db.slegt_savienojumu(conn)
        return False