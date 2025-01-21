from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.models import JobApplication, Client
from base.serializers.app_serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction
import logging


@api_view(["GET", "POST", "UPDATE"])
@permission_classes([IsAuthenticated])
def jobs_view(request):
    if request.method == "GET":
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def client_job_application(request, client_id=None, pk=None):
    if request.method == "GET":
        try:
            application_info = JobApplication.objects.get(client_id=client_id)
            serializer = JobApplicationSerializer(application_info)
            return Response(serializer.data)
        except JobApplication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        check = JobApplication.objects.filter(client=client_id).exists()
        client = Client.objects.filter(id=client_id).first()
        if check == False:
            JobApplication.objects.create(client=client, step="registration")
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        application_step = request.data.get("step")
        application_info = JobApplication.objects.get(client_id=client_id)
        if request.data.get("job") != None:
            application_job = request.data.get("job")
            selected_job = Job.objects.filter(id=application_job).first()
            application_info.job = selected_job
        application_info.step = application_step
        application_info.save()
        return Response(status=200)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def application_list(request, client_id):
    if request.method == "GET":
        # Get applications, optionally filtered by client
        client_id = request.query_params.get("client_id", None)
        if client_id:
            applications = Application.objects.filter(client_id=client_id)
        else:
            applications = Application.objects.all()

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data.copy()  # Make the data mutable
        client = Client.objects.get(user=request.user)
        data["client"] = client.id  # Add the client field to the data
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def application_detail(request, client_id, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == "GET":
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data.copy()  # Make the data mutable
        
        # Use the primary key (ID) of the client, not the object
        data["client"] = client_id
        data["step"] = request.data.get("step")  # Include other fields as needed
        data["service"] = request.data.get("service")
        
        serializer = ApplicationSerializer(application, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(["GET", "POST","PUT"])
def client_tickets(request, client_id=None):
    if request.method == "GET":
        if request.user.is_superuser:
            tickets = Ticket.objects.all()  # Fetch all tickets
            serializer = AdminTicketSerializer(tickets, many=True)
            return Response(serializer.data)
        
        # Check if the user is staff
        elif request.user.is_staff:
            # Staff might have limited access (adjust logic as needed)
            tickets = Ticket.objects.filter(assigned_to=request.user)
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)
        else:
            client = Client.objects.filter(id=client_id).first()
            if not client:
                return Response(
                    {"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND
                )
            tickets = client.ticket.all()  # Use the correct related_name from the model
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)

    elif request.method == "POST":
        client = Client.objects.filter(id=client_id).first()
        if not client:
            return Response(
                {"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Bind client to the request data
        data = request.data.copy()  # Make the data mutable
        data["client"] = client_id  # Add the client field to the data

        serializer = TicketSerializer(data=data)
        print("here")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PUT":
        # Ensure the ticket exists
        ticket_id = request.data.get("ticket")
        ticket = Ticket.objects.filter(id=ticket_id).first()

        if not ticket:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_superuser or request.user.is_staff:
            print(request.data)
            # Allowed fields for update
            allowed_fields = ["assigned_to", "resolved"]
            data = {key: request.data[key] for key in allowed_fields if key in request.data}

            if "assigned_to" in data:
                staff_member = StaffMember.objects.filter(id=data["assigned_to"]).first()
                if not staff_member:
                    return Response(
                        {"error": "Assigned staff member not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                data["assigned_to"] = staff_member.id

            serializer = TicketSerializer(ticket, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
def library_list(request):
    documents = Library.objects.all()
    serializer = LibrarySerializer(documents, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def library_upload(request):
    serializer = LibrarySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
