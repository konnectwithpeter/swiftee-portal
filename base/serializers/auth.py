from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ModelSerializer

from base.models import *


class RegisterUserSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
       # extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        email = attrs.get('email', None)
        username = attrs.get('username', None)

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username must be alphanumeric')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ResetPasswordEmailRequestSerializer(ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):

        email = attrs['data'].get('email', "")

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
    
    

class StaffSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ['username','is_staff']
























class ClientSerializer(serializers.ModelSerializer):
    amount_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ServicePackageSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = ServicePackage
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Note
        fields = '__all__'

class ClientServiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    amount_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ClientService
        fields = '__all__'

class ClientDetailSerializer(serializers.ModelSerializer):
    services = ClientServiceSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'