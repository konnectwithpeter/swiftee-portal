from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.conf import settings
from .managers import CustomUserManager
from django.dispatch import receiver
from django.conf import settings
from base.tasks import *


# Create your models here.


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="last login")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class StaffMember(models.Model):
    ROLE_CHOICES = [
        ("consultant", "Immigration Consultant"),
        ("admin", "Administrative Staff"),
        ("manager", "Manager"),
        ("director", "Director"),
    ]

    DEPARTMENT_CHOICES = [
        ("immigration", "Immigration Services"),
        ("legal", "Legal Services"),
        ("operations", "Operations"),
        ("customer_service", "Customer Service"),
        ("marketing", "Marketing"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = _("Staff Member")
        verbose_name_plural = _("Staff Members")


class Consultation(models.Model):
    CONSULTATION_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("no_show", "No Show"),
        ("converted", "Converted to Client"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    consultation_date = models.DateTimeField()
    consultation_type = models.CharField(max_length=200, blank=True, null=True)
    consultation_method = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.SET_NULL,
        null=True,
        related_name="consultations_conducted",
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=CONSULTATION_STATUS_CHOICES, default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-consultation_date"]

    def __str__(self):
        return f"Consultation with {self.first_name} {self.last_name} on {self.consultation_date}"


@receiver(post_save, sender=Consultation)
def send_consultation_email(sender, instance, created, **kwargs):
    if created:
        send_consultation_email_task(instance.email, instance.pk)


class Client(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Client)
def send_welcome_email(sender, instance, created, **kwargs):
    print("Sending welcome email")
    if created:
        user = instance.user
        send_welcome_email_task(user.email, instance.first_name)


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ServicePackage(models.Model):
    PACKAGE_TYPE_CHOICES = [("basic", "Basic"), ("premium", "Premium"), ("vip", "VIP")]

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="packages"
    )
    name = models.CharField(max_length=200)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ClientService(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="services"
    )
    service_package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_notes = models.TextField(blank=True)  # Changed from notes to service_notes

    @property
    def amount_due(self):
        return self.total_amount - self.amount_paid

    class Meta:
        ordering = ("-start_date",)


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("card", "Card Payment"),
    ]
    PAYMENT_STATUS = [
        ("unpaid", "Unpaid"),
        ("partially_paid", "Partially Paid"),
        ("unpaid", "Unpaid"),
    ]
    authorized = models.BooleanField(default=False)
    client_service = models.ForeignKey(
        ClientService, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="unpaid"
    )
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_notes = models.TextField(blank=True)


class ClientDocument(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    file = models.FileField(upload_to="client_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.client}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("rescheduled", "Rescheduled"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="appointments"
    )
    client_service = models.ForeignKey(
        ClientService,
        on_delete=models.CASCADE,
        related_name="appointments",
        null=True,
        blank=True,
    )
    appointment_type = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    appointment_notes = models.TextField(
        blank=True
    )  # Changed from notes to appointment_notes

    class Meta:
        ordering = ["-date_time"]


class Note(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_notes"
    )  # Changed related_name
    client_service = models.ForeignKey(
        ClientService,
        on_delete=models.CASCADE,
        related_name="notes",
        null=True,
        blank=True,
    )  # Changed related_name
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
