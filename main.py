from flask import Flask, request, jsonify, render_template
from config import app, db
from models import Exercise, Progress, DailyCheckIn, User
from datetime import datetime
from datetime import date, time
import sqlite3 
import json
    
@app.route("/get_user", methods=["GET"])
def get_user():
    auth0_id = request.args.get("auth0_id")
    if not auth0_id:
        return jsonify({"error": "Missing auth0_id"}), 400

    user = User.query.filter_by(auth0_id=auth0_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_json()})

@app.route("/register_user", methods=["POST"])
def register_user():
    try:
        data = request.json
        print("Received data:", data)

        auth0_id = data.get("auth0_id")
        email = data.get("email")
        name = data.get("name")
        picture = data.get("picture")

        if not auth0_id or not email:
            return jsonify({"message": "auth0_id and email are required."}), 400

        # Check if the user already exists
        existing_user = User.query.filter_by(auth0_id=auth0_id).first()
        if existing_user:
            # Update existing user info
            existing_user.name = name or existing_user.name
            existing_user.picture = picture or existing_user.picture
        else:
            # Create new user
            new_user = User(
                auth0_id=auth0_id,
                email=email,
                name=name,
                picture=picture,
            )
            db.session.add(new_user)

        # Commit the changes
        db.session.commit()
        return jsonify({"message": "User successfully registered!"}), 201

    except Exception as e:
        db.session.rollback()
        print("Error in register_user:", str(e))  # Debug error
        return jsonify({"message": str(e)}), 500
    
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    json_exercises = list(map(lambda x: x.to_json(), exercises))
    return jsonify({"exercises": json_exercises})

@app.route("/exercisesById", methods=["GET"])
def get_exercises_by_id():
    user_id = request.args.get('userID')  # Get the query parameter
    if not user_id:
        return jsonify({"error": "UserID is required"}), 400

    # Filter exercises by userID
    exercises = Exercise.query.filter_by(userID=user_id).all()
    exercise_list = [exercise.to_dict() for exercise in exercises]  # Convert to JSON serializable
    return jsonify({"exercises": exercise_list})


@app.route("/create_exercise", methods=["POST"])
def create_exercise():
    # Parse data from JSON payload
    name = request.json.get("name")
    date_str = request.json.get("date")
    time_str = request.json.get("time")
    category = request.json.get("category")
    weight = request.json.get("weight")
    reps = request.json.get("reps")
    sets = request.json.get("sets")
    workout_id = request.json.get("workoutID")
    user_id = request.json.get("userID")
    exercise_id = request.json.get("exerciseID")

    # Check for required fields
    if not name or not date_str or not time_str:
        return jsonify({"message": "Name, date and time are required."}), 400

    try:
        # Convert date and time strings to date and time objects
        exercise_date = date.fromisoformat(date_str)
        exercise_time = time.fromisoformat(time_str)
        reps = int(reps) if reps else 1
        sets = int(sets) if sets else 1
        weight = float(weight) if weight else 0

        # Create and add the new exercise
        new_exercise = Exercise(
            name=name,
            date=exercise_date,
            time=exercise_time,
            category=category,
            weight=weight,
            reps=reps,
            sets=sets,
            workoutID=workout_id,
            userID=user_id,
            exerciseID=exercise_id
        )
        
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify({"message": "Exercise Created!"}), 201

    except ValueError as e:
        return jsonify({"message": "Invalid date or time format. Please use ISO format."}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/update_exercise', methods=['PUT'])
def update_exercise():
    data = request.json
    exercise_id = data.get('id')
    if not exercise_id:
        return jsonify({'message': 'Exercise ID is required'}), 400

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({'message': 'Exercise not found'}), 404

    try:
        # Update the fields
        exercise.name = data.get('name', exercise.name)
        exercise.category = data.get('category', exercise.category)
        exercise.date = data.get('date', exercise.date)
        exercise.time = data.get('time', exercise.time)
        exercise.reps = data.get('reps', exercise.reps)
        exercise.sets = data.get('sets', exercise.sets)
        exercise.weight = data.get('weight', exercise.weight)

        db.session.commit()
        return jsonify({'message': 'Exercise Updated!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@app.route("/delete_exercise/<int:wanted_id>", methods=["DELETE"])
def delete_exercise(wanted_id):
    exercise = Exercise.query.get(wanted_id)

    if not exercise:
        return jsonify({"message": "Exercise not found."}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise Deleted!"}), 200

@app.route("/create_checkin", methods=["POST"])
def create_checkin():
    data = request.json
    try:
        # Parse data from the request
        date_str = data.get("date")  # Optional; defaults to today if not provided
        hours_slept = data.get("hours_slept")
        body_weight = data.get("body_weight")
        mood = data.get("mood")
        user_id = data.get("user_id")

        # Ensure user_id and mood are provided
        if not user_id or mood is None:
            return jsonify({"message": "Fields 'user_id' and 'mood' are required."}), 400

        # Convert date string to date object if provided
        checkin_date = date.fromisoformat(date_str) if date_str else date.today()

        # Create and add the new check-in
        new_checkin = DailyCheckIn(
            date=checkin_date,
            hours_slept=hours_slept,
            body_weight=body_weight,
            mood=mood,
            user_id=user_id
        )

        db.session.add(new_checkin)
        db.session.commit()
        return jsonify({"message": "Daily check-in created!"}), 201

    except ValueError as e:
        return jsonify({"message": "Invalid date format. Please use ISO format."}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route("/checkins", methods=["GET"])
def get_checkins():
    checkins = DailyCheckIn.query.all()
    json_checkins = [checkin.to_json() for checkin in checkins]
    return jsonify({"checkins": json_checkins})

@app.route("/create_progress", methods=["POST"])
def create_progress():
    data = request.get_json()
    try:
        # Convert date string to Python date object
        if "date" in data:
            data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()

        # Convert time string to Python time object
        if "time" in data:
            data["time"] = datetime.strptime(data["time"], "%H:%M:%S").time()

        progress_entry = Progress(
            user_id=data["user_id"],
            exercise_id=data["exercise_id"],
            exercise_name=data["exercise_name"],
            date=data["date"],
            time=data["time"],
            weight=data["weight"],
            reps=data["reps"],
            notes=data.get("notes"),
        )
        db.session.add(progress_entry)
        db.session.commit()

        return jsonify({"message": "Progress entry created!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# @app.route("/progress", methods=["GET"])
# def get_progress():
#     user_id = request.args.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Missing user_id"}), 400
    
#     progress_entries = Progress.query.filter_by(user_id=user_id).all()
#     return jsonify([entry.to_json() for entry in progress_entries])

@app.route('/user', methods=['GET'])
def get_user_by_auth0_id():
    auth0_id = request.args.get('auth0_id')
    if not auth0_id:
        return jsonify({"error": "auth0_id is required"}), 400

    user = User.query.filter_by(auth0_id=auth0_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_json())

@app.route('/progress', methods=['GET'])
def get_user_progress():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    progress_entries = Progress.query.filter_by(user_id=user_id).all()
    return jsonify([entry.to_json() for entry in progress_entries])



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

