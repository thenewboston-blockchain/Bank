from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.decorators.nodes import is_self_signed_message
from ..models.validator import Validator
from ..serializers.validator import ValidatorSerializer, ValidatorSerializerUpdate


class ValidatorViewSet(
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    Validators
    ---
    list:
      description: List validators
    update:
      description: Update validator
      parameters:
        - name: trust
          type: number
    """

    queryset = Validator.objects.all()
    lookup_field = 'node_identifier'
    serializer_class = ValidatorSerializer
    update_serializer_class = ValidatorSerializerUpdate

    @is_self_signed_message
    def update(self, request, *args, **kwargs):

        serializer = self.update_serializer_class(
            self.get_object(),
            data=request.data['message'],
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            self.get_serializer(serializer.save()).data
        )
