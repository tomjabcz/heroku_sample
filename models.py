from datetime import datetime
import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_data(): 
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()
    
    # create actors
    actor1 = Actor(name="Tom Hanks", age=64, gender="male")
    actor2 = Actor(name="Meryl Streep", age=71, gender="female")
    actor3 = Actor(name="Leonardo DiCaprio", age=46, gender="male")
    actor4 = Actor(name="Scarlett Johansson", age=36, gender="female")
    actor5 = Actor(name="Brad Pitt", age=57, gender="male")
    actor6 = Actor(name="Robert Downey Jr.", age=56, gender="male")
    actor7 = Actor(name="Jennifer Lawrence", age=31, gender="female")
    actor8 = Actor(name="Emma Watson", age=31, gender="female")
    actor9 = Actor(name="Chris Hemsworth", age=38, gender="male")
    actor10 = Actor(name="Morgan Freeman", age=84, gender="male")

    # create movies
    movie1 = Movie(title="The Post", release_date=datetime(2017, 12, 22))
    movie2 = Movie(title="Inception", release_date=datetime(2010, 7, 16))
    movie3 = Movie(title="Avengers: Endgame", release_date=datetime(2019, 4, 26))
    movie4 = Movie(title="Titanic", release_date=datetime(1997, 12, 19))
    movie5 = Movie(title="The Wolf of Wall Street", release_date=datetime(2013, 12, 25))

    # add actors to movies
    movie1.actors.extend([actor1, actor2])  # The Post: Tom Hanks, Meryl Streep
    movie2.actors.append(actor3)            # Inception: Leonardo DiCaprio
    movie3.actors.extend([actor6, actor9])  # Avengers: Robert Downey Jr., Chris Hemsworth
    movie4.actors.append(actor3)            # Titanic: Leonardo DiCaprio
    movie5.actors.extend([actor3, actor5])  # The Wolf of Wall Street: Leonardo DiCaprio, Brad Pitt

    # add actors who do not play in any movie
    db.session.add_all([actor4, actor7, actor8, actor10])  # Scarlett Johansson, Jennifer Lawrence, Emma Watson, Morgan Freeman (bez filmů)

    # inser everything in the database
    db.session.add_all([movie1, movie2, movie3, movie4, movie5])
    db.session.commit()


# Movies vs Actors: many to many realtionship
movie_actor = Table('movie_actor', db.Model.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)
    # Movies vs Actors: many to many realtionship
    actors = relationship('Actor', secondary=movie_actor, backref='movies')

    def __init__(self, title, release_date=None):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': str(self.release_date),
            'actors': [actor.format() for actor in self.actors]
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()



class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    
    def __init__(self, name, age=None, gender=None):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()




    
    