from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def generate_invoice(customer, vehicle, booking):

    filename = f"invoices/invoice_{booking.id}.pdf"

    pdf = SimpleDocTemplate(filename)

    elements = []

    elements.append(Paragraph("<b>Vehicle Service Invoice</b>", styles["Heading1"]))
    elements.append(Paragraph(f"Customer: {customer.name}", styles["Normal"]))
    elements.append(Paragraph(f"Vehicle: {vehicle.vehicle_number}", styles["Normal"]))
    elements.append(Paragraph(f"Service: {booking.service_type}", styles["Normal"]))
    elements.append(Paragraph(f"Status: {booking.status}", styles["Normal"]))

    pdf.build(elements)

    return filename