from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.member import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = all_field_names(Member)
