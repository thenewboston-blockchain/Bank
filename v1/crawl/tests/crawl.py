import time

import pytest
from django.core.cache import cache
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from thenewboston.constants.crawl import (
    CRAWL_COMMAND_START,
    CRAWL_COMMAND_STOP,
    CRAWL_STATUS_CRAWLING,
    CRAWL_STATUS_NOT_CRAWLING,
    CRAWL_STATUS_STOP_REQUESTED
)
from thenewboston.utils.signed_requests import generate_signed_request

from v1.cache_tools.cache_keys import CRAWL_STATUS
from v1.self_configurations.helpers.signing_key import get_signing_key
from ..serializers.crawl import CrawlSerializer


def crawl_request(client, command, status):
    return client.post_json(
        reverse('crawl-list'),
        generate_signed_request(
            data={
                'crawl': command
            },
            nid_signing_key=get_signing_key()
        ),
        expected=status,
    )


def crawl_status(client):
    return client.get_json(
        reverse('crawl-list'),
        expected=HTTP_200_OK,
    )


@pytest.mark.django_db(transaction=True)
def test_crawl_start_200(client, self_configuration, celery_worker):
    response = crawl_request(client, CRAWL_COMMAND_START, HTTP_200_OK)

    assert response['crawl_last_completed'] is None
    assert response['crawl_status'] == CRAWL_STATUS_CRAWLING

    assert cache.get(CRAWL_STATUS) == CRAWL_STATUS_CRAWLING
    time.sleep(2)
    assert cache.get(CRAWL_STATUS) == CRAWL_STATUS_NOT_CRAWLING
    assert crawl_status(client)['crawl_status'] == CRAWL_STATUS_NOT_CRAWLING


def test_crawl_start_400_already_crawling(client, self_configuration):
    cache.set(CRAWL_STATUS, CRAWL_STATUS_CRAWLING, None)

    response = crawl_request(client, CRAWL_COMMAND_START, HTTP_400_BAD_REQUEST)
    assert response['crawl'] == [CrawlSerializer().error_messages['cant_start_crawl']]
    assert crawl_status(client)['crawl_status'] == CRAWL_STATUS_CRAWLING


def test_crawl_start_400_stop_requested(client, self_configuration):
    cache.set(CRAWL_STATUS, CRAWL_STATUS_STOP_REQUESTED, None)

    response = crawl_request(client, CRAWL_COMMAND_START, HTTP_400_BAD_REQUEST)
    assert response['crawl'] == [CrawlSerializer().error_messages['cant_start_crawl']]
    assert crawl_status(client)['crawl_status'] == CRAWL_STATUS_STOP_REQUESTED


@pytest.mark.django_db(transaction=True)
def test_crawl_stop_200(client, self_configuration, celery_worker):
    crawl_request(client, CRAWL_COMMAND_START, HTTP_200_OK)
    response = crawl_request(client, CRAWL_COMMAND_STOP, HTTP_200_OK)

    assert response['crawl_last_completed'] is None
    assert response['crawl_status'] == CRAWL_STATUS_STOP_REQUESTED
    time.sleep(2)
    assert cache.get(CRAWL_STATUS) == CRAWL_STATUS_NOT_CRAWLING
    assert crawl_status(client)['crawl_status'] == CRAWL_STATUS_NOT_CRAWLING


def test_crawl_stop_400_not_crawling(client, self_configuration):
    cache.set(CRAWL_STATUS, CRAWL_STATUS_NOT_CRAWLING, None)

    response = crawl_request(client, CRAWL_COMMAND_STOP, HTTP_400_BAD_REQUEST)
    assert response['crawl'] == [CrawlSerializer().error_messages['cant_stop_crawl']]
    assert crawl_status(client)['crawl_status'] == CRAWL_STATUS_NOT_CRAWLING


@pytest.mark.parametrize(
    'status',
    [
        CRAWL_STATUS_CRAWLING,
        CRAWL_STATUS_NOT_CRAWLING,
        CRAWL_STATUS_STOP_REQUESTED
    ]
)
def test_crawl_status_200(client, status, self_configuration):
    cache.set(CRAWL_STATUS, status, None)
    assert crawl_status(client)['crawl_status'] == status
