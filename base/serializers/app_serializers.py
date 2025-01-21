from rest_framework import serializers
from base.models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ("step",)  # Make step read-only since it has a default

    def validate(self, data):
        # Check if client already has a job application
        client = data.get("client")
        if self.instance is None:  # Only for creation
            existing_application = JobApplication.objects.filter(client=client).exists()
            if existing_application:
                raise serializers.ValidationError(
                    "Client already has an active job application"
                )
        return data


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        
       
class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class StaffMemberDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = "__all__"
        
        
class AdminTicketSerializer(serializers.ModelSerializer):
    client = ClientDetailsSerializer()  # Nested serializer for client details
    assigned_to = StaffMemberDetailsSerializer()  # Nested serializer for staff details

    class Meta:
        model = Ticket
        fields = [
            "id",
            "client",
            "issue",
            "description",
            "priority",
            "assigned_to",
            "resolved",
            "resolved_at",
            "created_at",
            "updated_at",
        ]

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'file', 'description', 'size', 'category', 'created_at', 'updated_at']
        read_only_fields = ['size', 'created_at', 'updated_at']