from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from flask import url_for
import pandas as pd

input_columns = ['Support2023', 'Support12022', 'nbredealsupport12022', 'DealConclu2023', 'OpenDeals', 'Technologie', 'Support12021', 'nbredealsupport12021', 'nbredealsupport02023', 'DealConclu2021', 'annéeCreation', 'Moved', 'Support02023']

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/analytics')
def analytics():
    analytics_url = url_for('analytics')
    return render_template('Analytics.html', analytics_url=analytics_url)
@views.route('/predictions', methods=['GET', 'POST'], endpoint='predictions')
@login_required
def predictions():
    # Lire le fichier CSV
    data = pd.read_csv('dffinalaprèstest.csv.')

    # Extraire les noms de clients
    nom_clients = data['nomclient'].unique()




    # Extraire les noms de clients
    nom_clients = data['nomclient'].unique()

    if request.method == 'POST':
        # Récupérer la valeur sélectionnée depuis le formulaire
        selected_client = request.form.get('client')

        # Filtrer le DataFrame pour obtenir la ligne correspondante au client sélectionné
        client_row = data.loc[data['nomclient'] == selected_client]

        # Afficher la ligne correspondante
        return render_template('predictions.html', nom_clients=nom_clients, client_row=client_row)

    return render_template('predictions.html', nom_clients=nom_clients, user=current_user)


@views.route('/Forecast')
def Forecast():
    Forecast_url = url_for('forecast')
    return render_template('Forecast.html', Forecast_url=Forecast_url)