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

@app.route("/")
def index():
    mebeles = izvelne.mebelu_saraksts()
    print(mebeles)
    
    return render_template("index.html", mebeles = mebeles) #mebelesINDEXlapaa un mebelesnoDB

    
@app.route("/<int:ideja_id>")
def ideja(ideja_id):

    ideja = atjaunosanas_kods.test_izveleta_konkreta_ideja_apraksts(ideja_id)
    return render_template("ideja.html", ideja = ideja)


@app.route("/pieslegties", methods=('GET', 'POST'))
def pieslegties():
    if request.method == 'POST':
        pers_kods = request.form.get("pers_kods")
        parole = request.form.get("parole")

        print(pers_kods, parole)
        if darbinieka_piekluve.parbaude(pers_kods, parole):
            return render_template("darbinieka_landing_page.html")
        else:
            flash("Pieteikšanās neveiksmīga")

    return render_template("pieslegties.html")


if __name__ == "__main__":
    app.run(debug = True)