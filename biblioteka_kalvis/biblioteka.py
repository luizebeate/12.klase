from datetime import datetime

import PySimpleGUI as sg

import iespieddarbi
import lasitava
import lietotaji
import mekletajs

sg.theme('SystemDefault')

# darbinieka ielogošanās loga izveide
pieteiksanas = [[sg.Text('Ievadi personas kodu un paroli')],
                [sg.Text('Personas kods', size=(15, 1)), sg.InputText(key="-personas-kods-")],
                [sg.Text('Parole', size=(15, 1)), sg.InputText(password_char='*', key="-parole-")],
                [sg.Button("Pieteikties")]]

# meklēšanas forma
meklesanas = [[sg.Text('Meklēt')],
              [sg.Text('Izdevuma veids', size=(15, 1)),
               sg.Combo(values=iespieddarbi.kategorijas_combolist, key="-mekl-izdevuma-veids-")],
              [sg.Text('Autora vārds', size=(15, 1)), sg.InputText(key="-mekl-autors-vards-")],
              [sg.Text('Autora uzvārds', size=(15, 1)), sg.InputText(key="-mekl-autors-uzvards-")],
              [sg.Text('Nosaukums', size=(15, 1)), sg.InputText(key="-mekl-nosaukums-")],
              [sg.Text('Gads', size=(15, 1)), sg.InputText(key="-mekl-gads-")],
              [sg.Text('Izdevējs', size=(15, 1)), sg.InputText(key="-mekl-izdevejs-")],
              [sg.Text('Numurs', size=(15, 1)), sg.InputText(key="-mekl-numurs-")],
              [sg.Button("Meklēt", key="-meklet-darbu-")],
              [sg.HSeparator()],
              [sg.Table(values=[['', '', '', '', '', '']], expand_x=True,
                        headings=['ID', 'Autors', 'Nosaukums', 'Gads', 'Izdevējs', 'Numurs'], max_col_width=45,
                        auto_size_columns=True, display_row_numbers=False, justification='left', num_rows=15,
                        key='-MEKLESANAS-REZULTATI-')]]

# Iespieddarbu pievienošanas forma
pievienosana = [[sg.Text('Pievienot')],
                [sg.Text('Autora vārds', size=(15, 1)), sg.InputText(key="-autors-vards-")],
                [sg.Text('Autora uzvārds', size=(15, 1)), sg.InputText(key="-autors-uzvards-")],
                [sg.Text('Nosaukums', size=(15, 1)), sg.InputText(key="-nosaukums-")],
                [sg.Text('Gads', size=(15, 1)), sg.InputText(key="-gads-")],
                [sg.Text('Izdevējs', size=(15, 1)), sg.InputText(key="-izdevejs-")],
                [sg.Text('Numurs', size=(15, 1)), sg.InputText(key="-numurs-")],
                [sg.Text('Pieejamais skaits', size=(15, 1)), sg.InputText(key="-pieejamais-skaits-")],
                [sg.Text('Plaukta Nr.', size=(15, 1)), sg.InputText(key="-plaukta-nr-")],
                [sg.Text('Izdevuma veids', size=(15, 1)),
                 sg.Combo(values=iespieddarbi.kategorijas_combolist, key="-izdevuma-veids-")],
                [sg.Button("Pievienot", key="-pievienot-iespieddarbu-")]]

# Lietotāju pievienošana
pievienosana_lietotajs = [[sg.Text('Pievienot')],
                          [sg.Text('Vārds', size=(15, 1)), sg.InputText(key="-lietotajs-vards-")],
                          [sg.Text('Uzvārds', size=(15, 1)), sg.InputText(key="-lietotajs-uzvards-")],
                          [sg.Text('Personas kods', size=(15, 1)), sg.InputText(key="-lietotajs-personas-kods-")],
                          [sg.Text('Talrunis', size=(15, 1)), sg.InputText(key="-lietotajs-talrunis-")],
                          [sg.Text('Parole', size=(15, 1)), sg.InputText(key="-lietotajs-parole-")],
                          [sg.Text('Lietoāja kategorija', size=(15, 1)),
                           sg.Combo(values=lietotaji.kategorijas_combolist, key="-lietotajs-kategorija-")],
                          [sg.Button("Pievienot", key="-pievienot-lietotaju-")]]

