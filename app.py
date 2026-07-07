from flask import Flask
from config import Config
from database import db
from flask_login import LoginManager
from models import Customer, Vehicle, Appointment, Admin


from models import Customer

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

with app.app_context():
    db.create_all()

from routes import *

if __name__ == "__main__":
    app.run(debug=True)