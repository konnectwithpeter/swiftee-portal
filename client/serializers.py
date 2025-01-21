from rest_framework import serializers
from client.models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    current_address = AddressSerializer()
    permanent_address = AddressSerializer()
    emergency_contact = EmergencyContactSerializer()
    education = EducationSerializer(many=True)
    employment = EmploymentSerializer(many=True)
    languages = SkillSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data
        current_address_data = validated_data.pop('current_address', None)
        permanent_address_data = validated_data.pop('permanent_address', None)
        emergency_contact_data = validated_data.pop('emergency_contact', None)
        education_data = validated_data.pop('education', [])
        employment_data = validated_data.pop('employment', [])
        languages_data = validated_data.pop('languages', [])
        certifications_data = validated_data.pop('certifications', [])
        documents_data = validated_data.pop('documents', [])

        # Create Profile
        profile = Profile.objects.create(**validated_data)

        # Create related objects
        if current_address_data:
            profile.current_address = Address.objects.create(**current_address_data)
        if permanent_address_data:
            profile.permanent_address = Address.objects.create(**permanent_address_data)
        if emergency_contact_data:
            profile.emergency_contact = EmergencyContact.objects.create(**emergency_contact_data)

        profile.save()

        for edu in education_data:
            Education.objects.create(**edu, profile=profile)
        for emp in employment_data:
            Employment.objects.create(**emp, profile=profile)
        for lang in languages_data:
            Skill.objects.create(name=lang['name'], profile=profile)
        for cert in certifications_data:
            Certification.objects.create(name=cert['name'], profile=profile)
        for doc in documents_data:
            Document.objects.create(**doc)

        return profile

    def update(self, instance, validated_data):
        # Update nested fields
        current_address_data = validated_data.pop('current_address', None)
        permanent_address_data = validated_data.pop('permanent_address', None)
        emergency_contact_data = validated_data.pop('emergency_contact', None)
        education_data = validated_data.pop('education', [])
        employment_data = validated_data.pop('employment', [])
        languages_data = validated_data.pop('languages', [])
        certifications_data = validated_data.pop('certifications', [])
        documents_data = validated_data.pop('documents', [])

        # Update main profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related objects
        if current_address_data:
            Address.objects.update_or_create(profile=instance, defaults=current_address_data)
        if permanent_address_data:
            Address.objects.update_or_create(profile=instance, defaults=permanent_address_data)
        if emergency_contact_data:
            EmergencyContact.objects.update_or_create(profile=instance, defaults=emergency_contact_data)

        # Update many-to-many fields
        instance.education.set([Education.objects.create(**edu) for edu in education_data])
        instance.employment.set([Employment.objects.create(**emp) for emp in employment_data])
        instance.languages.set([Skill.objects.create(name=lang['name']) for lang in languages_data])
        instance.certifications.set([Certification.objects.create(name=cert['name']) for cert in certifications_data])
        instance.documents.set([Document.objects.create(**doc) for doc in documents_data])

        return instance
