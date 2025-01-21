from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from base.models import PersonalInformation, Client
from base.serializers.bio_data_serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def personal_information_view(request, client_id=None):
    if request.method == "GET":
        try:
            personal_info = PersonalInformation.objects.get(client_id=client_id)
            serializer = PersonalInformationSerializer(personal_info)
            return Response(serializer.data)
        except PersonalInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "POST":
        # Check if a record already exists for this client
        try:
            existing_record = PersonalInformation.objects.get(client_id=client_id)
            # If record exists, update it instead
            serializer = PersonalInformationSerializer(
                existing_record, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PersonalInformation.DoesNotExist:
            # If no record exists, create a new one
            serializer = PersonalInformationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client_id=client_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            personal_info = PersonalInformation.objects.get(client_id=client_id)
            serializer = PersonalInformationSerializer(personal_info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PersonalInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def contact_details_view(request, client_id=None):
    """
    Handle GET, POST and PUT requests for ContactDetails
    GET: Retrieve contact details for the authenticated user
    POST: Create new contact details for the authenticated user
    PUT: Update existing contact details for the authenticated user
    """
    if request.method == "GET":
        try:
            contact_details = ContactDetails.objects.get(client_id=client_id)
            serializer = ContactDetailsSerializer(contact_details)
            return Response(serializer.data)
        except ContactDetails.DoesNotExist:
            return Response(
                {"detail": "Contact details not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    elif request.method == "POST":
        # Check if contact details already exist
        if ContactDetails.objects.filter(client_id=client_id).exists():
            return Response(
                {"detail": "Contact details already exist. Use PUT to update."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ContactDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            contact_details = ContactDetails.objects.get(client_id=client_id)
            serializer = ContactDetailsSerializer(
                contact_details, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ContactDetails.DoesNotExist:
            return Response(
                {"detail": "Contact details not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def education_list(request, client_id=None, pk=None):
    """
    List all educations, create, update or delete an education entry
    """
    if request.method == "GET":
        educations = Education.objects.filter(client=client_id)
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            education = Education.objects.get(id=pk, client=client_id)
        except Education.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            education = Education.objects.get(id=pk, client=client_id)
        except Education.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def employment_list(request, client_id=None, pk=None):
    """
    List all employments, create, update or delete an emplyment entry
    """
    if request.method == "GET":
        employments = EmploymentHistory.objects.filter(client=client_id)
        serializer = EmploymentHistorySerializer(employments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EmploymentHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            employment = EmploymentHistory.objects.get(id=pk, client=client_id)
        except EmploymentHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EmploymentHistorySerializer(employment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            employment = EmploymentHistory.objects.get(id=pk, client=client_id)
        except EmploymentHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        employment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def qualification_detail(request, client_id=None):
    """
    Get, create, update or delete qualifications for the authenticated user.
    """
    if request.method == "GET":
        try:
            qualification_details = Qualification.objects.get(client_id=client_id)
            serializer = QualificationSerializer(qualification_details)
            return Response(serializer.data)
        except Qualification.DoesNotExist:
            return Response(
                {"detail": "Qualification details not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    elif request.method == "POST":
        # Check if Qualification details already exist
        if Qualification.objects.filter(client_id=client_id).exists():
            return Response(
                {"detail": "Qualification details already exist. Use PUT to update."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from collections import defaultdict
        import re

        # Parse `languages` from the nested QueryDict
        languages = []
        language_data = defaultdict(dict)
        for key, value in request.data.items():
            if key.startswith("languages"):
                # Extract index and field name from the key
                match = re.match(r"languages\[(\d+)\]\[(\w+)\]", key)
                if match:
                    index, field = match.groups()
                    language_data[int(index)][field] = value

        # Convert parsed language data to a list of dictionaries
        for index in sorted(language_data.keys()):
            languages.append(language_data[index])

        # Include parsed `languages` in request data
        data = request.data.dict()
        data["languages"] = languages

        serializer = QualificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            qualification = Qualification.objects.get(client_id=client_id)
        except Qualification.DoesNotExist:
            return Response(
                {"detail": "Qualification details not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        from collections import defaultdict
        import re

        # Parse `languages` from the nested QueryDict
        languages = []
        language_data = defaultdict(dict)
        for key, value in request.data.items():
            if key.startswith("languages"):
                # Extract index and field name from the key
                match = re.match(r"languages\[(\d+)\]\[(\w+)\]", key)
                if match:
                    index, field = match.groups()
                    language_data[int(index)][field] = value

        # Convert parsed language data to a list of dictionaries
        for index in sorted(language_data.keys()):
            languages.append(language_data[index])

        # Include parsed `languages` in request data
        data = request.data.dict()
        data["languages"] = languages

        serializer = QualificationSerializer(qualification, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def client_documents(request, client_id=None, pk=None):
    if request.method == "GET":
        client = get_object_or_404(Client, id=pk)
        documents = Document.objects.filter(client=client)

        serializer = DocumentSerializer(
            documents, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        """
        Upload documents for a specific client.
        Handles both required documents and additional documents with metadata.
        Will replace any existing documents with new ones.
        """
        client = get_object_or_404(Client, id=client_id)
        uploaded_documents = []

        try:
            with transaction.atomic():
                # Handle required documents
                required_documents = {
                    "photo": "photo",
                    "passport": "passport",
                    "national_id": "national_id",
                    "tax_certificate": "tax_certificate",
                    "financial_statement": "financial_statement",
                    "resume": "resume",
                    "transcripts": "transcripts",
                    "medical": "medical",
                    "clearance": "clearance",
                    "payment": "payment",
                    "agreement": "agreement",
                    "mpesa": "mpesa",
                    "dependents": "dependents",
                    "marriage": "marriage",
                    "divorce": "divorce",
                    "employment": "employment",
                    "payslip": "payslip",
                    "sponsor": "sponsor",
                    "supporting": "supporting",
                }

                # Process required documents
                for frontend_type, model_type in required_documents.items():
                    file_key = f"document[{frontend_type}]"

                    logger.debug(
                        f"Processing document type: {frontend_type} -> {model_type}"
                    )

                    if file_key in request.FILES:
                        try:
                            # Find and delete existing document
                            existing_doc = Document.objects.filter(
                                client=client, document_type=model_type
                            ).first()

                            if existing_doc:
                                logger.debug(
                                    f"Deleting existing document {existing_doc.id} for {model_type}"
                                )
                                existing_doc.file.delete()  # Delete the physical file
                                existing_doc.delete()  # Delete the database record

                            # Create new document
                            logger.debug(f"Creating new document for {model_type}")
                            doc = Document.objects.create(
                                client=client,
                                document_type=model_type,
                                name=request.FILES[file_key].name,
                                file=request.FILES[file_key],
                                document_name=model_type.replace("_", " ").title(),
                            )
                            uploaded_documents.append(doc)
                            logger.debug(f"Successfully created document: {doc.id}")
                        except Exception as e:
                            logger.error(
                                f"Error processing required document {model_type}: {str(e)}"
                            )
                            raise

                # Handle additional documents
                additional_metadata = {}

                # Extract metadata
                for key, value in request.data.items():
                    if key.startswith("additional["):
                        parts = key.strip("]").split("[")
                        if len(parts) == 3:
                            index = parts[1]
                            field = parts[2]
                            additional_metadata.setdefault(index, {})[field] = value

                # Process additional documents
                for index, metadata in additional_metadata.items():
                    doc_id = metadata.get("id")
                    file_key = f"document[{doc_id}]"

                    if file_key in request.FILES:
                        try:
                            # Generate a unique document type for additional documents
                            unique_doc_type = f"additional_{doc_id}"

                            # Find and delete existing document with the same unique_doc_type
                            existing_doc = Document.objects.filter(
                                client=client, document_type=unique_doc_type
                            ).first()

                            if existing_doc:
                                logger.debug(
                                    f"Deleting existing additional document {existing_doc.id}"
                                )
                                existing_doc.file.delete()  # Delete the physical file
                                existing_doc.delete()  # Delete the database record

                            logger.debug(
                                f"Creating additional document: {doc_id} with type {unique_doc_type}"
                            )
                            document = Document.objects.create(
                                client=client,
                                document_type=unique_doc_type,
                                name=request.FILES[file_key].name,
                                document_name=metadata.get("name", ""),
                                file=request.FILES[file_key],
                                description=metadata.get("description", ""),
                                accepted_formats=metadata.get("acceptedFormats", ""),
                            )
                            uploaded_documents.append(document)
                            logger.debug(
                                f"Successfully created additional document: {document.id}"
                            )
                        except Exception as e:
                            logger.error(
                                f"Error processing additional document {doc_id}: {str(e)}"
                            )
                            raise

            # Serialize and return the response
            serializer = DocumentSerializer(
                uploaded_documents, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error uploading documents: {str(e)}")
            logger.error(f"Current uploaded_documents count: {len(uploaded_documents)}")

            # Cleanup uploaded files
            for doc in uploaded_documents:
                try:
                    doc.file.delete()
                    doc.delete()
                except Exception as cleanup_error:
                    logger.error(f"Error during cleanup: {str(cleanup_error)}")

            return Response(
                {"error": f"Failed to upload documents: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_client_document(request, client_id, document_id):
    """Delete a specific document"""
    client = get_object_or_404(Client, id=client_id)
    document = get_object_or_404(Document, id=document_id, client=client)

    try:
        # Delete the file from storage
        document.file.delete()
        # Delete the document record
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
