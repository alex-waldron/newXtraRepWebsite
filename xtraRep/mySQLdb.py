import mysql.connector


dbHostName="162.241.224.47"
dbUserName="xtrarepa_admin"
dbDatabase="xtrarepa_workouts"
dbPassword="k$yCbVt;khz*"


def initUserDB():
    sqlFile = open("xtraRep/usersSchema.sql", 'r')
    sqlCommands = sqlFile.read().split(';')
    for command in sqlCommands:
        command = ' '.join(command.split())
        if command == "":
            continue
        try:
            get_cursor().execute(command)
        except:
            print("could not execute command: ", command)

def get_mySQLdb():
    workoutdb = mysql.connector.connect(
        host=dbHostName,
        user=dbUserName,
        database=dbDatabase,
        password=dbPassword
    )
    return workoutdb

def get_cursor():
    db = get_mySQLdb()
    return db.cursor()

def printTables():
    workoutdb = mysql.connector.connect(
        host=dbHostName,
        user=dbUserName,
        database=dbDatabase,
        password=dbPassword
    )
    cur = workoutdb.cursor()
    cur.execute("SHOW TABLES")
    for x in cur:
        print(x)

def removeUserTable():
    get_cursor().execute("DROP TABLE user")


if __name__ == "__main__":
    db = get_mySQLdb()
    cur = db.cursor(dictionary=True)
    cur.execute(
            "SELECT * FROM appUsers"
        )
    print(cur.fetchall())