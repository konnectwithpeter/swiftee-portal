# serializers.py
from rest_framework import serializers
from base.models import *
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "email"


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Add email field

    class Meta:
        model = Client
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "nationality",
            "passport_number",
            "id",
        )

    def create(self, validated_data):
        email = validated_data.pop("email")
        try:
            # Create user with a unique email
            user = get_user_model().objects.create_user(
                email=email, password="defaultpass123"
            )

            # Create client profile
            client = Client.objects.create(user=user, **validated_data)
            return client

        except IntegrityError as e:
            # Catch unique constraint violations and return a descriptive error
            if "unique constraint" in str(e).lower():
                raise ValidationError(
                    {"email": "A user with this email already exists."}
                )
            raise ValidationError(
                {"detail": "An error occurred while creating the client."}
            )


class ServicePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePackage
        fields = "__all__"


class PServiceSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = ClientService
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    client_service = PServiceSerializer()

    class Meta:
        model = Payment
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.username", read_only=True
    )

    class Meta:
        model = Note
        fields = ["id", "content", "created_at", "updated_at", "created_by_name"]


class ClientServiceSerializer(serializers.ModelSerializer):
    service_package_details = ServicePackageSerializer(
        source="service_package", read_only=True
    )
    payments = PaymentSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = ClientService
        fields = "__all__"


class ClientProfileSerializer(serializers.ModelSerializer):
    services = ClientServiceSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    client_notes = NoteSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Client
        fields = "__all__"

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ClientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = "__all__"


class AllAppointmentsSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # Include detailed client info
    client_service = ClientServiceSerializer(
        read_only=True
    )  # Include detailed client service info

    class Meta:
        model = Appointment
        fields = "__all__"
