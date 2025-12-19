from marshmallow import Schema, fields, validates_schema, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True)
    reps = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates_schema
    def validate_workout_exercise(self, data, **kwargs):
        has_sets_reps = data.get("sets") and data.get("reps")
        has_duration = data.get("duration_seconds")

        if not has_sets_reps and not has_duration:
            raise ValidationError(
                "WorkoutExercise must have either sets & reps or duration_seconds."
            )
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    @validates_schema
    def validate_duration(self, data, **kwargs):
        if data.get("duration_minutes", 0) <= 0:
            raise ValidationError(
                "Workout duration_minutes must be greater than 0."
            )