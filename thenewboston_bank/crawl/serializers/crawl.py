from django.core.cache import cache
from rest_framework import serializers
from thenewboston.constants.crawl import (
    CRAWL_COMMAND_START,
    CRAWL_COMMAND_STOP,
    CRAWL_STATUS_CRAWLING,
    CRAWL_STATUS_NOT_CRAWLING,
    CRAWL_STATUS_STOP_REQUESTED
)

from thenewboston_bank.cache_tools.cache_keys import CRAWL_CACHE_LOCK_KEY, CRAWL_STATUS
from thenewboston_bank.tasks.crawl import start_crawl


class CrawlSerializer(serializers.Serializer):
    crawl = serializers.ChoiceField(choices=[CRAWL_COMMAND_START, CRAWL_COMMAND_STOP])

    default_error_messages = {
        **serializers.Serializer.default_error_messages,
        'cant_start_crawl': 'Can not start new crawl when already crawling',
        'cant_stop_crawl': 'Can not stop crawl if not crawling',
    }

    def create(self, validated_data):
        """Start a network crawl"""
        crawl = validated_data['crawl']

        if crawl == CRAWL_COMMAND_START:
            cache.set(CRAWL_STATUS, CRAWL_STATUS_CRAWLING, None)
            start_crawl.delay()

        if crawl == CRAWL_COMMAND_STOP:
            cache.set(CRAWL_STATUS, CRAWL_STATUS_STOP_REQUESTED, None)

        return validated_data

    def is_valid(self, raise_exception=False):
        with cache.lock(CRAWL_CACHE_LOCK_KEY):
            return super().is_valid(raise_exception)

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate_crawl(self, crawl):
        """
        Validate the correct crawl command is given

        - can not start new crawl when already crawling
        - can not stop crawl if not crawling
        """
        crawl_status = cache.get(CRAWL_STATUS)

        if crawl == CRAWL_COMMAND_START and crawl_status in (CRAWL_STATUS_CRAWLING, CRAWL_STATUS_STOP_REQUESTED):
            raise serializers.ValidationError(self.error_messages['cant_start_crawl'])

        if crawl == CRAWL_COMMAND_STOP and crawl_status in (CRAWL_STATUS_NOT_CRAWLING, CRAWL_STATUS_STOP_REQUESTED):
            raise serializers.ValidationError(self.error_messages['cant_stop_crawl'])

        return crawl
