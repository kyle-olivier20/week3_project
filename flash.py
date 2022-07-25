from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from login_check import LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'cf8b797bab3e5b3a5ed1f6d02ab32de0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.password})"


@app.route("/")
def home_page():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')


@app.route("/about")
def about_page():
    return render_template('about.html', subtitle='About Page', text='This is the about page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('/home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET'])
def login_page():
    log = LoginForm()
    if log.validate_on_submit():  # checks if entries are valid
        if log.validate_on_submit():
            user = User(username=log.username.data, email=log.email.data, password=log.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {log.username.data}!', 'success')
            return redirect(url_for('/home')) # if so - send to home page
    return render_template('login.html', subtitle='Login Page', form = log)

def check_password_hash(pw_hash, password):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.generate_password_hash(User.password, salt)
    bcrypt.check_password_hash(pw_hash, User.password)


if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")
