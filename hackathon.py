from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
admin = Admin(app, name='pingins', template_mode='bootstrap3')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.TEXT)
    balance = db.Column(db.REAL)
    parking = db.Column(db.BOOLEAN)
    checkin = db.Column(db.BOOLEAN)
    security = db.Column(db.BOOLEAN)
    shopping = db.Column(db.BOOLEAN)
    departure = db.Column(db.BOOLEAN)

db.create_all()

admin.add_view(ModelView(User, db.session))
api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == "__main__":
    app.run()