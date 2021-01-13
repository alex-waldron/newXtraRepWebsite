import functools

import click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import mySQLdb

import mysql.connector

from datetime import datetime

from xtraRep.auth import login_required
bp = Blueprint('createWorkoutPlan', __name__,
               url_prefix='/create-workout-plan')

muscleGroups = ['chest', 'back', 'triceps', 'biceps', 'shoulders', 'legs']

workoutdb = mySQLdb.get_mySQLdb()
WORKOUT_PLAN_IMAGE_FOLDER = "xtraRep/static/images/workoutPlanImages/"
WORKOUT_IMAGE_FOLDER = "xtraRep/static/images/workoutImages/"
EXERCISE_IMAGE_FOLDER = "xtraRep/static/images/exerciseImages/"


class SingleWorkout:

    def __init__(self, name, musclesWorked, user):
        self.name = name
        self.musclesWorked = musclesWorked
        self.dateCreated = datetime.now()
        self.user = user


class Exercise:

    def __init__(self, exerciseName, sets, reps, picOfExercise, notes):
        self.exerciseName = exerciseName
        self.sets = sets
        self.reps = reps
        self.picOfExercise = picOfExercise
        self.notes = notes


def getFileExtension(file):
    return file.filename.split('.')[-1]


@bp.route('/', methods=('GET', 'POST'))
@login_required
def createWorkoutPlanHome():
    return render_template('createWorkoutPlan/createWorkoutPlanHome.html')


@bp.route('/get-started', methods=('GET', 'POST'))
@login_required
def getStarted():

    if request.method == 'POST':
        workoutPlanName = request.form['workoutPlanName']
        workoutPlanDescription = request.form['workoutPlanDescription']
        programLength = request.form['programLength']
        programDifficulty = request.form['difficulty']

        workoutPlanPic = request.files['workoutPlanPicture']

        workoutPlanPicExt = getFileExtension(workoutPlanPic)

        db = mySQLdb.get_mySQLdb()
        cur = db.cursor()

        cur.execute(
            'INSERT INTO workoutPlans (user_id, workoutPlanName, workoutPlanDescription, programLength, programDifficulty) VALUES (%s,%s,%s,%s,%s)',
            (g.user['id'], workoutPlanName, workoutPlanDescription,
             programLength, programDifficulty)
        )
        db.commit()

        cur.execute(
            'SELECT LAST_INSERT_ID()'
        )
        workoutPlanId = cur.fetchone()[0]
        filename = str(workoutPlanId) + "." + workoutPlanPicExt
        mediaLoc = '"' + WORKOUT_PLAN_IMAGE_FOLDER + filename + '"'

        cur.execute(
            'UPDATE workoutPlans SET mediaLoc = {0} WHERE id={1}'.format(
                mediaLoc, workoutPlanId)
        )
        db.commit()
        workoutPlanPic.save(WORKOUT_PLAN_IMAGE_FOLDER + filename)
        return redirect(url_for('createWorkoutPlan.addWorkoutsToPlan', workoutPlanId=workoutPlanId))

    return render_template('createWorkoutPlan/getStarted.html')


@bp.route('/add-workouts-to-plan/<int:workoutPlanId>')
@login_required
def addWorkoutsToPlan(workoutPlanId):
    # CREATE LAYOUT FOR PROGRAM WHERE EACH DAY CAN BE CLICKED ON AND CREATED/EDITED
    db = mySQLdb.get_mySQLdb()
    cur = db.cursor()
    cur.execute(
        "SELECT programLength, workoutPlanName FROM workoutPlans WHERE id = {}".format(workoutPlanId)
    )
    queryResult = cur.fetchone()
    programLength = queryResult[0]
    workoutPlanName = queryResult[1]

    cur.execute(
        "SELECT dayForWorkout FROM workouts WHERE workoutPlanId = {}".format(workoutPlanId)
    )
    daysCompleted = cur.fetchall()
    adjustedList = [day[0] for day in daysCompleted]
    
    return render_template('createWorkoutPlan/addWorkoutsToPlan.html', numOfRows=int(programLength/8)+1, programLength=programLength, workoutPlanId=workoutPlanId, daysCompleted = adjustedList, workoutPlanName=workoutPlanName)


