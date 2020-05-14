from rest_framework import serializers

from ..models.member import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'
