from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from config.settings import EMAIL_HOST_USER
from datetime import datetime

def opt_verification_email(user_email, user_name, otp):
    html_content = render_to_string('email_templates/otp_verification.html', {
        'user_name': user_name,
        'otp': otp,
        'year': datetime.now().year,
    })

    email = EmailMessage(
        subject='OTP Verification',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[user_email],
    )
    email.content_subtype = 'html'
    email.send()
