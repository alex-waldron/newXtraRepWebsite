from flask import Blueprint, render_template

bp = Blueprint("blog", __name__)

@bp.route("/blog")
def blog():
    return render_template('blog/blog.html')