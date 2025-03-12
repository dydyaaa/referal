import logging
from app import db
from flask import current_app
from datetime import datetime
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise


logger = logging.getLogger('app.auth')


class Calendar():
    @staticmethod
    def add_workout(user_id,
                    title,
                    workout_date,
                    notes,
                    workout_type):
        new_workout = Workout(user_id=user_id,
                              title=title,
                              workout_date=workout_date,
                              notes=notes,
                              workout_type=workout_type)
        db.session.add(new_workout)
        db.session.commit()
        logger.info(f'add new workout with params: {title, workout_date, notes, workout_type}')

    @staticmethod
    def get_all_user_workouts(user_id):

        workouts = Workout.query.with_entities(Workout.id, Workout.title).filter_by(user_id=user_id).all()

        return workouts
    
    @staticmethod
    def get_workout(workout_id):

        workout = Workout.query.filter_by(id=workout_id).first()

        return workout
    
    @staticmethod
    def delete_workout(workout_id):

        workout = Workout.query.filter_by(id=workout_id).first()
        db.session.delete(workout)
        db.session.commit()
        