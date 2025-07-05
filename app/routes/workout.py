from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.workout_service import Calendar, WorkOut
from werkzeug.exceptions import Forbidden


workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/add_workout', methods=['POST'])
@jwt_required()
def add_workout():
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    workout_date = data.get('workout_date')
    notes = data.get('notes', '')
    workout_type = data.get('workout_type', 'regular workout')
    
    try:
        Calendar.add_workout(user_id, title, workout_date, notes, workout_type)
    except ValueError as error:
        return jsonify({'error': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    
    return jsonify({'workout': "created"}), 201

@workout_bp.route('/get_all_user_workouts', methods=['GET'])
@jwt_required()
def get_all_user_workouts():

    user_id = get_jwt_identity()
    workouts = Calendar.get_all_user_workouts(user_id)
    
    return jsonify({'workouts': workouts}), 200

@workout_bp.route('/get_future_workouts', methods=['GET'])
@jwt_required()
def get_future_workouts():
    user_id = get_jwt_identity()
    
    try:
        future_workouts = Calendar.get_future_workouts(user_id)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'future_workouts': future_workouts}), 200

@workout_bp.route('/get_workout/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    
    user_id = get_jwt_identity()

    try:
        workout = Calendar.get_workout(user_id, workout_id)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
        
    return jsonify({'workout': workout}), 200

@workout_bp.route('/delete_workout/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    
    user_id = get_jwt_identity()

    try:
        Calendar.delete_workout(user_id, workout_id)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'workout': 'deleted'}), 200

@workout_bp.route('/add_exercise/<int:workout_id>', methods=['POST'])
@jwt_required()
def add_exercise(workout_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    name = data.get('name')
    
    try:
        WorkOut.add_exercise(user_id, workout_id, name)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
    except ValueError:
        return jsonify({'error': 'Workout does not exist'})
    
    return jsonify({'exercise': 'add'})

@workout_bp.route('/add_sets/<int:exercise_id>', methods=['POST'])
@jwt_required()
def add_sets(exercise_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    weight = data.get('weight')
    reps = data.get('reps')
    
    try:
        WorkOut.add_sets(user_id, exercise_id, weight, reps)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
    except ValueError:
        return jsonify({'error': 'Workout does not exist'})
    
    return jsonify({'set': 'add'})