from flask import Flask, render_template, session
from config import db
from routes.registration import registration_bp
from routes.scheduler import scheduler_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'srmist-secret-key'

db.init_app(app)
app.register_blueprint(registration_bp)
app.register_blueprint(scheduler_bp)

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

if __name__ == '__main__':
    app.run(debug=True)