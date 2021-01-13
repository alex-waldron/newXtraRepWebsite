from flask import Blueprint, render_template

bp = Blueprint("appFeatures", __name__)

@bp.route("/app-features")
def appFeatures():
    return render_template('appFeatures/appFeatures.html')