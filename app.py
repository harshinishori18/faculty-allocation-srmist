from flask import Flask, render_template, session
from config import db
from routes.registration import registration_bp
from routes.scheduler import scheduler_bp
from routes.fa import fa_bp
from models.fa_entry import FAEntry
from scheduler.schedule_generator import generate_schedule
from scheduler.export_schedule import (
    build_matrix_timetable
)

from scheduler.analytics.workload import (
    analyze_faculty_workload
)
from scheduler.sample_data import time_slots

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'srmist-secret-key'

db.init_app(app)
app.register_blueprint(registration_bp)
app.register_blueprint(scheduler_bp)
app.register_blueprint(fa_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    faculty_name = session.get('faculty_name', '')
    return render_template('dashboard.html', faculty_name=faculty_name)

@app.route('/fa-list')
def fa_list_page():
    return render_template('fa_list.html')

@app.route('/allocation-sheet')
def allocation_sheet_page():
    return render_template('allocation_sheet.html')

@app.route('/timetable')
def timetable():

    schedule = generate_schedule()

    matrix_timetable = build_matrix_timetable(
        schedule
    )

    workload_data = analyze_faculty_workload(
        schedule
    )

    print("\nTIMETABLE KEYS")
    print(matrix_timetable.keys())

    print("\nWORKLOAD DATA")
    print(workload_data)

    return render_template(

        'timetable.html',

        timetable=matrix_timetable,

        workload=workload_data,

        time_slots=time_slots

    )


if __name__ == '__main__':
    app.run(debug=True)