from rest_framework import serializers

from ..models.node_configuration import NodeConfiguration


class NodeConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NodeConfiguration
        fields = '__all__'
