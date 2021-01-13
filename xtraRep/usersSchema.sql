DROP TABLE IF EXISTS workouts;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  password TEXT NOT NULL,
  dateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  profilePicLoc TEXT
);
CREATE TABLE workouts (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  workoutPlanId INTEGER NOT NULL,
  dayForWorkout INTEGER NOT NULL,
  workoutName TEXT,
  workoutDescription TEXT,
  musclesWorked TEXT,
  dateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  mediaLoc TEXT
);
CREATE TABLE exercises (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  workout_id INTEGER NOT NULL,
  exerciseName TEXT,
  numOfSets INT,
  reps TEXT,
  restTimeBetweenSets INTEGER,
  mediaLoc TEXT,
  notes TEXT,
  dateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE workoutPlans (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  workoutPlanName TEXT,
  workoutPlanDescription TEXT,
  programLength INTEGER,
  programDifficulty TEXT,
  mediaLoc TEXT,
  dateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)