# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from email import message
# Créer un objet message vide
email_message = message.Message()

import json
import os 
import re
import re
motif = "python"
texte = "Ceci est un exemple de texte avec le mot python."
resultat = re.search(motif, texte)
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import AlertModel, UserModel, TaskModel, db, login, EtatTask # type: ignore
from werkzeug.utils import secure_filename
from flask_admin import AdminIndexView, expose, Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_adminlte3 import AdminLTE3

# Importation des packages faire faire l'interface
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier

app = Flask(__name__)
app.secret_key = 'dddnedd.ds.=e)zezççàezçz)èeèé"^à#@@#@'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/img"
app.config['UPLOAD_PP'] = "static/pp"

db.init_app(app)
login.init_app(app) # type: ignore
login.login_view = 'login' # type: ignore

def extension(fichier):
    return fichier.split(".")[-1]

# with app.app_context():
#     db.drop_all()
#     db.create_all()

@app.route('/accueil')
def accueil():
    return render_template("accueil.html")


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

    

@app.route("/task")
@login_required
def task():
    userTask=[{'alerte':AlertModel.query.get(task.id_alert),'user':UserModel.query.get(task.nomprenom), 'date_creation':task.date_creation, 'delai':task.delai,'etat':task.etat} for task in TaskModel.query.all() if task.nomprenom==current_user.id]
    for tache in userTask:
        print(tache)
    return render_template("task.html",userTask=userTask)


@app.route("/list", methods=['POST', 'GET'])
@login_required
def list():
    listAlerts=[AlertModel.query.get(x+1).to_json() for x in range(len(AlertModel.query.all()))] # type: ignore
    print(listAlerts)
    return render_template("list.html", listAlerts=listAlerts)


@app.route('/map', methods=['POST', 'GET'])
@login_required
def map():
    if request.method == "POST":
        try:
            id_alerte=AlertModel.query.get(len(AlertModel.query.all())).id+1 # type: ignore
        except:
            id_alerte=1
        try:
            titre = request.form['alerte_titre']
            typeAlert = request.form['type_alerte']
            print(typeAlert)
            message = request.form['alerte_message']
            # image = request.files['picture']
            picture="static/icon/default_alert.jpg"
            if request.files['picture']:
                UPLOAD_FOLDER=app.config["UPLOAD_FOLDER"]
                imageFiles = request.files.get('picture')
                file_base_name=imageFiles.filename
                filename = secure_filename(file_base_name)
                    # img_path=os.path.join(UPLOAD_FOLDER, id_alerte)
                    # os.mkdir(img_path)
                imageFiles.save(os.path.join(UPLOAD_FOLDER, str(id_alerte)+'_'+filename))
                picture=os.path.join(UPLOAD_FOLDER, str(id_alerte)+'_'+filename)
            x=request.form['xcoord']
            y=request.form['ycoord']
            auteurId = current_user.nomprenom
            contact=current_user.contact
            date_creation = datetime.now()
            if x!="" and typeAlert!="" and titre!="" and message!="":
                alerte=AlertModel(
                    auteurId=auteurId,
                    titre = titre,
                    typeAlert=typeAlert,
                    message=message,
                    picture=picture,
                    contact=contact,
                    x = x,
                    y = y,
                    date_creation = date_creation
                )
            db.session.add(alerte)
            db.session.commit()
            print("Nouvelle alerte ajouté")
        except:
            pass
        # listAlert=[AlertModel.query.get(x+1).to_json() for x in range(len(AlertModel.query.all()))]
        # print(listAlert)
        # print()
        # print(titre, typeAlerte, message,image, dateCreation)
        # return redirect('/map')
        # return render_template('map.html')
    listAlert=[AlertModel.query.get(x+1).to_json() for x in range(len(AlertModel.query.all()))]
    listAlertId=[str(AlertModel.query.get(x+1).id) for x in range(len(AlertModel.query.all()))]
    # print(listAlertId)
    listAlert=dict(zip(listAlertId,listAlert))
    print("Taille de dictionnaire",len(listAlert))
    # print(l2)
    # print(type(l2))
    # print(type(jsonify(l2)))
    return render_template('map.html',listAlert=json.loads(json.dumps(listAlert)),indent=2)

