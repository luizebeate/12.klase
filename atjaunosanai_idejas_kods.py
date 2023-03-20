from abc import ABC, abstractmethod
import db_savienotajs1 as db
import sqlite3

conn  = sqlite3.connect("atjaunosanas_idejas.db")
c = conn.cursor()

class Idejas:
    def __init__(self, mebele, materials, tehnika, stils, apraksts):
        self.mebele = mebele
        self.materials = materials 
        self.tehnika = tehnika
        self.stils = stils
        self.apraksts = apraksts

    def mebelu_saraksts(self):
        c.execute("SELECT mebeles_nosaukums FROM mebele")
        razotaji = c.fetchall()
        return razotaji
    
    def materialu_saraksts(self):
        c.execute("SELECT materiala_nosaukums FROM mebele")
        razotaji = c.fetchall()
        return razotaji
    
    def tehniku_saraksts(self):
        c.execute("SELECT tehnikas_nosaukums FROM mebele")
        razotaji = c.fetchall()
        return razotaji
    
    def stilu_saraksts(self):
        c.execute("SELECT stila_nosaukums FROM mebele")
        razotaji = c.fetchall()
        return razotaji
         
Idejas.stilu_saraksts()
