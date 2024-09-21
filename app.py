import os
from flask import Flask
from flask.json import jsonify
from models import setup_db, create_data, Movie, Actor
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    
    @app.route('/init')
    def test_endpoint():
        create_data()
        
        actors = Actor.query.all()
        actors_list = []
        for actor in actors:
            actor_data = {
                'name': actor.name,
                
            }
            actors_list.append(actor_data)

        movies = Movie.query.all()
        movies_list = []
        for movie in movies:
            movie_data = {
                'name': movie.title,
                
            }
            movies_list.append(movie_data)
        
        return jsonify({
            'success': True,
            'actors': actors_list,
            'movies': movies_list

        })
        
    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        movies_list = [movie.format() for movie in movies]
       
        return jsonify ({
            'success': True,
            'movies': movies_list
        })
    
    @app.route('/movies/<int:movie_id>')
    def get_movie(movie_id):
        # get move by id
        movie = Movie.query.get(movie_id)
    
        # check if movie exists
        if movie is None:
            return jsonify({
                'success': False,
                'message': 'Movie not found'
            }), 404
        
        # data formating
        movie_data = {
            'title': movie.title,
            'release_date': str(movie.release_date),
            'actors': [actor.name for actor in movie.actors]
        }

        
        return jsonify({
            'success': True,
            'movie': movie_data
        })


    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        actors_list = [actor.format() for actor in actors]
               
        return jsonify({
            'success': True,
            'actors': actors_list
        })

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def get_actor(actor_id):
        # get actor by id
        actor = Actor.query.get(actor_id)
        
        # check if actor exists
        if actor is None:
            return jsonify({
                'success': False,
                'message': 'Actor not found'
            }), 404
        
        # data formating
        actor_data = {
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender,
            'movies': [movie.title for movie in actor.movies]  # Získání filmů, ve kterých hrál
        }
       
        return jsonify({
            'success': True,
            'actor': actor_data
        })


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
