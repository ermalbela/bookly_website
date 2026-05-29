from celery import Celery
from .mail import create_message, mail
from asgiref.sync import async_to_sync #converts async code to sync code

c_app = Celery() ##doesnt support async code

c_app.config_from_object('src.config')


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(
        recipients=recipients, subject=subject, body=body
    )

    async_to_sync(mail.send_message)(message)
    print("Email Sent")