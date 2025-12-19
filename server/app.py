import os

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__, instance_relative_config=True)

os.makedirs(app.instance_path, exist_ok=True)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.get("/")
def home():
    return make_response({"message": "Workout API is running"}, 200)


@app.get("/workouts")
def get_workouts():
    return make_response({"message": "GET /workouts"}, 501)


@app.get("/workouts/<int:id>")
def get_workout_by_id(id):
    """Show one workout + related exercises (placeholder)."""
    return make_response({"message": f"GET /workouts/{id})"}, 501)


"/workouts"
def create_workout():
    """Create a workout (placeholder)."""
    return make_response({"message": "POST /workouts"}, 501)


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    """Delete a workout (placeholder)."""
    return make_response({"message": f"DELETE /workouts/{id}"}, 501)


@app.get("/exercises")
def get_exercises():
    """List all exercises (placeholder)."""
    return make_response({"message": "GET /exercises"}, 501)


@app.get("/exercises/<int:id>")
def get_exercise_by_id(id):
    """Show one exercise + related workouts (placeholder)."""
    return make_response({"message": f"GET /exercises/{id}"}, 501)


"/exercises"
def create_exercise():
    """Create an exercise (placeholder)."""
    return make_response({"message": "POST /exercises"}, 501)


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    """Delete an exercise (placeholder)."""
    return make_response({"message": f"DELETE /exercises/{id}"}, 501)


"/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises"
def add_exercise_to_workout(workout_id, exercise_id):
    """
    Add an exercise to a workout with reps/sets/duration (placeholder).
    """
    return make_response(
        {
            "message": (
                "POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises "
            )
        },
        501,
    )

if __name__ == "__main__":
    app.run(port=5555, debug=True)
