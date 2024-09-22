import os, sys
from flask import Flask, abort, request, json
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
    
    @app.route('/movies', methods=['POST'])
    def post_movie():
        body = request.get_json()
    
        try:
            movie = Movie(title=body['title'], release_date=body['release_date'])
            
            actor_ids = body.get('actors', [])
            actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
        
            #actors added to movie
            movie.actors.extend(actors)
            movie.insert()
            
            return jsonify ({
                "success": True,
                "movie": movie.title,
                "actors": [actor.name for actor in movie.actors],
                "release_date": movie.release_date 
            })
            
        except Exception as e:
            print(f"Error: {e}")
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movie(movie_id):
        body = request.get_json()

        try:
            # find movie by id
            movie = Movie.query.get(movie_id)
            
            if movie is None:
                abort(404)

            # update title if present
            if 'title' in body:
                movie.title = body['title']

            # update release date if present
            if 'release_date' in body:
                movie.release_date = body['release_date']

            # update list of actors if present
            if 'actors' in body:
                actor_ids = body['actors']
                actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
                movie.actors = actors  # Přiřadíme nové herce k filmu

            
            movie.update()

            return jsonify({
                "success": True,
                "movie": movie.title,
                "actors": [actor.name for actor in movie.actors],
                "release_date": movie.release_date
            })

        except Exception as e:
            print(f"Error: {e}")
            abort(500)



    @app.route('/movies/<int:movie_id>')
    def get_movie(movie_id):
        # get move by id
        movie = Movie.query.get(movie_id)
    
        # check if movie exists
        if movie is None:
            abort(404)
        
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
            abort(404)
        
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

    """
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['description']
        })
        response.status_code = ex.status_code
        return response
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(500)
    def server_errror(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "An error occurred while processing your request."
        }), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found."
        }), 404

    return app




app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
