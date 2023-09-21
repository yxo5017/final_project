from flask import Flask, abort, request, jsonify
from models import db, setup_db, Movie, Actor, movie_actor
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/movie-list')
    @requires_auth('get:movies')
    def movieList(): 
        movies = Movie.query.all()
        formatted_movie = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movie
        })

    @app.route('/actor-list')
    @requires_auth('get:actors')
    def actorList(): 
        actors = Actor.query.all()
        formatted_actor = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actor': formatted_actor
        })

    @app.route('/movie/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def movieDetail(movie_id): 
        movies = Movie.query.all()
        formatted_movie = [movie.format() for movie in movies]
        movie_detail = [item for item in formatted_movie if item["id"] == movie_id]
        return jsonify({
            'movie_id': movie_detail,
            'success': True,
        })  

    @app.route('/actor/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def actorDetail(actor_id): 
        actors = Actor.query.all()
        formatted_actor = [actor.format() for actor in actors]
        actor_detail = [item for item in formatted_actor if item["id"] == actor_id]
        return jsonify({
            'actor_id': actor_detail,
            'success': True,
        })  

    @app.route('/movie-edit/<int:movie_id>', methods=['GET'])
    @requires_auth('patch:movies')
    def movieEdit(movie_id): 
        movies = Movie.query.all()
        formatted_movie = [movie.format() for movie in movies]
        movie_detail = [item for item in formatted_movie if item["id"] == movie_id]
        return jsonify({
            'movie_id': movie_detail,
            'success': True,
        })  
    
    @app.route('/actor-edit/<int:actor_id>', methods=['GET'])
    @requires_auth('patch:actors')
    def actorEdit(actor_id): 
        actors = Actor.query.all()
        formatted_actor = [actor.format() for actor in actors]
        actor_detail = [item for item in formatted_actor if item["id"] == actor_id]
        return jsonify({
            'actor_id': actor_detail,
            'success': True,
        })  
    
    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def actorDelete(actor_id): 
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            
            actor.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

        return jsonify({
            'success': True,
        })  
    
    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def movieDelete(movie_id): 
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            
            movie.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

        return jsonify({
            'success': True,
        })  
    

    @app.route('/actor-post', methods=['POST'])
    @requires_auth('post:actors')
    def actorPost(): 
        body = request.get_json()
        
        new_fname = body.get('first_name')
        new_lname = body.get('last_name')
        new_email = body.get('email')
        new_age = body.get('age')
        new_gender = body.get('gender')
        new_tel = body.get('tel_number')
        new_msg = body.get('message')
        new_image = body.get('image_url')

        try:
            actor = Actor(first_name=new_fname, last_name=new_lname, email=new_email, age=new_age, gender=new_gender, tel_number=new_tel, message=new_msg, image_url=new_image)
            actor.insert()

            return jsonify({
                'success': True,
            })  
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movie-post', methods=['POST'])
    @requires_auth('post:movies')
    def moviePost(): 
        body = request.get_json()
        
        new_title = body.get('title')
        new_release_date = body.get('release_date')
        new_msg = body.get('message')
        new_image = body.get('image_url')

        try:
            movie = Movie(title=new_title, release_date=new_release_date, message=new_msg, image_url=new_image)
            movie.insert()

            return jsonify({
                'success': True,
            })  
        except Exception as e:
            print(e)
            abort(422) 

    @app.route('/movie-edit/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def movieSubmit(movie_id): 
        
        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body.get('title', movie.title)  # If 'title' isn't in body, keep the existing value
                movie.release_date = body.get('release_date', movie.release_date)
                movie.message = body.get('message', movie.message)
                movie.image_url = body.get('image_url', movie.image_url)
                
                # Assuming you're using Flask-SQLAlchemy
                db.session.commit()

            return jsonify({
                'success': True,
            })  
        except Exception as e:
            print(e)
            abort(422) 

    @app.route('/actor-edit/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def actorSubmit(actor_id): 
        
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            if 'first_name' in body:
                actor.first_name = body.get('first_name', actor.first_name)  # If 'title' isn't in body, keep the existing value
                actor.last_name = body.get('last_name', actor.last_name)
                actor.email = body.get('email', actor.email)
                actor.age = body.get('age', actor.age)
                actor.tel_number = body.get('tel_number', actor.tel_number)
                actor.gender = body.get('gender', actor.gender)
                actor.message = body.get('message', actor.message)
                actor.image_url = body.get('image_url', actor.image_url)
                
                # Assuming you're using Flask-SQLAlchemy
                db.session.commit()

            return jsonify({
                'success': True,
            })  
        except Exception as e:
            print(e)
            abort(422) 

    @app.route('/actor/<int:actor_id>/movies', methods=['GET'])
    @requires_auth('patch:movies')
    def get_movies_by_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({'error': 'Order not found'}), 404
        movies = [{'id':movie.id, 'name':movie.title} for movie in actor.movies]
        return jsonify(movies)

    @app.route('/movie/<int:movie_id>/actors', methods=['GET'])
    @requires_auth('patch:actors')
    def get_actors_by_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'error': 'Actor not found'}), 404
        actors = [{'id':actor.id, 'first_name':actor.first_name, 'last_name':actor.last_name} for actor in movie.actors]
        return jsonify(actors)

    @app.route('/update-movie-actors', methods=['POST'])
    @requires_auth('patch:actors')
    def update_movie_actors():
        data = request.json
        movie_id = data['movieId']
        actor_ids = set(data['actorIds'])

        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        # 現在関連付けられている俳優のIDを取得
        current_actor_ids = set(actor.id for actor in movie.actors)

        # 削除する必要がある俳優を特定
        for actor_id in current_actor_ids - actor_ids:
            actor = Actor.query.get(actor_id)
            movie.actors.remove(actor)

        # 追加する必要がある俳優を特定
        for actor_id in actor_ids - current_actor_ids:
            actor = Actor.query.get(actor_id)
            movie.actors.append(actor)

        db.session.commit()
        return jsonify({"message": "Updated successfully"})

    @app.route('/update-actor-movies', methods=['POST'])
    @requires_auth('patch:movies')
    def update_actor_movies():
        data = request.json
        actor_id = data['actorId']
        movie_ids = set(data['movieIds'])

        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({"error": "Actor not found"}), 404

        # 現在関連付けられている俳優のIDを取得
        current_movie_ids = set(movie.id for movie in actor.movies)

        # 削除する必要がある俳優を特定
        for movie_id in current_movie_ids - movie_ids:
            movie = Movie.query.get(movie_id)
            actor.movies.remove(movie)

        # 追加する必要がある俳優を特定
        for movie_id in movie_ids - current_movie_ids:
            movie = Movie.query.get(movie_id)
            actor.movies.append(movie)

        db.session.commit()
        return jsonify({"message": "Updated successfully"})
    
    return app
