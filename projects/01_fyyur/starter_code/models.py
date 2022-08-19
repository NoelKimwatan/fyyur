
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
from sqlalchemy.ext.hybrid import hybrid_property


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    image_link = db.Column(db.String(500),nullable=True)
    facebook_link = db.Column(db.String(120),nullable=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500),nullable=True)
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(200))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    all_shows = db.relationship('Show',backref='Venue',lazy=True,collection_class=list)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)




  

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500),nullable=True)
    facebook_link = db.Column(db.String(120),nullable=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500),nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False,nullable=False)
    seeking_description = db.Column(db.String(200),nullable=True)
    past_shows_count= db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    all_shows = db.relationship('Show',backref='Artist',lazy=True,collection_class=list)

    def __repr__(self) :
        return str(self.name)

    def __str__(self):
        return str(self.name)



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=True)
    start_time = db.Column(db.String,nullable=False)

    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),nullable=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=True)


    def __repr__(self):
        return str(self.name)


    def __str__(self):
        return str(self.name)

    @property
    def venue_name(self):
        try:
            return self.Venue.name
        except:
            return "Venue Deleted"

    @property
    def artist_name(self):
        try:
            return self.Artist.name
        except:
            return "Artist deleted"

    @property
    def artist_image_link(self):
        try:
            return self.Artist.image_link
        except:
            return "Artist deleted"


