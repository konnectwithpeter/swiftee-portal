from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_email(subject, recipient_email, context, template_name):
    """
    Sends an HTML email asynchronously.
    """
    html_content = render_to_string(template_name, context)
    text_content = f"Hello {context.get('full_name', '')}, your profile has been successfully created."

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
