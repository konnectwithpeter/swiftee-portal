from rest_framework import serializers
from base.models import *


class ClientMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class JobMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobApplicationAdminSerializer(serializers.ModelSerializer):
    client = ClientMinimalSerializer(read_only=True)
    job = JobMinimalSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ["id", "client", "step", "job", "created_at", "updated_at"]

class ClientSimpleService(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = "__all__"

class AllApplicationAdminSerializer(serializers.ModelSerializer):
    client = ClientMinimalSerializer(read_only=True)
    class Meta:
        model = Application
        fields = "__all__"
