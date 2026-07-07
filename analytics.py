import matplotlib.pyplot as plt
from models import Appointment

def generate_booking_chart():
    pending = Appointment.query.filter_by(status="Pending").count()
    approved = Appointment.query.filter_by(status="Approved").count()
    completed = Appointment.query.filter_by(status="Completed").count()

    labels = ["Pending", "Approved", "Completed"]
    values = [pending, approved, completed]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.title("Service Booking Status")
    plt.savefig("static/images/chart.png")
    plt.close()