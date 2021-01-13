from flask import Blueprint, render_template

bp = Blueprint('browseWorkoutPlans', __name__)

@bp.route('/browse-workout-plans')
def browseWorkoutPlans():
    return render_template('browseWorkoutPlans/browseWorkoutPlans.html')