from django.db import models
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator


class Job(models.Model):
    employer = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    country = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    processing = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class JobApplication(models.Model):
    JOB_APPLICATION_STEP = [
        ("registration", "Registration"),
        ("documents", "Documents"),
        ("payment", "Payments"),
        ("medical", "Medical"),
        ("review", "Review"),
        ("matching", "Job Matching"),
        ("agreement", "Agreement"),
        ("completed", "Completed"),
    ]
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="job_application"
    )
    step = models.CharField(max_length=100, choices=JOB_APPLICATION_STEP)
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="job", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =  ['-created_at']


class Application(models.Model):
    APPLICATION_STEP = [
        ("service", "Service Selection"),
        ("registration", "Registration"),
        ("payment", "Payments"),
        ("documents", "Documents"),
        ("completed", "Completed"),
    ]
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="application"
    )
    step = models.CharField(
        max_length=200,
        choices=APPLICATION_STEP,
        default="service",
    )
    service = models.ForeignKey("ClientService",on_delete=models.CASCADE,null=True,blank=True)
    visa = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    travel_date = models.DateField(null=True, blank=True)
    biometric_date = models.DateTimeField(null=True, blank=True)
    sponsored = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =  ['-created_at']


class Ticket(models.Model):
    priority = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="ticket"
    )
    issue = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=200, choices=priority)
    assigned_to = models.ForeignKey(
        "StaffMember", on_delete=models.SET_NULL, blank=True, null=True
    )
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set resolved_at timestamp when resolved is set to True
        if self.resolved and not self.resolved_at:
            self.resolved_at = now()
        elif not self.resolved:
            # Clear resolved_at if resolved is set back to False
            self.resolved_at = None
        super().save(*args, **kwargs)
        
    class Meta:
        ordering =  ['-created_at']


class Library(models.Model):
    CATEGORY_CHOICES = [
        ("HR", "HR"),
        ("IT", "IT"),
        ("FINANCE", "Finance"),
    ]

    file = models.FileField(
        upload_to="library/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    description = models.TextField()
    size = models.IntegerField(editable=False)  # Size in bytes
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)
