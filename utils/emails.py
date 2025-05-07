from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_email_task(subject, message, recipient_list, from_email=None):
    """
    General email task that can be used for various purposes (verification, ads, etc.)
    """
    send_mail(
        subject,
        message,
        from_email or settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

@shared_task
def send_verification_email(user_id, domain, subject="Verify your email address"):
    from django.contrib.auth.models import User

    user = User.objects.get(id=user_id)

    message = render_to_string(
        "emails/verification_email.html",
        {"user": user, "domain": domain}
    )

    send_mail(
        subject,
        '',  # plain text empty
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message  # ✅ Send HTML message properly
    )
    
@shared_task
def send_ad_email(user_id, subject, message, domain):
    """
    Send promotional emails (ads) to the user.
    """
    from django.contrib.auth.models import User

    user = User.objects.get(id=user_id)

    message = render_to_string(
        "emails/advertisement_email.html",
        {"user": user, "subject": subject, "message": message, "domain": domain}
    )

    send_email_task.delay(subject, message, [user.email])  # Send ad email
