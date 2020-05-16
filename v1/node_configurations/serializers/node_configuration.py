from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.node_configuration import NodeConfiguration


class NodeConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NodeConfiguration
        fields = all_field_names(NodeConfiguration)
