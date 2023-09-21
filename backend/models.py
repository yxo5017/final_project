import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql.schema import PrimaryKeyConstraint

database_name = "movie_theater"
database_path ="postgres://{}:{}@{}/{}".format('yosukeota', 'ohtapo4086','localhost:5432', database_name)

db = SQLAlchemy()

"""
setup_db
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
association_table
"""
movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

"""
Movie class
"""
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String)
    release_date = db.Column(Integer)
    image_url = db.Column(String)
    message = db.Column(String)
    actors = db.relationship('Actor', secondary=movie_actor, backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date, image_url, message):
        self.title = title
        self.release_date = release_date
        self.image_url = image_url
        self.message = message


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "image_url": self.image_url,
            "message": self.message,
        }

"""
Actor class
"""
class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String)
    last_name = db.Column(Integer)
    image_url = db.Column(String)
    age = db.Column(Integer)
    gender = db.Column(Boolean)
    tel_number = db.Column(String)
    email = db.Column(String)
    message = db.Column(String)

    def __init__(self, first_name, last_name, age, gender, tel_number, email, image_url, message):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.tel_number = tel_number
        self.email = email
        self.image_url = image_url
        self.message = message


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "tel_number": self.tel_number,
            "email": self.email,
            "image_url": self.image_url,
            "message": self.message,
        }