'''
Blueprint of flask app which contains login, signup and logout page urls
'''
from flask import Blueprint, render_template, request, flash, redirect, url_for
#  import the use table from the database for adding the quering users

from .models import User                                                   
# password hashing library so that when we store the password in the database it will be in hashed format.
from werkzeug.security import generate_password_hash, check_password_hash 

# importing databse to create connection and commiting changes 
from . import db                                              

# importing various flask login funtions for restricting only logged in user to use the functionalities of the website
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)



# route for login its logic defined
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # getiing all the information from frontend
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            # validating password for login
            if check_password_hash(user.password, password):
                # flash message in screen
                flash('Logged in successfully!', category='success')
                # remember the user and for that user only goto home page 
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



# route for logout
@auth.route('/logout')
# login is required to logout.
@login_required
def logout():
    # when logout button is pressed in the navbar the user is logges out from home page and goes to the login page
    logout_user()
    return redirect(url_for('auth.login'))


# route for signup its logic defined
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        # rules defined for values entered
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        else:
            # adding user with hashed password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # for this user goto home page
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
