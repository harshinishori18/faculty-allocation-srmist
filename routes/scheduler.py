import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scheduler'))

from flask import Blueprint, jsonify
from schedule_generator import generate_schedule
from analytics.workload import analyze_faculty_workload
from analytics.movement import analyze_faculty_movement
from analytics.scoring import calculate_schedule_score

scheduler_bp = Blueprint('scheduler', __name__)

# Generate and return the full schedule
@scheduler_bp.route('/schedule/generate', methods=['GET'])
def get_schedule():
    schedule = generate_schedule()
    return jsonify({"schedule": schedule})

# Get workload for a specific faculty by name
@scheduler_bp.route('/schedule/workload/<faculty_name>', methods=['GET'])
def get_workload(faculty_name):
    schedule = generate_schedule()
    workload = analyze_faculty_workload(schedule)
    if faculty_name not in workload:
        return jsonify({"error": "Faculty not found in schedule"}), 404
    stats = workload[faculty_name]
    return jsonify({
        "faculty": faculty_name,
        "total_classes": stats["total_classes"],
        "consecutive_classes": stats["consecutive_classes"],
        "idle_gaps": stats["idle_gaps"],
        "workload_score": stats["workload_score"],
        "daily_classes": dict(stats["daily_classes"])
    })

# Get the full schedule analytics
@scheduler_bp.route('/schedule/analytics', methods=['GET'])
def get_analytics():
    schedule = generate_schedule()
    workload = analyze_faculty_workload(schedule)
    movement = analyze_faculty_movement(schedule)
    score = calculate_schedule_score(workload, movement)
    return jsonify({"score": score})