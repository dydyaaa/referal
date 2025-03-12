from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.workout_service import Calendar

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/add_workout', methods=['POST'])
@jwt_required()
def add_workout():
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    workout_date = data.get('workout_date')
    notes = data.get('notes')
    workout_type = data.get('workout_type', 'regular workout')

    Calendar.add_workout(user_id, title, workout_date, notes, workout_type)

    return jsonify({'workout': "created"}), 201

@workout_bp.route('/get_all_user_workouts', methods=['GET'])
@jwt_required()
def get_all_user_workouts():

    user_id = get_jwt_identity()

    workouts = Calendar.get_all_user_workouts(user_id)
    return jsonify({'message': f'{workouts}'})

@workout_bp.route('/get_workout/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):

    workout = Calendar.get_workout(workout_id)

    return jsonify({'workout': workout.to_dict()})

@workout_bp.route('/delete_workout/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):

    Calendar.delete_workout(workout_id)

    return jsonify({'workout': 'deleted'})