from flask import Blueprint, render_template

bp = Blueprint('contactUs', __name__)

@bp.route('/contact-us', methods=('GET','POST'))
def contactUs():
    return render_template("contactUs/contactUs.html")