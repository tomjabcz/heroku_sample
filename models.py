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
  
  db.drop_all()
  db.create_all()
  
  actor1 = Actor(name="Tom Hanks", age=64, gender="male")
  actor2 = Actor(name="Meryl Streep", age=71, gender="female")

  # Vytvoření nového filmu
  new_movie = Movie(title="The Post", release_date=datetime(2017, 12, 22))

  # Přidání herců k filmu
  new_movie.actors.append(actor1)
  new_movie.actors.append(actor2)

  # Uložení změn do databáze
  db.session.add(new_movie)
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




    
    