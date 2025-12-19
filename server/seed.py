from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

def reset_database():
    """Reset database tables for a clean seed run."""
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

def seed_data():
    """Insert sample data into the database."""
    # Create Exercises
    pushups = Exercise(name="Push-Ups", category="Strength", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    bike = Exercise(name="Stationary Bike", category="Cardio", equipment_needed=True)

    db.session.add_all([pushups, running, squats, bike])
    db.session.commit()

    # Create Workouts
    w1 = Workout(date=date(2025, 12, 1), duration_minutes=30, notes="Upper body focus")
    w2 = Workout(date=date(2025, 12, 2), duration_minutes=45, notes="Cardio day")

    db.session.add_all([w1, w2])
    db.session.commit()

    # Join table entries (WorkoutExercise)
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=pushups.id, sets=3, reps=12)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=squats.id, sets=4, reps=10)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=running.id, duration_seconds=1200)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=bike.id, duration_seconds=900)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        reset_database()
        seed_data()
        print("Database seeded successfully!")