# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from sqlalchemy_serializer import SerializerMixin

login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    localite = db.Column(db.String(80), unique=True)
    contact = db.Column(db.String(15), unique=True)
    nomprenom = db.Column(db.String(100),unique=True)
    password_hash = db.Column(db.String())
    autorisation = db.Column(db.String(100))
    fonction = db.Column(db.String(100))
    profile= db.Column(db.String(120))
    genre= db.Column(db.String(10), unique=True)
    niveauscolaite= db.Column(db.String(120))
    statut= db.Column(db.String(120))
    besoins= db.Column(db.String(200))
    superficie=db.Column(db.String(15), unique=True)

 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'> {self.nomprenom}'
 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class AlertModel(db.Model):
    __tablename__ = 'alert'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    auteurId=db.Column(db.String(80))
    titre = db.Column(db.String(125))
    typeAlert=db.Column(db.String(100))
    message=db.Column(db.String(5000))
    picture = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    x = db.Column(db.String(10))
    y = db.Column(db.String(10))
    date_creation = db.Column(db.String(125))

    def __repr__(self):
        return f'Type:{self.typeAlert} De:{self.auteurId} Le: {self.date_creation}>'

    def to_json(self):
        return dict(
                    auteurId=self.auteurId,
                    titre = self.titre,
                    typeAlert=self.typeAlert,
                    message=self.message,
                    picture=self.picture.replace("\\",'/'),
                    contact=self.contact,
                    x = self.x,
                    y = self.y,
                    date_creation = self.date_creation
            )

class EtatTask(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    etat=db.Column(db.String())

    def __repr__(self):
        return f'{self.etat}'


class TaskModel(db.Model):
    __tablename__ = 'tache'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_alert=db.Column(db.Integer,db.ForeignKey('alert.id')) 
    alert = db.relationship("AlertModel")
    id_utilisateur=db.Column(db.Integer,db.ForeignKey('users.id'))
    users = db.relationship("UserModel")
    etat=db.Column(db.Integer,db.ForeignKey('state.id'))
    state= db.relationship("EtatTask")
    date_creation = db.Column(db.DateTime)
    delai = db.Column(db.DateTime)
    def __repr__(self):
        return f'< tache {self.id}>'