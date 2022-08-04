from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

class User(db.Model, UserMixin):
    __tablename__="users"
    username = db.Column(db.String(20),primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    typeUser = db.Column(db.Integer, nullable=False)
    seller = db.relationship('Seller', backref= 'user', uselist= False )
    buyer =  db.relationship('Buyer', backref= 'user', uselist= False )
    lab =  db.relationship('Lab', backref= 'user',passive_deletes=True, uselist= False )
    def get_id(self):
        return self.username
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.typeUser}')"



class Seller(db.Model):
    __tablename__="sellers"
    sID = db.Column(db.String(20), db.ForeignKey('users.username',ondelete='CASCADE' ), primary_key=True)
    report= db.relationship('Report', backref= 'seller',passive_deletes=True, lazy= 'dynamic')


class Buyer(db.Model):
    __tablename__="buyers"
    bID = db.Column(db.String(20), db.ForeignKey('users.username' ,ondelete='CASCADE'),primary_key=True)
    report = db.relationship('Report', backref= 'buyer',passive_deletes=True,lazy= 'dynamic')

class Lab(db.Model):
    __tablename__="labs"
    lID = db.Column(db.String(20), db.ForeignKey('users.username' ,ondelete='CASCADE'),primary_key=True)
    report = db.relationship('Report', backref= 'lab',passive_deletes=True, lazy= 'dynamic')

class Report(db.Model):
    sID = db.Column(db.String(20),db.ForeignKey('sellers.sID',ondelete='CASCADE' ),nullable=False)
    bID = db.Column(db.String(20),db.ForeignKey('buyers.bID' ,ondelete='CASCADE'),nullable=False)
    lID=db.Column(db.String(20),db.ForeignKey('labs.lID',ondelete='CASCADE' ))
    uID = db.Column(db.String(50), primary_key=True)
    grossCalorificValue = db.Column(db.Float)
    netCalorificValue = db.Column(db.Float)
    testDate= db.Column(db.DateTime)
    validityFlag=db.Column(db.Boolean,default=True)
