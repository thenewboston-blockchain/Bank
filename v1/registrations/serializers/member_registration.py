from rest_framework import serializers

from ..models.member_registration import MemberRegistration


class MemberRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberRegistration
        fields = '__all__'
