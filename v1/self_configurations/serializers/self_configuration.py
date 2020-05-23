from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.self_configuration import SelfConfiguration


class SelfConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelfConfiguration
        fields = '__all__'
        read_only_fields = all_field_names(SelfConfiguration)
