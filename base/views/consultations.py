from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.serializers.packages import *


@api_view(['POST', 'PUT', 'GET'])
@permission_classes([IsAuthenticated])
def consultation_create_update(request, pk=None):
    if request.method == 'GET':
        if pk:
            consultation = get_object_or_404(Consultation, pk=pk)
            serializer = ConsultationSerializer(consultation)
            return Response(serializer.data)
        
        consultations = Consultation.objects.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            print("validating")
            # Automatically assign the staff member based on the authenticated user
            staff_member = get_object_or_404(StaffMember, user=request.user)
            
            serializer.save(staff_member=staff_member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        consultation = get_object_or_404(Consultation, pk=pk)
        serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)