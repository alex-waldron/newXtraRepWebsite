import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash

from xtraRep.mySQLdb import get_mySQLdb

#import mySQLdb

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/getAllPrograms.json', methods=(['GET']))
def getAllPrograms():
    db = get_mySQLdb()
    cur = db.cursor(dictionary=True)
    cur.execute(
        'SELECT * FROM workoutPlans'
    )
    workouts = cur.fetchall()


    #GET DATA FROM MYSQL AND JSONIFY IT
    return jsonify(workouts)



@bp.route('/<int:workoutId>/getProgramById.json', methods=(['GET']))
def getProgramById(workoutId):
    db = get_mySQLdb()
    cur = db.cursor(dictionary=True)
    cur.execute(
        'SELECT * FROM workoutPlans WHERE id = %s', (workoutId,)
    )
    return jsonify(cur.fetchone())


@bp.route('/getAllWorkouts.json', methods=(['GET']))
def getAllWorkouts():
    db = get_mySQLdb()
    cur = db.cursor(dictionary=True)
    cur.execute(
        'SELECT * FROM workouts'
    )
    return jsonify(cur.fetchall())