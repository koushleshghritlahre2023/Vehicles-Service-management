from flask_mail import Mail, Message

mail = Mail()

def send_invoice(app, receiver, invoice_url):

    with app.app_context():

        msg = Message(
            "Vehicle Service Invoice",
            recipients=[receiver]
        )

        msg.body = f"""
Thank you for choosing our service.

Your invoice is available here:

{invoice_url}

Regards,
Vehicle Service Team
"""

        mail.send(msg)