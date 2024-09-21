import os
from flask import Flask
from flask.json import jsonify
from models import setup_db, create_data, Movie, Actor
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    
    @app.route('/test')
    def test_endpoint():
        create_data()
        return "hotovo"
        

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        movies_list = [movie.format() for movie in movies]
       
        return jsonify ({
            'success': True,
            'movies': movies_list
        })
    
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        actors_list = [actor.format() for actor in actors]
               
        return jsonify({
            'success': True,
            'actors': actors_list
        })



    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
