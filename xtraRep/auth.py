import functools

from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from os import path

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
UPLOAD_FOLDER = 'xtraRep/static/images/profilepics/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from werkzeug.security import check_password_hash, generate_password_hash

from xtraRep.db import get_db

from xtraRep.mySQLdb import get_mySQLdb

bp = Blueprint('auth', __name__, url_prefix='/auth')



def correct_file_extension(fileName):
    fileParts = fileName.split('.')
    return len(fileParts) == 2 and fileParts[-1] in ALLOWED_EXTENSIONS
        

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        #get and save prof pic and create reference
        profilePicLoc = None
        if 'profilePic' not in request.files:
            flash("no profile pic")
        
        profilePic = request.files['profilePic']
        
        profPicExt = profilePic.filename.split('.')[-1]

        profilePicLoc = UPLOAD_FOLDER + username + '.' + profPicExt
        
        


        
        db = get_mySQLdb()
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE username="{}"'.format(username))

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'
        elif cur.fetchone() is not None:
            error = 'User {} is already registered'.format(username)
        
        if error is None:
            cur.execute(
                'INSERT INTO users (username, email, firstName, lastName, password, profilePicLoc) VALUES (%s,%s,%s,%s,%s,%s)',
                (username, email, firstName, lastName, generate_password_hash(password),  profilePicLoc)
            )
            db.commit()
            
            profilePic.save(profilePicLoc)
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            firstName = request.form['firstname']
        except BadRequestKeyError:
            username = request.form['username']
            password = request.form['password']
            db = get_mySQLdb()
            error = None
            toCheckPassword = ""
            cur = db.cursor()

            cur.execute(
                'SELECT username, password, id FROM users WHERE username = %s', (username,)
            )
            user = cur.fetchone()
            
            
            if user is None:
                error = 'Incorrect username'
            else:
                toCheckPassword = user[1]
                id = user[2]
                if not check_password_hash(toCheckPassword, password):
                    error = "Incorrect password"

            if error is None:
                session.clear()
                session['user_id'] = id
                return redirect(url_for('home.home'))
        else:
            lastName = request.form['lastname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            db = get_mySQLdb()
            cur = db.cursor()
            cur.execute('SELECT * FROM users WHERE username="{}"'.format(username))

            error = None
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required'
            elif cur.fetchone() is not None:
                error = 'User {} is already registered'.format(username)
            
            if error is None:
                cur.execute(
                    'INSERT INTO users (username, email, firstName, lastName, password) VALUES (%s,%s,%s,%s,%s)',
                    (username, email, firstName, lastName, generate_password_hash(password))
                )
                db.commit()

                cur.execute(
                    'SELECT username, password, id FROM users WHERE username = %s', (username,)
                )
                user = cur.fetchone()
                
                
                if user is None:
                    error = 'Incorrect username'
                else:
                    toCheckPassword = user[1]
                    id = user[2]
                    if not check_password_hash(toCheckPassword, password):
                        error = "Incorrect password"

                if error is None:
                    session.clear()
                    session['user_id'] = id
                return redirect(url_for('home.home'))
                
                
                
    
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_mySQLdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cursor.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

if __name__ =="__main__":
    print(correct_file_extension('home/pic.png'))