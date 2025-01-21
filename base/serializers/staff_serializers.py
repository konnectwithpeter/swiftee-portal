from rest_framework import serializers
from base.models import *


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = "__all__"