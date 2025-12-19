import os

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
)

app = Flask(__name__, instance_relative_config=True)

os.makedirs(app.instance_path, exist_ok=True)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Marshmallow schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

#Error handlers
@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    """Return Marshmallow validation errors as JSON."""
    return make_response({"errors": err.messages}, 400)

@app.errorhandler(404)
def not_found(_err):
    """Return a JSON 404 response."""
    return make_response({"error": "Not Found"}, 404)


# Routes
@app.get("/")
def home():
    return make_response({"message": "Workout API is running"}, 200)

# Workouts 
@app.get("/workouts")
def get_workouts():
    """List all workouts."""
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)

@app.get("/workouts/<int:id>")
def get_workout_by_id(id):
    """Show one workout + related exercises with join data."""
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    # Base workout data
    workout_data = workout_schema.dump(workout)

    # Join table data + linked exercise info
    links = WorkoutExercise.query.filter_by(workout_id=id).all()
    exercises_payload = []
    for link in links:
        ex = Exercise.query.get(link.exercise_id)
        exercises_payload.append(
            {
                "id": ex.id if ex else link.exercise_id,
                "name": ex.name if ex else None,
                "category": ex.category if ex else None,
                "equipment_needed": ex.equipment_needed if ex else None,
                "sets": link.sets,
                "reps": link.reps,
                "duration_seconds": link.duration_seconds,
            }
        )

    workout_data["exercises"] = exercises_payload
    return make_response(workout_data, 200)

@app.post("/workouts")
def create_workout():
    """Create a workout from request JSON."""
    data = request.get_json() or {}

    # Marshmallow will validate + convert types 
    valid_data = workout_schema.load(data)

    workout = Workout(
        date=valid_data["date"],
        duration_minutes=valid_data["duration_minutes"],
        notes=valid_data.get("notes"),
    )

    db.session.add(workout)
    db.session.commit()

    return make_response(workout_schema.dump(workout), 201)

@app.delete("/workouts/<int:id>")
def delete_workout(id):
    """Delete a workout and its join records."""
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    # Remove join table rows first
    WorkoutExercise.query.filter_by(workout_id=id).delete()

    db.session.delete(workout)
    db.session.commit()

    return make_response({}, 204)

# Exercises 
@app.get("/exercises")
def get_exercises():
    """List all exercises."""
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)

@app.get("/exercises/<int:id>")
def get_exercise_by_id(id):
    """Show one exercise + related workouts with join data."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error":


"Exercise not found"}, 404)

    exercise_data = exercise_schema.dump(exercise)

    links = WorkoutExercise.query.filter_by(exercise_id=id).all()
    workouts_payload = []
    for link in links:
        w = Workout.query.get(link.workout_id)
        workouts_payload.append(
            {
                "id": w.id if w else link.workout_id,
                "date": w.date.isoformat() if w and w.date else None,
                "duration_minutes": w.duration_minutes if w else None,
                "notes": w.notes if w else None,
                "sets": link.sets,
                "reps": link.reps,
                "duration_seconds": link.duration_seconds,
            }
        )

    exercise_data["workouts"] = workouts_payload
    return make_response(exercise_data, 200)

"/exercises"
@app.post("/exercises")
def create_exercise():
    """Create an exercise from request JSON."""
    data = request.get_json() or {}
    valid_data = exercise_schema.load(data)

    exercise = Exercise(
        name=valid_data["name"],
        category=valid_data["category"],
        equipment_needed=valid_data["equipment_needed"],
    )

    db.session.add(exercise)
    db.session.commit()

    return make_response(exercise_schema.dump(exercise), 201)

@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    """Delete an exercise and its join records."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    WorkoutExercise.query.filter_by(exercise_id=id).delete()

    db.session.delete(exercise)
    db.session.commit()

    return make_response({}, 204)

# Join table: add an exercise to a workout 
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json() or {}
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    valid_data = workout_exercise_schema.load(data)

    link = WorkoutExercise(
        workout_id=valid_data["workout_id"],
        exercise_id=valid_data["exercise_id"],
        sets=valid_data.get("sets"),
        reps=valid_data.get("reps"),
        duration_seconds=valid_data.get("duration_seconds"),
    )

    db.session.add(link)
    db.session.commit()

    return make_response(
        {
            "message": "Exercise added to workout",
            "workout_exercise": workout_exercise_schema.dump(link),
        },
        201,
    )

if __name__ == "__main__":
    app.run(port=5555, debug=True)
