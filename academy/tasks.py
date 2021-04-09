from celery import shared_task

# from LMS.celery import app
from django.template.loader import render_to_string

from sendgrid import Mail, SendGridAPIClient

from LMS.settings import EMAIL_SENDER, EMAIL_RECEIVER, SENDGRID_KEY

from logger.models import LogRecord


@shared_task
def clear_log():
    LogRecord.objects.all().delete()


@shared_task
def send_email(data):
    context = {
        'name': data['name'],
        'email': data['email'],
        'message': data['message']
    }
    content = render_to_string('Email/contact_us.html', context)
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_RECEIVER,
        subject='Added new comment',
        html_content=content
    )

    sg = SendGridAPIClient(SENDGRID_KEY)
    sg.send(message)
    print("123")