

from flask import Blueprint, render_template

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/test2', methods=('GET',))
def test2():
    return render_template('test/test.html')