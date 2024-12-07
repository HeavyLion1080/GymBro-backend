from config import db
from datetime import date
from datetime import datetime

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    time = db.Column(db.Time, unique=False, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    weight = db.Column(db.Float, nullable=True, default=0)
    reps = db.Column(db.Integer, unique=False, nullable=True, default=1)
    sets = db.Column(db.Integer, unique=False, nullable=True, default=1)
    workoutID = db.Column(db.Integer, unique=False, nullable=False, default=1)
    userID = db.Column(db.Integer, unique=False, nullable=False, default=1)
    exerciseID = db.Column(db.Integer, unique=False, nullable=False, default=0)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "category": self.category,
            "weight": self.weight,
            "reps": self.reps,
            "sets": self.sets,
            "workout_id": self.workoutID,
            "user_id": self.userID,
            "exercise_id": self.exerciseID,
        }

class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Add user_id column
    exercise_id = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255), nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,  # Include user_id in the JSON response
            "exercise_id": self.exercise_id,
            "exercise_name": self.exercise_name,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "weight": self.weight,
            "reps": self.reps,
            "notes": self.notes,
        }

class DailyCheckIn(db.Model):
    __tablename__ = "daily_checkins"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    hours_slept = db.Column(db.Float, nullable=True)
    body_weight = db.Column(db.Float, nullable=True)
    mood = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "hours_slept": self.hours_slept,
            "body_weight": self.body_weight,
            "mood": self.mood,
            "user_id": self.user_id,
        }
        
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_json(self):
        return {
        "id": self.id,
        "auth0_id": self.auth0_id,
        "email": self.email,
        "name": self.name,
        "picture": self.picture,
        "created_at": self.created_at.isoformat() if self.created_at else None,
    }

