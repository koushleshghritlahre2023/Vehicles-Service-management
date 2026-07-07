from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, login_required, current_user

from app import app
from database import db
from models import Customer
from models import Vehicle, Appointment,Admin
from flask import session


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        user = Customer.query.filter_by(email=email).first()

        if user:
            flash("Email already exists")
            return redirect("/register")

        hashed = generate_password_hash(password)

        new_user = Customer(
            name=name,
            email=email,
            phone=phone,
            password=hashed
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = Customer.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect("/dashboard")

        flash("Invalid Credentials")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        user=current_user
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")
from models import Vehicle
@app.route("/add_vehicle", methods=["GET", "POST"])
@login_required
def add_vehicle():

    if request.method == "POST":

        vehicle = Vehicle(
            customer_id=current_user.id,
            vehicle_number=request.form["vehicle_number"],
            brand=request.form["brand"],
            model=request.form["model"],
            fuel=request.form["fuel"],
            year=request.form["year"],
            km=request.form["km"]
        )

        db.session.add(vehicle)
        db.session.commit()

        return redirect("/my_vehicles")

    return render_template("add_vehicle.html")
@app.route("/my_vehicles")
@login_required
def my_vehicles():

    vehicles = Vehicle.query.filter_by(
        customer_id=current_user.id
    ).all()

    return render_template(
        "my_vehicles.html",
        vehicles=vehicles
    )
@app.route("/delete_vehicle/<int:id>")
@login_required
def delete_vehicle(id):

    vehicle = Vehicle.query.get_or_404(id)

    if vehicle.customer_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(vehicle)
    db.session.commit()

    return redirect("/my_vehicles")

@app.route("/book_service", methods=["GET", "POST"])
@login_required
def book_service():

    vehicles = Vehicle.query.filter_by(customer_id=current_user.id).all()

    if request.method == "POST":

        booking = Appointment(

            customer_id=current_user.id,

            vehicle_id=request.form["vehicle"],

            service_type=request.form["service"],

            problem=request.form["problem"],

            booking_date=request.form["date"]

        )

        db.session.add(booking)
        db.session.commit()

        return redirect("/my_bookings")

    return render_template(
        "book_service.html",
        vehicles=vehicles
    )

@app.route("/my_bookings")
@login_required
def my_bookings():

    bookings = Appointment.query.filter_by(
        customer_id=current_user.id
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )

@app.route("/admin", methods=["GET","POST"])
def admin_login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        admin=Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session["admin"]=admin.id

            return redirect("/admin/dashboard")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    total_customers = Customer.query.count()

    total_vehicles = Vehicle.query.count()

    total_bookings = Appointment.query.count()

    pending = Appointment.query.filter_by(
        status="Pending"
    ).count()

    return render_template(
        "admin_dashboard.html",
        customers=total_customers,
        vehicles=total_vehicles,
        bookings=total_bookings,
        pending=pending
    )

@app.route("/admin/bookings")
def admin_bookings():

    if "admin" not in session:
        return redirect("/admin")

    bookings = Appointment.query.all()

    return render_template(
        "admin_bookings.html",
        bookings=bookings
    )

@app.route("/approve/<int:id>")
def approve(id):

    booking = Appointment.query.get_or_404(id)

    booking.status = "Approved"

    db.session.commit()

    return redirect("/admin/bookings")

@app.route("/complete/<int:id>")
def complete(id):

    booking = Appointment.query.get_or_404(id)

    booking.status = "Completed"

    db.session.commit()

    return redirect("/admin/bookings")