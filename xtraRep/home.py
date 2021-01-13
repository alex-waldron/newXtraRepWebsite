from flask import Blueprint, render_template

bp = Blueprint("home", __name__)

@bp.route('/')
def home():
    return render_template('home/home.html')

@bp.route('/success')
def success():
    return render_template('home/success.html')