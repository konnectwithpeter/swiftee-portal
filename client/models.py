from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import Client

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


class EmergencyContact(models.Model):
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.institution or "Unknown Institution"


class Employment(models.Model):
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)

    def __str__(self):
        return self.company


class Skill(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Certification(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_expiry_date = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    alternate_phone = models.CharField(max_length=50, blank=True, null=True)
    current_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, related_name='current_address')
    permanent_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, related_name='permanent_address')
    emergency_contact = models.OneToOneField(EmergencyContact, on_delete=models.SET_NULL, null=True)
    education = models.ManyToManyField(Education, blank=True)
    employment = models.ManyToManyField(Employment, blank=True)
    languages = models.ManyToManyField(Skill, blank=True, related_name='languages')
    documents = models.ManyToManyField(Document, blank=True)
    submission_date = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