# izsniegšanas skats
izsniegsana = [[sg.Text('Izsniegšana')],
               [sg.Text('Vārds', size=(15, 1)), sg.InputText(key="-las-vards-")],
               [sg.Text('Uzvārds', size=(15, 1)), sg.InputText(key="-las-uzvards-")],
               [sg.Text('Personas kods', size=(15, 1)), sg.InputText(key="-las-pk-")],
               [sg.Button("Atrast lietotāju", key="-las-atrast-")],
               [sg.Text('Izdevuma ID', size=(15, 1)), sg.InputText(key="-las_izd_id-")],
               [sg.CalendarButton("Atdošanas termiņš", target="-las-termins-", format="%Y-%m-%d", locale="lv_LV",
                                  begin_at_sunday_plus=1), sg.InputText(key="-las-termins-")],
               [sg.Button("Izsniegt", key="-las-izsniegt-", disabled=True)],
               [sg.HSeparator()],
               [sg.Text('Atdošana')],
               [sg.Text('Izsnieguma Nr.', size=(15, 1)), sg.InputText(key="-izsnieguma-nr-")],
               [sg.Button("Atdot", key="-atdosana-")],
               [sg.HSeparator()],
               [sg.Text('Kopsavilkums', expand_x=True, key="-kopsavilkums-")],
               [sg.HSeparator()],
               [sg.Text("Atskaites")]]

layout = [[sg.TabGroup([[sg.Tab('Meklēšana', meklesanas), sg.Tab('Pieteikšanās', pieteiksanas),
                         sg.Tab('Iespieddarbu pievienošana', pievienosana, visible=False),
                         sg.Tab('Lietotāju pievienošana', pievienosana_lietotajs, visible=False),
                         sg.Tab('Lasītāju apkalpošana', izsniegsana, visible=False)]])]]

