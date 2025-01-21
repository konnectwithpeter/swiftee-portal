# serializers.py
from rest_framework import serializers
from base.models import *
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = "__all__"


class ConsultationSerializer(serializers.ModelSerializer):
    staff_member_name = serializers.SerializerMethodField()
    class Meta:
        model = Consultation
        fields = "__all__"

    def validate_consultation_date(self, value):
        """
        Validate that consultation date is not in the past
        """
        if value < timezone.now():
            raise serializers.ValidationError("Consultation date cannot be in the past")
        return value
    
    def get_staff_member_name(self, obj):
        """
        Retrieve the full name of the staff member
        """
        if obj.staff_member:
            return f"{obj.staff_member.first_name} {obj.staff_member.last_name}"
        return None


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServicePackageSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = ServicePackage
        fields = [
            "id",
            "service",
            "service_name",
            "name",
            "package_type",
            "price",
            "features",
            "is_active",
        ]


class ServiceWithPackagesSerializer(serializers.ModelSerializer):
    packages = ServicePackageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "description", "base_price", "is_active", "packages"]
