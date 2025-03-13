from datetime import datetime
import logging

logger = logging.getLogger('app.validate')

class WorkoutValidate():
    def add_workout_validate(
        user_id,
        title,
        workout_date,
        notes,
        workout_type):
        
        if not isinstance(title, str):
            logger.error(f'title must be str, got {type(title)}')
            raise TypeError(f'title must be str, got {type(title)}')
        if not isinstance(workout_date, datetime):
            logger.error(f'workout_date must be datetime, got {type(workout_date)}')
            raise TypeError(f'workout_date must be datetime, got {type(workout_date)}')
        if not isinstance(notes, str):
            logger.error(f'notes must be str, got {type(notes)}')
            raise TypeError(f'notes must be str, got {type(notes)}')
        if not isinstance(workout_type, str):
            logger.error(f'workout_type must be str, got {type(workout_type)}')
            raise TypeError(f'workout_type must be str, got {type(workout_type)}')
        
        if not title.strip():
            logger.error('title cannot be empty')
            raise ValueError('title cannot be empty')
        if not workout_type.strip():
            logger.error('workout_type cannot be empty')
            raise ValueError('workout_type cannot be empty')

