import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'xtraRep.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #from . import db
    #db.init_app(app)

    from . import test, home, appFeatures, createWorkoutPlan, browseWorkoutPlans, contactUs, auth, api, appAuth, blog
    app.register_blueprint(test.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(appFeatures.bp)
    app.register_blueprint(createWorkoutPlan.bp)
    app.register_blueprint(browseWorkoutPlans.bp)
    app.register_blueprint(contactUs.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(appAuth.bp)
    app.register_blueprint(blog.bp)

    
    



    return app