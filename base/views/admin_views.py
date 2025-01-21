from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from base.models import JobApplication, Client
from base.serializers.app_serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction
import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from base.models import *
from base.serializers.bio_data_serializer import *
from base.serializers.admin_client_serializer import *
from base.serializers.client import *


@api_view(["GET"])
def client_admin_detail(request, client_id):
    client = Client.objects.get(id=client_id)

    if request.method == "GET":
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_personal_information(request, client_id):
    print(client_id)
    personal_info = PersonalInformation.objects.get(client=3)
    serializer = PersonalInformationSerializer(personal_info)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_contact_details(request, client_id):
    contact_details = get_object_or_404(ContactDetails, client_id=client_id)
    serializer = ContactDetailsSerializer(contact_details)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_education_history(request, client_id):
    education_history = Education.objects.filter(client_id=client_id)
    serializer = EducationSerializer(education_history, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_employment_history(request, client_id):
    employment_history = EmploymentHistory.objects.filter(client_id=client_id)
    serializer = EmploymentHistorySerializer(employment_history, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_qualifications(request, client_id):
    qualifications = get_object_or_404(Qualification, client_id=client_id)
    serializer = QualificationSerializer(qualifications)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def get_documents(request, client_id):
    if request.method == "GET":
        documents = Document.objects.filter(client_id=client_id)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    else:
        data = request.data.copy()
        data["client"] = client_id
        serializer = DocumentSerializer(data=data)
        print(client_id)
        client = Client.objects.get(id=client_id)
        if serializer.is_valid():
            serializer.save(client=client)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST", "UPDATE"])
@permission_classes([IsAdminUser])
def staff_members_view(request):
    if request.method == "GET":
        staff = StaffMember.objects.all()
        serializer = StaffMemberDetailsSerializer(staff, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT"])
@permission_classes([IsAdminUser])
def get_job_applications(request):
    if request.method == "GET":
        applications = JobApplication.objects.all()
        serializer = JobApplicationAdminSerializer(
            applications, many=True
        )  # Add many=True here
        return Response(serializer.data)
    elif request.method == "PUT":
        application_id = request.data.get("application")
        application = get_object_or_404(JobApplication, id=application_id)
        application.step = request.data.get("step")
        application.save()
        serializer = JobApplicationAdminSerializer(application)
        return Response(serializer.data) @ api_view(["GET", "PUT"])


@api_view(["GET", "PUT"])
@permission_classes([IsAdminUser])
def get_all_applications(request):
    if request.method == "GET":
        applications = Application.objects.all()
        serializer = AllApplicationAdminSerializer(applications, many=True)
        return Response(serializer.data)
    elif request.method == "PUT":
        application_id = request.data.get("application")
        application = get_object_or_404(Application, id=application_id)
        application.step = request.data.get("step")
        application.biometric_date = request.data.get("biometric")
        application.save()
        serializer = JobApplicationAdminSerializer(application)
        return Response(serializer.data)