# @app.route("/map/json")
# def mapJson():
#     pass

@app.route('/login', methods=['POST', 'GET'])
def login():
        if request.form=="POST":      

            nomprenom = request.form['nomprenom']
            pasword= request.form['pasword']
            user = UserModel.query.filter_by(nomprenom=nomprenom).first()
            if current_user is not None and user.check_password(request.form['password']):
                login_user(user)
                return redirect("/formulaire")
                print('Remplissez le formulaire')
            # else:
            #     print("le nom ou le mot de pass incorrect, Veuillez réessayer!")
            #     return redirect("{url_for{'login}}")
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated and current_user.autorisation!="Admin":
        return redirect('/login')
    print("Déjà enregistré")    

    if request.method == 'POST':
        print("La requete d'enrégistrement d'utilisateur a été envoyée")
        contact = request.form['contact']
        nomprenom = request.form['nomprenom']
        password = request.form['password']
        autorisation = request.form['autorisation']
        fonction = request.form['fonction']
        print("---------------------------------")
        profile="static/icon/default_pp.jpg"
        # print(request.files.get('profile'))
        print("teste d'existance d'image")
        if request.files['profile']:
            print("Image exite")
            ext=extension(request.files.get('profile').filename)
            print("Extension de fichier:",ext)
            UPLOAD_PP=app.config["UPLOAD_PP"]
            imageFiles = request.files.get('profile')
            filename = secure_filename(nomprenom)
            profile=os.path.join(UPLOAD_PP,'_'+filename+'.'+ext)
            imageFiles.save(profile)
            print("Image sauvegardé")
        if UserModel.query.filter_by(contact=contact).first() or UserModel.query.filter_by(nomprenom=nomprenom).first():
            erreur_message='''  <div class="notification is-danger">
                                    <button class="delete"></button>
                                    Cet utilisateur existe déjà. Veillez changer le<strong>nom et le(s) prénom(s), ou le contact.</strong>
                                </div>
                            '''
            return erreur_message
        else:
            print("Essais d'enregistrement de l'utilisateur")
            user = UserModel(nomprenom=nomprenom, contact=contact, autorisation=autorisation, fonction=fonction,profile=profile)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    listUser=[UserModel.query.get(x+1) for x in range(len(UserModel.query.all()))]
    # print(listUser) 
    return render_template('register.html')

@app.route('/formulaire/', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nomprenom = request.form['nomprenom']
        print(f"Bonjour {nomprenom}")
        culture=request.form['culture']
        maraîchage = request.form['maraîchage']
        elevage = request.form['elevage']
        agri_vivriere = request.form['agri_vivriere']
        statut = request.form['statut']
        contact = request.form['contact']
        genre= request.form['genre']
        return f"Bonjour {nomprenom}"
    return render_template('formulaire.html')

@app.route('/traitement', methods =['POST','GET'])
def traitement():
    with open('mon_modele.pkl', 'rb') as f:
        model = pickle.load(f)
    return render_template('traitement.html')

@app.route('/resultat', methods=['POST','GET'])
def resultat():
    if request.method == 'POST':
        data = request.json
        # Prétraitement des données si nécessaire
        prediction = model.predict(data)
        return {'prediction': prediction.tolist()}
    return render_template('/resultat.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/map')

class AdminModelViewer(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.autorisation=="Admin"
    def inaccessible_callback(self,name,**kwargs):
        return redirect()


admin=Admin(app)

admin.add_view(AdminModelViewer(UserModel,db.session))
admin.add_view(AdminModelViewer(AlertModel,db.session))
admin.add_view(AdminModelViewer(TaskModel,db.session))
admin.add_view(AdminModelViewer(EtatTask,db.session))

app.run(host='0.0.0.0', port='8080', debug=True)


