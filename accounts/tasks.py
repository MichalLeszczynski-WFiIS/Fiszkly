import os
import fiszkly
from celery import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sites.models import Site


@task()
def send_email_notifications():
    email_subject = "Notification"
    site_domain = Site.objects.get_current().domain
    for user in User.objects.all():
        message = render_to_string(
            "notifications_mail_template.html", {"user": user, "domain": "fiszkly.pl"}
        )
        if (timezone.now() - user.last_login).days > 0 and os.environ.get("SENDGRID_API_KEY"):
            send_mail(
                email_subject, message, "fiszkly@gmail.com", [user.email], fail_silently=False,
            )
        else:
            return message
