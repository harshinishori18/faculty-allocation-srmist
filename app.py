from flask import Flask
from config import db
from routes.registration import registration_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'srmist-secret-key'

db.init_app(app)
app.register_blueprint(registration_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)