@bp.route('/add-workout/<int:day>/<int:workoutPlanId>', methods=('GET', 'POST'))
@login_required
def addWorkout(day, workoutPlanId):
    if request.method == 'POST':
        db = mySQLdb.get_mySQLdb()
        cursor = db.cursor()

        workoutPic = request.files['workoutPicture']

        workoutPicExtension = getFileExtension(workoutPic)

        nameOfWorkout = request.form["nameOfWorkout"]
        workoutDescription = request.form['workoutDescription']
        musclesWorked = request.form.getlist('musclesWorked')
        muscleWorkString = ""
        for muscle in musclesWorked:
            muscleWorkString = muscleWorkString + muscle + ","
        cursor.execute(
            'INSERT INTO workouts (user_id, workoutPlanId, dayForWorkout, workoutName, workoutDescription, musclesWorked) VALUES (%s,%s,%s,%s,%s,%s)',
            (g.user['id'], workoutPlanId, day, nameOfWorkout,
             workoutDescription, muscleWorkString)
        )
        db.commit()

        cursor.execute(
            'SELECT LAST_INSERT_ID()'
        )
        workoutId = cursor.fetchone()[0]
        saveFileLocation = WORKOUT_IMAGE_FOLDER + str(workoutId) + "." + workoutPicExtension
        workoutPic.save(saveFileLocation)
        cursor.execute(
            'UPDATE workouts SET mediaLoc = {0} WHERE id={1}'.format(
                '"' + saveFileLocation + '"', workoutId)
        )
        db.commit()

        return redirect(url_for('createWorkoutPlan.addExercises', workout_id=workoutId, workoutPlanId=workoutPlanId))
    return render_template('createWorkoutPlan/addWorkout.html')


@bp.route('/add-exercises/<int:workout_id>/<int:workoutPlanId>', methods=("GET", "POST"))
@login_required
def addExercises(workout_id, workoutPlanId):
    if request.method == 'POST':
        db = mySQLdb.get_mySQLdb()
        cursor = db.cursor()
        numExercises = 1

        while True:
            try:
                request.form['exerciseName{}'.format(numExercises)]
            except:
                break
            exerciseName = request.form['exerciseName{}'.format(numExercises)]
            #picOfExercise = request.form['picOfExercise{}'.format(numExercises)]
            sets = request.form.get('sets{}'.format(numExercises))
            pic = request.files['picOfExercise{}'.format(numExercises)]
            picExt = getFileExtension(pic)

            reps = request.form['reps{}'.format(numExercises)]
            notes = request.form['notesOnExercise{}'.format(numExercises)]
            cursor.execute(
                'INSERT INTO exercises (workout_id, exerciseName, numOfSets, reps, notes) VALUES (%s,%s,%s,%s,%s)',
                (workout_id, exerciseName, sets, reps, notes)
            )
            db.commit()
            cursor.execute(
                'SELECT LAST_INSERT_ID()'
            )
            exerciseId = cursor.fetchone()[0]
            saveFileLoc = EXERCISE_IMAGE_FOLDER + str(exerciseId) + "." + picExt

            cursor.execute(
            'UPDATE exercises SET mediaLoc = {0} WHERE id={1}'.format(
                '"' + saveFileLoc + '"', exerciseId)
            )
            db.commit()
            pic.save(saveFileLoc)
            numExercises = numExercises + 1
        return redirect(url_for('createWorkoutPlan.addWorkoutsToPlan', workoutPlanId=workoutPlanId))

    return render_template('createWorkoutPlan/addExercises.html')


@bp.route('load-user-workout-plans', methods=('GET', 'POST'))
@login_required
def loadUserWorkoutPlan():
    if request.method == 'POST':
        workoutPlanIdSelection = request.form["workoutPlanSelection"]
        return redirect(url_for("createWorkoutPlan.addWorkoutsToPlan", workoutPlanId=workoutPlanIdSelection))
    userId = g.user['id']
    db = mySQLdb.get_mySQLdb()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM workoutPlans WHERE user_id={}".format("'" + str(userId) + "'")
    )
    return render_template('createWorkoutPlan/loadUserWorkoutPlans.html', userWorkoutPlanList = cur.fetchall())
