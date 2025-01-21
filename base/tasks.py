from background_task import background
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@background(schedule=2)
def send_consultation_email_task(email, consultation_id):
    from base.models import Consultation

    try:
        consultation = Consultation.objects.get(id=consultation_id)

        # Add error handling for when staff_member is None
        if consultation.staff_member:
            staff_name = f"{consultation.staff_member.first_name} {consultation.staff_member.last_name}"
        else:
            staff_name = "Our Immigration Consultant"  # fallback name

        context = {
            "first_name": consultation.first_name,
            "staff_member_name": staff_name,
            "consultation_date": consultation.consultation_date.strftime("%B %d, %Y"),
            "consultation_time": consultation.consultation_date.strftime("%I:%M %p"),
            "company_phone": "+254 712 553 768",
        }

        message = ""
        send_mail(
            "Thank You for Visiting SwiftPass Global",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=render_to_string(
                "base/consultation.html",
                context,
            ),
            fail_silently=False,
        )
    except Consultation.DoesNotExist:
        print(f"Consultation with id {consultation_id} not found")
    except Exception as e:
        print(f"Error sending consultation email: {str(e)}")


background(schedule=2)


def send_welcome_email_task(email, first_name):
    print(email, first_name)
    message = ""
    send_mail(
        "WELCOME TO SWIFTPASS GLOBAL",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=render_to_string(
            "base/welcome.html",
            {"first_name": first_name},
        ),
        fail_silently=False,
    )


@background(schedule=2)
def send_reset_email_task(email, reset_url):
    print(f"Starting reset email task for {email}")
    try:
        message = ""
        send_mail(
            "PASSWORD RESET REQUEST",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=render_to_string(
                "base/reset_password.html",
                {"reset_url": reset_url},
            ),
            fail_silently=False,
        )
        print(f"Reset email sent successfully to {email}")
    except Exception as e:
        print(f"Error sending reset email: {str(e)}")
        raise
