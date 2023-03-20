import sqlite3
from flask import Flask, abort, render_template, request, flash
import izvelne
import atjaunosanas_kods
import darbinieka_piekluve


def izveidot_savienojumu():
    conn = sqlite3.connect("atjaunosanas_idejas.db")
    conn.row_factory = sqlite3.Row
    return conn

def sanemt_aprakstu(id):
    conn = izveidot_savienojumu()
    ideja = conn.execute("SELECT * FROM idejas WHERE apraksts_ID = ?", (id,)).fetchone()
    conn.close()

    if ideja is None:
        abort(404)


    return ideja

app = Flask(__name__)
app.config["SECRET_KEY"] = "Mēbeles"

@app.route("/")
def index():
    mebeles = izvelne.mebelu_saraksts()
    print(mebeles)
    return render_template("index.html", mebeles = mebeles) #mebelesINDEXlapaa un mebelesnoDB

#@app.route("/<int:ideja_id>")
@app.route("/ideja", methods=('GET', 'POST'))
def ideja():
    
    if request.method == 'POST':
            mebele = request.form.get("mebele")
            materials = request.form.get("materials")
            tehnika = request.form.get("tehnika")
            stils = request.form.get("stils")
            #print(mebele, materials, tehnika, stils)

    idejasid = atjaunosanas_kods.izveleta_konkreta_ideja(mebele, materials, tehnika, stils) #?
    ideja = atjaunosanas_kods.test_izveleta_konkreta_ideja_apraksts(2)
    return render_template("ideja.html", ideja = ideja, idejasid = idejasid)

@app.route("/pieslegties")
def pieslegties():
    if request.method == 'POST':
        pers_kods = request.form.get("pers_kods")
        parole = request.form.get("parole")

        print(pers_kods, parole)

    if darbinieka_piekluve.parbaude(pers_kods, parole):
         return render_template("darbinieka_lapa.html")
    else:
        flash("Pieteikšanās neveiksmīga")   
    return render_template("pieslegties.html")



if __name__ == "__main__":
    app.run(debug = True)

