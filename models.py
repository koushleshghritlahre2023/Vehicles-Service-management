from database import db
from flask_login import UserMixin

class Customer(UserMixin, db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20))

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
class Appointment(db.Model):

    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)

    service_type = db.Column(db.String(100), nullable=False)

    problem = db.Column(db.Text)

    booking_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(30), default="Pending")

    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Vehicle(db.Model):

    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    vehicle_number = db.Column(db.String(30))

    brand = db.Column(db.String(50))

    model = db.Column(db.String(50))

    fuel = db.Column(db.String(30))

    year = db.Column(db.Integer)

    km = db.Column(db.Integer)

class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(255))