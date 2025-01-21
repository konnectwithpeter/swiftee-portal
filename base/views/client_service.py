from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from datetime import datetime
from base.models import *
from base.serializers.client import ClientServiceSerializer


@api_view(["GET", "POST"])
def client_services(request, pk):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=pk)
        services = client.services.all()
        serializer = ClientServiceSerializer(services, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        client = get_object_or_404(Client, pk=pk)
        data = request.data

        try:
            with transaction.atomic():
                # 1. Create ClientService
                service_data = {
                    "client": client,
                    "service_package": get_object_or_404(
                        ServicePackage, pk=data.get("service[service_package]")
                    ),
                    "start_date": data.get("service[start_date]"),
                    "end_date": (
                        data.get("service[end_date]")
                        if data.get("service[end_date]")
                        else None
                    ),
                    "status": "pending",
                }

                # Get package price for total_amount
                service_package = service_data["service_package"]
                service_data["total_amount"] = service_package.price
                service_data["amount_paid"] = 0

                client_service = ClientService.objects.create(**service_data)

                # 2. Create Appointment if data exists
                if "appointment[type]" in data:                    
                    appointment_data = {
                        "client": client,
                        "client_service": client_service,
                        "appointment_type": data.get("appointment[type]"),
                        "date_time": datetime.strptime(
                            data.get("appointment[date_time]"), "%Y-%m-%dT%H:%M"
                        ),
                        "status": data.get("appointment[status]"),
                        "appointment_notes": (
                            data.get("appointment[notes]")
                            if data.get("appointment[notes]")
                            else ""
                        ),
                    }

                    Appointment.objects.create(**appointment_data)

                # 3. Create Documents if they exist
               
                index = 0
                while f'documents[{index}][name]' in data or f'documents[{index}]' in data:
                    file_key = f'documents[{index}]'
                    print(file_key)
                    # Get the uploaded file (InMemoryUploadedFile)
                    document_file = data.get(file_key)

                    if document_file:
                        # Create and save the ClientDocument object
                        client_document = ClientDocument.objects.create(
                            client=client,
                            file=document_file,
                            uploaded_by=request.user
                        )
                        client_document.save()

                    # Increment index for the next document
                    index += 1
                    
                

                # 4. Create initial Payment record
                payment_data = {
                    "client_service": client_service,
                    "amount": service_package.price,
                    "payment_method": "pending",  # You might want to adjust this
                    "authorized": False,
                    "payment_notes": "Initial payment record created",
                }
                Payment.objects.create(**payment_data)

                # Return the created service with all related data
                serializer = ClientServiceSerializer(client_service)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
