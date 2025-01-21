from rest_framework import serializers
from base.models import (
    PersonalInformation,
    ContactDetails,
    Education,
    EmploymentHistory,Qualification,Client,Document
)


class PersonalInformationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    middleName = serializers.CharField(
        source="middle_name", required=False, allow_blank=True
    )
    dateOfBirth = serializers.DateField(source="date_of_birth")
    passportNumber = serializers.CharField(source="passport_number")
    passportExpiryDate = serializers.DateField(
        source="passport_expiry_date", required=False
    )
    maritalStatus = serializers.CharField(source="marital_status")
    documentType = serializers.CharField(source="document_type")

    class Meta:
        model = PersonalInformation
        fields = [
            "id",
            "firstName",
            "middleName",
            "lastName",
            "dateOfBirth",
            "gender",
            "nationality",
            "documentType",
            "passportNumber",
            "passportExpiryDate",
            "maritalStatus",
        ]

    def validate(self, data):
        if data.get("document_type") == "passport" and not data.get(
            "passport_expiry_date"
        ):
            raise serializers.ValidationError(
                {
                    "passportExpiryDate": "Passport expiry date is required for passport documents"
                }
            )
        return data


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = [
            "email",
            "phone",
            "alternate_phone",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "emergency_contact_name",
            "emergency_contact_relationship",
            "emergency_contact_phone",
        ]

    def validate_phone(self, value):
        """
        Check that the phone number is valid
        """
        if not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise serializers.ValidationError(
                "Phone number can only contain digits, +, -, and spaces"
            )
        return value

    def validate_emergency_contact_phone(self, value):
        """
        Check that the emergency contact phone number is valid
        """
        if not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise serializers.ValidationError(
                "Phone number can only contain digits, +, -, and spaces"
            )
        return value


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "grade",
            "country",
        ]

    def validate(self, data):
        """
        Check that start date is before end date
        """
        if data.get("end_date") and data.get("start_date") > data.get("end_date"):
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date"}
            )
        return data


class EmploymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentHistory
        fields = [
            "id",
            "company_name",
            "job_title",
            "location",
            "employment_type",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "industry",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        """
        Custom validation for employment history entries.
        """
        if data.get("is_current") and data.get("end_date"):
            raise serializers.ValidationError(
                {"end_date": "Current employment cannot have an end date."}
            )

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        return data
    
    
class QualificationSerializer(serializers.ModelSerializer):
    languages = serializers.JSONField(default=list)
    technical_skills = serializers.CharField(allow_blank=True)
    certifications = serializers.CharField(allow_blank=True)

    class Meta:
        model = Qualification
        fields = ['id', 'languages', 'technical_skills', 'certifications']
        
        
class DocumentSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'document_type', 'name', 'file', 'document_name',
            'uploaded_at', 'updated_at', 'document_url'
        ]
        read_only_fields = ['uploaded_at', 'updated_at']

    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None



   

