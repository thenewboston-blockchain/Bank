from django_filters.rest_framework import FilterSet

from ..models.confirmation_block import ConfirmationBlock


class ConfirmationBlockFilter(FilterSet):

    class Meta:
        model = ConfirmationBlock
        fields = [
            'block',
            'block__signature'
        ]
