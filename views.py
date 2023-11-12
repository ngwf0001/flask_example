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
    movies = db.get_movies()
    print(movies)
    return render_template('movies.html', movies=sorted(movies))

def movie_page(movie_key):
    db =current_app.config['db']
    movie = db.get_movie(movie_key)
    if movie is  None:
        abort(404)
    return render_template('movie.html', movie=movie)

def movie_add_page():
    if request.method =="GET":
        return render_template('movie_edit.html', min_year=1887, max_year=dt.datetime.now().year)
    form_title = request.form['title']
    form_year = request.form['year']
    db = current_app.config['db']
    movie = Movie(form_title, int(form_year)) if form_year else None

    movie_key = db.add_movie(movie)
    return redirect(url_for('movie_page', movie_key=movie_key))