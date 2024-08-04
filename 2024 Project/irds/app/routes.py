from app import app
from flask import render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "birds.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import models and forms after app and extensions are initialized
from flask_login import UserMixin
from app.models import User, db
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def hello_world():
    return render_template('home.html', page_title="home", details="Steve")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('hello_world'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello_world'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # Here, you would typically send the reset email
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Here, you would typically verify the token and update the user's password
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)



import app.models as models
from app.forms import Add_Bird, SearchBirdForm


@app.route('/all_birds')
def all_birds():
    allbirds = models.Bird.query.all()
    return render_template("all_birds.html", allbirds=allbirds)


@app.route('/birds/<int:id>')
def single_bird(id):
    bird = models.Bird.query.filter_by(id=id).first()
    return render_template('bird.html', bird=bird)


@app.route('/add_bird', methods=['GET', 'POST'])
def add_bird():
    form = Add_Bird()
    if request.method == 'GET':
        return render_template('add_bird.html', form=form, title="Add A Bird")
    else:
        if form.validate_on_submit():
            new_bird = models.Bird()
            new_bird.name = form.name.data
            new_bird.maximum_lifespan = form.maximum_lifespan.data
            new_bird.description = form.description.data
            new_bird.status = form.status.data
            new_bird.habitats = form.habitats.data  # Add selected statuses
            db.session.add(new_bird)
            db.session.commit()
            return redirect(url_for('all_birds', all_birds=new_bird.id))
        else:
            return render_template('add_bird.html', form=form, title="Add A Bird")

from app.models import Bird, Habitat


@app.route('/search_bird', methods=['GET', 'POST'])
def search_bird():
    form = SearchBirdForm()
    birds = []
    if form.validate_on_submit():
        query = Bird.query
        if form.name.data:
            query = query.filter(Bird.name.ilike(f"%{form.name.data}%"))
        if form.habitat.data:
            query = query.filter(Bird.habitats.contains(form.habitat.data))
        birds = query.all()
    return render_template('search_bird.html', form=form, birds=birds)


@app.route('/triangles/<int:size>')
def triangle(size):
    if size <= 1:
        print("That isn't a triangle!")
    else:
        for i in range(1, size+1):
            print(i * '*')


if __name__ == "__main__":
    app.run(debug=True)
