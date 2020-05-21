from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import timezone


@task()
def send_email_notifications():
    email_subject = "Notification"
    message = render_to_string("notifications_mail_template.html", {})
    to_email = set(
        user.email for user in User.objects.all() if (timezone.now() - user.last_login).days > 0
    )
    send_mail(email_subject, message, "fiszkly@gmail.com", to_email, fail_silently=False)
