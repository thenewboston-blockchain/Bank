import logging

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from thenewboston.constants.network import BANK, CONFIRMATION_VALIDATOR

from v1.cache_tools.cache_keys import CLEAN_LAST_COMPLETED, CLEAN_STATUS
from v1.clean.constants import CLEAN_STATUS_NOT_CLEANING

logger = logging.getLogger('thenewboston')


def clean_nodes(*, nodes_type):
    """
    Clean nodes: delete or update nodes of type BANK or CONFIRMATION_VALIDATOR
    """
    # TODO: implement


@shared_task
def start_clean():
    """
    Start a network clean
    """

    clean_nodes(nodes_type=BANK)
    clean_nodes(nodes_type=CONFIRMATION_VALIDATOR)

    cache.set(CLEAN_LAST_COMPLETED, str(timezone.now()), None)
    cache.set(CLEAN_STATUS, CLEAN_STATUS_NOT_CLEANING, None)

    # TODO: implement
    # send_clean_status_notification()
