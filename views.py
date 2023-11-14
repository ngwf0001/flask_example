import datetime as dt
from flask import current_app, render_template, request, redirect, url_for, abort
from movie import Movie
from forms import MovieEditForm

def validate_movie_form(form):
    form.data = {}
    form.errors = {}
    form_title = form.get("title","").strip()
    if len(form_title) == 0:
        form.errors["title"] = "Title can not be blank."
    else:
        form.data["title"] = form_title

    form_year = form.get("year")
    if not form_year:
        form.data["year"] = None
    elif not form_year.isdigit():
        form.errors["year"] = "Year must be a number."
    else:
        year =int(form_year)
        if (year < 1887) or (year > dt.datetime.now().year):
            form.errors["year"] = "Year not in valid range."
        else:
            form.data["year"] = year
    return form.errors == {}


#@app.route('/')
def home_page():
    today = dt.datetime.now()
    return render_template('home.html', day=today.strftime("%A (%Y-%m-%d)"))

# @app.route('/movies', endpoint='movies_endpoint')
def movies_page():
    db = current_app.config['db']
    if request.method == 'GET':
        movies = db.get_movies()
        return render_template('movies.html', movies=sorted(movies))
    else:
        form_movie_keys = request.form.getlist('movie_keys')
        for form_movie_key in form_movie_keys:
            db.delete_movie(int(form_movie_key))
        return redirect(url_for('movies_page'))

def movie_page(movie_key):
    db =current_app.config['db']
    movie = db.get_movie(movie_key)
    if movie is  None:
        abort(404)
    return render_template('movie.html', movie=movie)



def movie_add_page_check_manual():
    
    if request.method =="GET":
        values = {"title": "", "year": ""}
        return render_template('movie_edit.html', min_year=1887, max_year=dt.datetime.now().year, values=values)
    else:
        valid = validate_movie_form(request.form)
        if not valid:
            return render_template('movie_edit.html', min_year=1887, max_year=dt.datetime.now().year, values=request.form)
        form_title = request.form['title']
        form_year = request.form['year']
        db = current_app.config['db']
        movie = Movie(form_title, int(form_year) if form_year else None)

        movie_key = db.add_movie(movie)
        return redirect(url_for('movie_page', movie_key=movie_key))

def movie_add_page():
    form = MovieEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        year = form.data["year"]
        movie= Movie(title, year=year)
        db = current_app.config['db']
        movie_key = db.add_movie(movie)
        return redirect(url_for('movie_page', movie_key=movie_key))
    else:
        return render_template('movie_edit.html', form=form)


def movie_edit_page_check_manaul(movie_key):
    if request.method =="GET":
        db = current_app.config['db']
        movie = db.get_movie(movie_key)
        if movie is  None:
            abort(404)
        else:
            values = {"title": movie.title, "year": movie.year}
            return render_template('movie_edit.html', min_year=1887, max_year=dt.datetime.now().year, values=values)
    else:
        valid = validate_movie_form(request.form)
        if not valid:
            return render_template(
                "movie_edit.html",
                min_year=1887,
                max_year=datetime.now().year,
                values=request.form,
            )
        title = request.form.data["title"]
        year = request.form.data["year"]
        db = current_app.config['db']
        movie = Movie(title, year=year)
        db.update_movie(movie_key=movie_key, movie=movie)
        return redirect(url_for('movie_page', movie_key=movie_key))
    
def movie_edit_page(movie_key):
    db = current_app.config['db']
    movie = db.get_movie(movie_key)
    form = MovieEditForm()
    if form.validate_on_submit():
        title= form.data["title"]
        year = form.data["year"]
        movie= Movie(title, year=year)
        db.update_movie(movie_key=movie_key, movie=movie)
        return redirect(url_for('movie_page', movie_key=movie_key))
    else:
        form.title.data = movie.title
        form.year.data = movie.year if movie.year else ""
        return render_template('movie_edit.html', form=form)