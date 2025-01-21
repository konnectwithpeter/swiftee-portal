# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.serializers.client import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.tasks import *
from django.db import transaction


@api_view(["GET", "POST"])
def client_list(request):
    if request.method == "GET":
        clients = Client.objects.all()
        serializer = ClientProfileSerializer(clients, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        required_fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "nationality",
            "passport_number",
        ]

        # Validate required fields
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {"error": f"Missing required field: {field}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        User = get_user_model()
        email = request.data.get("email")

        try:
            with transaction.atomic():
                # Check if user with email exists
                user = User.objects.filter(email=email).first()

                if not user:
                    # Create new user if doesn't exist
                    user = User.objects.create(email=email)
                else:
                    # Check if user already has a client profile
                    if Client.objects.filter(user=user).exists():
                        return Response(
                            {"error": "Client profile already exists for this email"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # Create client profile
                client = Client.objects.create(
                    user=user,
                    first_name=request.data.get("first_name"),
                    last_name=request.data.get("last_name"),
                    phone_number=request.data.get("phone_number"),
                    nationality=request.data.get("nationality"),
                    passport_number=request.data.get("passport_number"),
                )

                serializer = ClientProfileSerializer(client)
                return Response(
                    {
                        "message": "Client created successfully",
                        "client": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return Response(
                {"error": "Failed to create client", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def client_detail(request, pk):
    client = Client.objects.get(user_id=request.user.id)
    print(client)
    if request.method == "GET":
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:

        serializer = ClientProfileSerializer(
            client, data=request.data, partial=(request.method == "PATCH")
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        client.delete()
        return Response(status=204)


@api_view(["GET"])
def client_full_profile(request, pk):
    client = get_object_or_404(Client, pk=pk)
    serializer = ClientProfileSerializer(client)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def client_documents(request, pk):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=pk)
        documents = ClientDocument.objects.filter(client=client)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        files = request.FILES.values()  # Get all files in the request
        client = get_object_or_404(Client, pk=pk)

        # Check if any files are provided
        if not files:
            return Response(
                {"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        for file in files:
            data = {"file": file, "client": pk}
            serializer = DocumentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(uploaded_by=request.user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


@api_view(["GET", "POST", "PATCH"])
@permission_classes([IsAuthenticated])
def client_appointments(request, pk):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=pk)
        appointments = client.appointments.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        print(request.data)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            client = get_object_or_404(Client, pk=pk)
            serializer.save(client=client)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == "PATCH":
        # Retrieve appointment ID from the request
        appointment_id = request.data.get("id")
        if not appointment_id:
            return Response(
                {"error": "Appointment ID is required for updating."}, status=400
            )

        # Get the specific appointment
        appointment = get_object_or_404(Appointment, id=appointment_id, client__id=pk)

        # Partially update the appointment
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_appointments(request):
    appointments = Appointment.objects.all().order_by("-date_time")
    serializer = AllAppointmentsSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_payments(request, pk):
    client = get_object_or_404(Client, pk=pk)
    payments = Payment.objects.filter(client_service__client=client)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST", "PATCH", "DELETE"])
def client_notes(request, pk):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=pk)
        notes = client.client_notes.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            client = get_object_or_404(Client, pk=pk)
            serializer.save(client=client, created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == "PATCH":
        note_id = request.data.get("editingNoteId")
        if not note_id:
            return Response({"error": "Note ID is required for updating."}, status=400)
        note = get_object_or_404(Note, id=note_id, client__id=pk)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        note_id = request.query_params.get("note_id")
        print(note_id)
        if not note_id:
            return Response(
                {"error": "Note ID is required to delete a note."}, status=400
            )

        note = get_object_or_404(Note, id=note_id)

        if request.user != note.created_by and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to delete this note."}, status=403
            )

        note.delete()
        return Response({"message": "Note deleted successfully."}, status=204)


@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data["name"],
            username=data["email"],
            email=data["email"],
        )
        user.set_password(data["password"])
        user.save()
        client = Client.objects.create(user=user)
        serializer = ClientProfileSerializer(client, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "User with this email already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# class SecureDocumentViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, ClientDocumentPermission]

#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return ClientDocument.objects.all()
#         return ClientDocument.objects.filter(client__user=self.request.user)

#     @action(detail=True, methods=['get'])
#     def secure_download(self, request, pk=None, signature=None):
#         try:
#             # Verify the signature
#             signer = Signer()
#             decoded_signature = urlsafe_base64_decode(signature).decode()
#             doc_id, expires_in = signer.unsign(decoded_signature).split(':')

#             if int(doc_id) != int(pk):
#                 raise Http404("Invalid document")

#             document = self.get_object()

#             if not document.file:
#                 raise Http404("File not found")

#             response = FileResponse(document.file.open('rb'))
#             response['Content-Type'] = 'application/force-download'
#             response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
#             return response

#         except (BadSignature, ValueError, ClientDocument.DoesNotExist):
#             raise Http404("Invalid or expired download link")

#     @action(detail=True, methods=['get'])
#     def get_download_url(self, request, pk=None):
#         document = self.get_object()
#         download_url = generate_temporary_file_url(document)
#         return Response({'download_url': download_url})
