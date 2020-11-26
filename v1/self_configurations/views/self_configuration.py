from django.utils.decorators import classonlymethod
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..helpers.self_configuration import get_self_configuration
from ..serializers.self_configuration import SelfConfigurationSerializer


class SelfConfigurationViewSet(
    ListModelMixin,
    GenericViewSet,
):
    """
    Self configuration

    ---
    get:
      description: Get self configuration details
    """

    serializer_class = SelfConfigurationSerializer

    @classonlymethod
    def as_view(cls, actions=None, **kwargs):
        return super().as_view(actions={'get': 'retrieve_first'}, **kwargs)

    def retrieve_first(self, request, *args, **kwargs):
        return Response(
            self.get_serializer(
                get_self_configuration(exception_class=RuntimeError)
            ).data
        )
