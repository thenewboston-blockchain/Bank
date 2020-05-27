from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.confirmation_block import ConfirmationBlock


class ConfirmationBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmationBlock
        fields = '__all__'
        read_only_fields = all_field_names(ConfirmationBlock)
