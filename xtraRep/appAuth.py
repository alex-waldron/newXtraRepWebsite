from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from xtraRep.mySQLdb import get_mySQLdb

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("appAuth",__name__, url_prefix="/appAuth")

@bp.route('/checkLogin', methods= ['POST'])
def checkLogin():
    if request.method == 'POST':
        jsonUserPass = request.json

        returnDict = {
            'userId': None,
            'error': None
        }
        print(jsonUserPass)
        email = jsonUserPass['email']
        password = jsonUserPass['password']
        db = get_mySQLdb()
        cur = db.cursor()
        cur.execute(
            "SELECT id FROM appUsers WHERE email={}".format('"' + email + '"')
        )
        appUserId = cur.fetchone()
        if appUserId:
            #if found, the id is returned as a tuple so extract the id value
            appUserId = appUserId[0]

            #GET password to check hash
            cur.execute(
                "SELECT password FROM appUsers WHERE id = {}".format(appUserId)
            )
            dbPassword = cur.fetchone()
            if check_password_hash(password, dbPassword):
                returnDict['userId'] = appUserId
            else:
                returnDict['error'] = "incorrect password"

        else:
            returnDict['error'] = "user not registered"
        return jsonify(returnDict)

@bp.route('/registerAppUser', methods= ['POST'])
def registerAppUser():
    if request.method == 'POST':
        jsonDict = request.json

        registerError = None
        email = jsonDict["email"]
        password = jsonDict["password"]
        firstName = jsonDict["firstName"]
        lastName = jsonDict["lastName"]

        db = get_mySQLdb()
        cur = db.cursor()

        cur.execute(
            'SELECT id FROM appUsers WHERE email = %s', (email,)
        )

        if cur.fetchall():
            registerError = "email already registered"
        else:
            cur.execute(
                'INSERT INTO users (email, firstName, lastName, password) VALUES (%s,%s,%s,%s)', 
                (email, firstName, lastName, password)
            )
        return jsonify(registerError)