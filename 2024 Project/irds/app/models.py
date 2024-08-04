from app.routes import db
from flask_login import UserMixin


BirdHabitats = db.Table('BirdHabitat',
                        db.Column('bid', db.Integer,
                                  db.ForeignKey('Bird.id')),
                        db.Column('hid', db.Integer,
                                  db.ForeignKey('Habitat.id')))

BirdRegions = db.Table('BirdRegion',
                       db.Column('bid', db.Integer,
                                 db.ForeignKey('Bird.id')),
                       db.Column('rid', db.Integer,
                                 db.ForeignKey('Region.id')))


class Bird(db.Model):
    __tablename__ = "Bird"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    maximum_lifespan = db.Column(db.Integer())
    similarity = db.Column(db.Text())
    photo = db.Column(db.Text())
    status_id = db.Column(db.Integer, db.ForeignKey('Status.id'))
    status = db.relationship('Status', backref='birdstatus')
    family_id = db.Column(db.Integer, db.ForeignKey('MainDiet.id'))
    family = db.relationship('MainDiet', backref='birdmaindiet')
    length_id = db.Column(db.Integer, db.ForeignKey('Length.id'))
    length = db.relationship('Length', backref='birdlength')
    habitats = db.relationship(
        'Habitat', secondary='BirdHabitat', back_populates='birds')
    regions = db.relationship(
        'Region', secondary='BirdRegion', back_populates='birds')


class Status(db.Model):
    __tablename__ = "Status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())


class MainDiet(db.Model):
    __tablename__ = "MainDiet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())


class Length(db.Model):
    __tablename__ = "Length"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())


class Habitat(db.Model):
    __tablename__ = "Habitat"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    birds = db.relationship('Bird', secondary='BirdHabitat',
                            back_populates='habitats')


class Region(db.Model):
    __tablename__ = "Region"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    birds = db.relationship(
        'Bird', secondary='BirdRegion', back_populates='regions')
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(20), unique=True, nullable=False)
    email = db.Column(db.Text(120), unique=True, nullable=False)
    password = db.Column(db.Text(60), nullable=False)


def __repr__(self):
    return self.name
