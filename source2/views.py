import datetime as dt
from flask import current_app, render_template, request, redirect, url_for, abort
from movie import Movie

# from server import app 

#@app.route('/')
def home_page():
    today = dt.datetime.now()
    return render_template('home.html', day=today.strftime("%A (%Y-%m-%d)"))

# @app.route('/movies', endpoint='movies_endpoint')
def movies_page():
    db = current_app.config['db']
    if request.method =="GET":
        movies = db.get_movies()
        return render_template('movies.html', movies=sorted(movies))
    else:
        form_movie_keys = request.form.getlist('movie_keys')
        for form_movie_key in form_movie_keys:
            db.delete_movie(form_movie_key)
        return redirect(url_for('movies_page'))

def movie_page(movie_key):
    db =current_app.config['db']
    movie = db.get_movie(movie_key)
    if movie is  None:
        abort(404)
    return render_template('movie.html', movie=movie)

def movie_add_page():
    if request.method =="GET":
        values = {"title": "", "year": ""}
        return render_template('movie_edit.html', 
                                min_year=1887, 
                                max_year=dt.datetime.now().year,
                                values=values)
    else:
        form_title = request.form['title']
        form_year = request.form['year']
        db = current_app.config['db']
        movie = Movie(form_title, int(form_year)) if form_year else None
        movie_key = db.add_movie(movie)
        return redirect(url_for('movie_page', movie_key=movie_key))
    
def movie_edit_page(movie_key):
    if request.method =="GET":
        db = current_app.config['db']
        movie = db.get_movie(movie_key)
        if movie is  None:
            abort(404)
        values = {"title": movie.title, "year": movie.year}
        return render_template('movie_edit.html', 
                                min_year=1887, 
                                max_year=dt.datetime.now().year,
                                values=values)
    else:
        form_title = request.form['title']
        form_year = request.form['year']
        db = current_app.config['db']
        movie = Movie(form_title, int(form_year)) if form_year else None
        db.update_movie(movie_key, movie)
        return redirect(url_for('movie_page', movie_key=movie_key))