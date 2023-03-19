import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, url_for, flash, redirect
import iespieddarbi
import mekletajs
import lietotaji
import lasitava

app = Flask(__name__)
app.config["SECRET_KEY"] = "Biblioteka2023!"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/meklet", methods=('GET', 'POST'))
def meklet():
    if request.method == 'POST':
        vards = request.form["autors_vards"]
        uzvards = request.form["autors_uzvards"]
        nosaukums = request.form["nosaukums"]
        gads = request.form["gads"]
        izdevejs = request.form["izdevejs"]
        numurs = request.form["numurs"]
        veids = request.form.get("veids")

        print(veids, vards, uzvards, nosaukums, gads, izdevejs, numurs)

        if veids not in iespieddarbi.kategorijas_combolist:
            flash("Izvēlies iespieddarba veidu")

        else:
            if veids == "grāmata":
                atrasts = mekletajs.meklet_gramatu(vards, uzvards, nosaukums)
                rezultati = mekletajs.rezultatu_tabula(atrasts)
                print(rezultati)

            elif veids == "periodika":
                atrasts = mekletajs.meklet_periodiku(nosaukums, gads, numurs)
                rezultati = mekletajs.rezultatu_tabula(atrasts)
                print(rezultati)

            return render_template("rezultati.html", rezultati=rezultati)

    return render_template("meklet.html")


@app.route("/pieslegties", methods=('GET', 'POST'))
def pieslegties():
    if request.method == 'POST':
        pers_kods = request.form.get("pers_kods")
        parole = request.form.get("parole")

        print(pers_kods, parole
              )
        if lietotaji.parbaude(pers_kods, parole):
            return render_template("darbinieka_landing_page.html")
        else:
            flash("Pieteikšanās neveiksmīga")

    return render_template("pieslegties.html")


@app.route("/pievienot_lasitaju", methods=('GET', 'POST'))
def pievienot_lasitaju():
    if request.method == "POST":
        kategorija = request.form.get("kategorija")
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        personas_kods = request.form["personas_kods"]
        talrunis = request.form["talrunis"]
        parole = request.form["parole"]
        datums = datetime.now().date()

        if vards == "" or uzvards == "" or personas_kods == "" or talrunis == "":
            flash('Nav aizpildīti lietotāja pievienošanai nepieciešamie lauki.')

        else:
            if kategorija == "lasītājs":
                lasitajs = lietotaji.Lasitajs(vards, uzvards, personas_kods, talrunis, datums)
                lietotaji.saglabat_db(lasitajs)
            elif kategorija == "darbinieks":
                if parole == "":
                    flash('Darbiniekam nepieciešama parole.')
                else:
                    darbinieks = lietotaji.Darbinieks(vards, uzvards, personas_kods, talrunis, datums, parole)
                    lietotaji.saglabat_db(darbinieks)
            else:
                flash('Nav izvēlēta lietotāja kategorija.')


    return render_template("pievienot_lasitaju.html")


@app.route("/pievienot_iespieddarbu", methods=('GET', 'POST'))
def pievienot_iespieddarbu():
    if request.method == 'POST':
        veids = request.form.get("veids")
        vards = request.form["autors_vards"]
        uzvards = request.form["autors_uzvards"]
        nosaukums = request.form["nosaukums"]
        gads = request.form["gads"]
        izdevejs = request.form["izdevejs"]
        numurs = request.form["numurs"]
        pieejamais_skaits = request.form["pieejamais_skaits"]
        plaukta_numurs = request.form["plaukta_numurs"]

        if veids == "grāmata":
            if vards == "" or uzvards == "" or nosaukums == "" or gads == "" or izdevejs == "" or pieejamais_skaits == "" or plaukta_numurs == "":
                flash('Nav aizpildīti grāmatas pievienošanai nepieciešamie lauki.')
            else:
                gramata = iespieddarbi.Gramata(izdevejs, vards, uzvards, nosaukums, gads,
                                               pieejamais_skaits, plaukta_numurs)
                gramata.saglabat_db()

        elif veids == "periodika":
            if nosaukums == "" or gads == "" or numurs == "" or pieejamais_skaits == "" or plaukta_numurs == "":
                flash('Nav aizpildīti periodikas pievienošanai nepieciešamie lauki.')
            else:
                periodika = iespieddarbi.Periodika(izdevejs, nosaukums, gads, numurs, pieejamais_skaits, plaukta_numurs)
                periodika.saglabat_db()

        else:
            flash('Nav izvēlēts iespieddarba veids.')

    return render_template("pievienot_iespieddarbu.html")


@app.route("/lasitavas_darbs", methods=('GET', 'POST'))
def lasitavas_darbs():
    rezultati = {}
    if request.method == 'POST':

        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        personas_kods = request.form["personas_kods"]

        lasitaja_id = mekletajs.meklet_lasitaju(vards, uzvards, personas_kods)

        if lasitaja_id == -1:
            flash("Lasītājs nav atrasts.")
        else:
            lasitajs = mekletajs.lasitaja_dati(lasitaja_id)
            izdevuma_id = request.form["izdevuma_id"]
            termins = request.form["termins"]

            lasitaja_id = mekletajs.meklet_lasitaju(vards, uzvards, personas_kods)
            numurs = lasitava.izsniegt(lasitaja_id, izdevuma_id, termins)

            rezultati["Izsnieguma Nr."] = numurs
            rezultati["Vārds:"] = lasitajs["vards"]
            rezultati["Uzvārds"] = lasitajs["uzvards"]
            rezultati["Iespieddarbs"] = mekletajs.izdevuma_info(izdevuma_id)
            rezultati["Nodošanas termiņš"] = termins

            return render_template("parskats.html", rezultati=rezultati)


    return render_template("lasitava.html")

@app.route("/darbinieku_izvelne")
def darbinieku_izvelne():
    return render_template("darbinieka_landing_page.html")

@app.route("/sanemsana", methods=('GET', 'POST'))
def sanemsana():
    rezultati = {}
    if request.method == "POST":
        izsnieguma_id = request.form["izsnieguma_id"]
        status = lasitava.atdot(izsnieguma_id)
        if status:
            kavejuma_nauda = lasitava.aprekinat_kavejuma_naudu(izsnieguma_id)
            rezultati["Statuss: "] = "Nodošana apstiprināta."
            rezultati["Aprēķināta kavējuma nauda"] = kavejuma_nauda

            return render_template("parskats.html", rezultati=rezultati)
        else:
            flash("Šāda izsnieguma numura nav.")

    return render_template("sanemsana.html")

if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
