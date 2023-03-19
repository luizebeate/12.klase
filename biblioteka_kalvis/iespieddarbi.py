# https://codefather.tech/blog/python-abstract-class/
# https://blog.teclado.com/python-abc-abstract-base-classes/

from abc import ABC, abstractmethod
import db_savienotajs as db

kategorijas_combolist = ["grāmata", "periodika"]
kategorijas_dict = {i: kategorijas_combolist[i - 1] for i in range(1, len(kategorijas_combolist) + 1)}


class Iespieddarbs(ABC):
    @abstractmethod
    def __init__(self, izdevejs, nosaukums, gads, pieejamais_skaits, plaukta_nr):
        self.izdevejs = izdevejs
        self.nosaukums = nosaukums
        self.gads = gads
        self.pieejamais_skaits = pieejamais_skaits
        self.plaukta_nr = plaukta_nr

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def saglabat_db(self):
        pass


# noinspection DuplicatedCode
class Gramata(Iespieddarbs):
    def __init__(self, izdevejs, autors_vards, autors_uzvards, nosaukums, gads, pieejamais_skaits, plaukta_nr):
        self.izdevejs = izdevejs
        self.autors_vards = autors_vards
        self.autors_uzvards = autors_uzvards
        self.nosaukums = nosaukums
        self.gads = gads
        self.pieejamais_skaits = pieejamais_skaits
        self.plaukta_nr = plaukta_nr

    def __str__(self):
        return f"{self.izdevejs}, {self.autors_vards}, {self.autors_uzvards}, {self.nosaukums}, {self.gads}, {self.pieejamais_skaits}, {self.plaukta_nr}"

    def saglabat_db(self):
        conn = db.izveidot_savienojumu()

        parbaudit_autoru_vaicajums = f"SELECT vards, uzvards FROM autori WHERE vards=\"{self.autors_vards}\" AND uzvards=\"{self.autors_uzvards}\""
        rezultats = conn.execute(parbaudit_autoru_vaicajums).fetchall()
        if len(rezultats) == 0:
            autors_uz_db = (self.autors_vards, self.autors_uzvards)
            conn.execute("INSERT INTO autori (vards, uzvards) VALUES (?, ?)", autors_uz_db)
            conn.commit()

        autora_id_vaicajums = f"SELECT ID FROM autori WHERE vards=\"{self.autors_vards}\" AND uzvards=\"{self.autors_uzvards}\""
        atbilde = conn.execute(autora_id_vaicajums).fetchone()
        autora_id = atbilde["ID"]

        parbaudit_izdeveju_vaicajums = f"SELECT izdeveja_nosaukums FROM izdeveji WHERE izdeveja_nosaukums=\"{self.izdevejs}\""
        rezultats = conn.execute(parbaudit_izdeveju_vaicajums).fetchall()
        if len(rezultats) == 0:
            izdevejs_uz_db = (self.izdevejs,)
            conn.execute("INSERT INTO izdeveji (izdeveja_nosaukums) VALUES (?)", izdevejs_uz_db)
            conn.commit()

        izdeveja_id_vaicajums = f"SELECT ID FROM izdeveji WHERE izdeveja_nosaukums=\"{self.izdevejs}\""
        atbilde = conn.execute(izdeveja_id_vaicajums).fetchone()
        izdeveja_id = atbilde["ID"]

        parbaudit_gramatu_vaicajums = \
            f"SELECT nosaukums, izdeveja_ID, autora_ID FROM iespieddarbs \
            WHERE nosaukums=\"{self.nosaukums}\" AND autora_ID=\"{autora_id}\" AND izdeveja_id = \"{izdeveja_id}\""
        rezultats = conn.execute(parbaudit_gramatu_vaicajums).fetchall()
        if len(rezultats) == 0:
            gramata_uz_db = (1, izdeveja_id, autora_id, self.nosaukums, self.gads, self.pieejamais_skaits, self.plaukta_nr)
            conn.execute(
                "INSERT INTO iespieddarbs (veida_ID, izdeveja_ID, autora_ID, nosaukums, izd_gads, pieej_skaits, plaukta_nr) VALUES (?, ?, ?, ?, ?, ?, ?)",
                gramata_uz_db)
            conn.commit()

        db.slegt_savienojumu(conn)


class Periodika(Iespieddarbs):
    def __init__(self, izdevejs, nosaukums, gads, numurs, pieejamais_skaits, plaukta_nr):
        self.izdevejs = izdevejs
        self.nosaukums = nosaukums
        self.gads = gads
        self.numurs = numurs
        self.pieejamais_skaits = pieejamais_skaits
        self.plaukta_nr = plaukta_nr

    def __str__(self):
        return f"{self.izdevejs}, {self.nosaukums}, {self.gads}, {self.numurs}, {self.pieejamais_skaits}, {self.plaukta_nr}"

    def saglabat_db(self):
        conn = db.izveidot_savienojumu()

        parbaudit_izdeveju_vaicajums = f"SELECT izdeveja_nosaukums FROM izdeveji WHERE izdeveja_nosaukums=\"{self.izdevejs}\""
        rezultats = conn.execute(parbaudit_izdeveju_vaicajums).fetchall()
        if len(rezultats) == 0:
            izdevejs_uz_db = (self.izdevejs,)
            conn.execute("INSERT INTO izdeveji (izdeveja_nosaukums) VALUES (?)", izdevejs_uz_db)
            conn.commit()

        izdeveja_id_vaicajums = f"SELECT ID FROM izdeveji WHERE izdeveja_nosaukums=\"{self.izdevejs}\""
        atbilde = conn.execute(izdeveja_id_vaicajums).fetchone()
        izdeveja_id = atbilde["ID"]

        parbaudit_periodiku_vaicajums = \
            f"SELECT nosaukums, izdeveja_id, numurs FROM iespieddarbs \
            WHERE nosaukums=\"{self.nosaukums}\" AND izdeveja_id = \"{izdeveja_id}\" AND numurs = \"numurs\""
        rezultats = conn.execute(parbaudit_periodiku_vaicajums).fetchall()
        if len(rezultats) == 0:
            periodika_uz_db = (2, izdeveja_id, self.nosaukums, self.gads, self.numurs, self.pieejamais_skaits, self.plaukta_nr)
            conn.execute(
                "INSERT INTO iespieddarbs (veida_ID, izdeveja_id, nosaukums, izd_gads, numurs, pieej_skaits, plaukta_nr) VALUES (?, ?, ?, ?, ?, ?, ?)",
                periodika_uz_db)
            conn.commit()

        db.slegt_savienojumu(conn)