window = sg.Window('Bibliotēka', layout, font=14)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'Pieteikties':
        personas_kods = values['-personas-kods-']
        parole = values["-parole-"]
        if lietotaji.parbaude(personas_kods, parole):
            sg.popup('Pieteikšanās veiksmīga')
            window['Pieteikšanās'].update(visible=False)
            window['Meklēšana'].update(visible=True)
            window['Iespieddarbu pievienošana'].update(visible=True)
            window['Lietotāju pievienošana'].update(visible=True)
            window['Lasītāju apkalpošana'].update(visible=True)
        else:
            print('Pieteikšanās neveiksmīga')

    if event == '-meklet-darbu-':
        vards = values['-mekl-autors-vards-']
        uzvards = values['-mekl-autors-uzvards-']
        nosaukums = values['-mekl-nosaukums-']
        gads = values['-mekl-gads-']
        izdevejs = values['-mekl-izdevejs-']
        numurs = values['-mekl-numurs-']
        veids = values['-mekl-izdevuma-veids-']
        if veids == "":
            sg.popup('Izvēlies veidu')
        else:
            if veids == "grāmata":
                atrasts = mekletajs.meklet_gramatu(vards, uzvards, nosaukums)
                rezultati = mekletajs.rezultatu_tabula(atrasts)
                window.find_element("-MEKLESANAS-REZULTATI-").update(values=rezultati)
            elif veids == "periodika":
                atrasts = mekletajs.meklet_periodiku(nosaukums, gads, numurs)
                rezultati = mekletajs.rezultatu_tabula(atrasts)
                window.find_element("-MEKLESANAS-REZULTATI-").update(values=rezultati)

    if event == "-pievienot-iespieddarbu-":
        veids = values["-izdevuma-veids-"]
        autors_vards = values["-autors-vards-"]
        autors_uzvards = values["-autors-uzvards-"]
        nosaukums = values["-nosaukums-"]
        gads = values["-gads-"]
        izdevejs = values["-izdevejs-"]
        numurs = values["-numurs-"]
        pieejamais_skaits = values["-pieejamais-skaits-"]
        plaukta_nr = values["-plaukta-nr-"]
        if veids == "grāmata":
            if autors_vards == "" or autors_uzvards == "" or nosaukums == "" or gads == "" or izdevejs == "" or pieejamais_skaits == "" or plaukta_nr == "":
                sg.popup('Nav aizpildīti grāmatas pievienošanai nepieciešamie lauki.')
            else:
                gramata = iespieddarbi.Gramata(izdevejs, autors_vards, autors_uzvards, nosaukums, gads,
                                               pieejamais_skaits, plaukta_nr)
                gramata.saglabat_db()
        elif veids == "periodika":
            if nosaukums == "" or gads == "" or numurs == "" or pieejamais_skaits == "" or plaukta_nr == "":
                sg.popup('Nav aizpildīti periodikas pievienošanai nepieciešamie lauki.')
            else:
                periodika = iespieddarbi.Periodika(izdevejs, nosaukums, gads, numurs, pieejamais_skaits, plaukta_nr)
                periodika.saglabat_db()
        else:
            sg.popup('Nav izvēlēts iespieddarba veids.')

        print('Pievienošana veiksmīga')

    if event == '-pievienot-lietotaju-':
        vards = values["-lietotajs-vards-"]
        uzvards = values["-lietotajs-uzvards-"]
        personas_kods = values["-lietotajs-personas-kods-"]
        talrunis = values["-lietotajs-talrunis-"]
        parole = values["-lietotajs-parole-"]
        kategorija = values["-lietotajs-kategorija-"]
        datums = datetime.now().date()
        if vards == "" or uzvards == "" or personas_kods == "" or talrunis == "":
            sg.popup('Nav aizpildīti lietotāja pievienošanai nepieciešamie lauki.')
        else:
            if kategorija == "lasītājs":
                lasitajs = lietotaji.Lasitajs(vards, uzvards, personas_kods, talrunis, datums)
                lietotaji.saglabat_db(lasitajs)
            elif kategorija == "darbinieks":
                if parole == "":
                    sg.popup('Darbiniekam nepieciešama parole.')
                else:
                    darbinieks = lietotaji.Darbinieks(vards, uzvards, personas_kods, talrunis, datums, parole)
                    lietotaji.saglabat_db(darbinieks)
            else:
                sg.popup('Nav izvēlēta lietotāja kategorija.')

    if event == '-las-atrast-':
        vards = values["-las-vards-"]
        uzvards = values["-las-uzvards-"]
        personas_kods = values["-las-pk-"]
        lasitaja_id = mekletajs.meklet_lasitaju(vards, uzvards, personas_kods)
        if lasitaja_id != -1:
            lasitajs = mekletajs.lasitaja_dati(lasitaja_id)
            window.find_element("-las-vards-").update(value=lasitajs["vards"])
            window.find_element("-las-uzvards-").update(value=lasitajs["uzvards"])
            window.find_element("-las-pk-").update(value=lasitajs["pers_kods"])
            window.find_element("-las-izsniegt-").update(disabled=False)

    if event == "-las-izsniegt-":
        vards = values["-las-vards-"]
        uzvards = values["-las-uzvards-"]
        personas_kods = values["-las-pk-"]
        izdevuma_id = values["-las_izd_id-"]
        termins = values["-las-termins-"]

        lasitaja_id = mekletajs.meklet_lasitaju(vards, uzvards, personas_kods)
        lasitajs = mekletajs.lasitaja_dati(lasitaja_id)

        numurs = lasitava.izsniegt(lasitaja_id, izdevuma_id, termins)

        izdevums = mekletajs.izdevuma_info(izdevuma_id)

        kopsavilkuma_teksts = f"Izsnieguma nr: {numurs}\nLasītājs: {vards}, {uzvards}\nIzdevums: {izdevums}\nNodošanas termiņš: {termins}"
        window.find_element("-kopsavilkums-").update(value=kopsavilkuma_teksts)

    if event == '-atdosana-':
        izsnieguma_id = int(values["-izsnieguma-nr-"])
        rezult = lasitava.atdot(izsnieguma_id)
        if rezult:
            kavejuma_nauda = lasitava.aprekinat_kavejuma_naudu(izsnieguma_id)
            kopsavilkuma_teksts = f"Nodošana apstiprināta. Aprēķināta kavējuma nauda {kavejuma_nauda}."
        else:
            kopsavilkuma_teksts = "Šāda izsnieguma numura nav."
        window.find_element("-kopsavilkums-").update(value=kopsavilkuma_teksts)

window.close()
