from django.db import models


class PersonalInformation(models.Model):
    DOCUMENT_CHOICES = [
        ("passport", "Passport"),
        ("id", "ID Card"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="personal_information"
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    document_type = models.CharField(
        max_length=10, choices=DOCUMENT_CHOICES, default="passport"
    )
    passport_number = models.CharField(
        max_length=50
    )  # Used for both passport and ID numbers
    passport_expiry_date = models.DateField(
        null=True, blank=True
    )  # Optional for ID type
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ContactDetails(models.Model):
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="contatc_details"
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_relationship = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Contact Details"


class Education(models.Model):
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="education_history"
    )
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name_plural = "Education History"

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"


class EmploymentHistory(models.Model):
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="employment_history"
    )
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ("FULL_TIME", "Full Time"),
            ("PART_TIME", "Part Time"),
            ("CONTRACT", "Contract"),
            ("INTERNSHIP", "Internship"),
            ("FREELANCE", "Freelance"),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-end_date"]
        verbose_name_plural = "Employment histories"


class Qualification(models.Model):
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="qualifications"
    )
    languages = models.JSONField(default=list)  # Stores array of language objects
    technical_skills = models.TextField(blank=True)  # Stores comma-separated skills
    certifications = models.TextField(
        blank=True
    )  # Stores comma-separated certifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("photo", "Passport Size Photo"),
        ("passport", "Passport Page Containing Biodata"),
        ("national_id", "National ID"),
        ("tax_certificate", "Tax Certificate"),
        ("financial_statement", "Financial Statement"),
        ("transcripts", "Transcripts"),
        ("resume", "Resume"),
        ("clearance", "Criminal Clearance"),
        ("medical", "Medical"),
        ("payment", "payment"),
        ("agreement", "agreement"),
        ("mpesa", "mpesa"),
        ("dependents", "dependents"),
        ("marriage", "marriage"),
        ("divorce", "divorce"),
        ("employment", "employment"),
        ("payslip", "payslip"),
        ("sponsor", "sponsor"),
        ("supporting", "supporting"),
        ("additional", "Additional Document"),
    ]

    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    custom_document_type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="client_documents/%Y/%m/%d/")
    document_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # For additional documents
    description = models.CharField(max_length=255, blank=True, null=True)
    accepted_formats = models.CharField(max_length=255, blank=True, null=True)
    admin_upload = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-uploaded_at"]
