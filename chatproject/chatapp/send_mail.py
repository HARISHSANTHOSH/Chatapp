import base64
import os

from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail, To

from .exceptions import CustomException


sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
from_mail = os.getenv("FROM_EMAIL")



def mail_engine(message):
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(response)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")
        CustomException(
            detail={
                "result": False,
                "msg": "Error sending email",
            },
            code="Email Error",
        )

def send_subscription_email(user_email, customer_name, plan_name, payment_status):
    """Send email notification for successful subscription or payment."""
    try:
        # Create the email content (you can use HTML templates here)
        subject = "Your Subscription is Confirmed!"
        context = {
            'customer_name': customer_name,
            'plan_name': plan_name,
            'payment_status': payment_status
        }
        # Prepare the SendGrid Mail object
        message = Mail(
            from_email=from_mail,  # Sender's email
            to_emails=user_email,  # Recipient's email
            subject=subject,  # Email subject
            html_content=render_to_string("subscription.html", context),
        )

        mail_engine(message)