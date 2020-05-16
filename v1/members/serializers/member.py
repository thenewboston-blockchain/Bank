from rest_framework import serializers

from v1.network.utils.serializers import all_field_names
from ..models.member import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = all_field_names(Member)
