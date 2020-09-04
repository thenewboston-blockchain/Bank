from django.core.cache import cache
from rest_framework import serializers

from v1.cache_tools.cache_keys import CRAWL_STATUS
from v1.tasks.crawl import start_crawl
from ..constants import (
    CRAWL_COMMAND_START,
    CRAWL_COMMAND_STOP,
    CRAWL_STATUS_CRAWLING,
    CRAWL_STATUS_NOT_CRAWLING,
    CRAWL_STATUS_STOP_REQUESTED
)


class CrawlSerializer(serializers.Serializer):
    crawl = serializers.ChoiceField(choices=[CRAWL_COMMAND_START, CRAWL_COMMAND_STOP])

    def create(self, validated_data):
        """
        Start a network crawl
        """

        crawl = validated_data['crawl']
        crawl_status = None

        if crawl == CRAWL_COMMAND_START:
            cache.set(CRAWL_STATUS, CRAWL_STATUS_CRAWLING, None)
            start_crawl()
            crawl_status = CRAWL_STATUS_CRAWLING

        if crawl == CRAWL_COMMAND_STOP:
            cache.set(CRAWL_STATUS, CRAWL_STATUS_STOP_REQUESTED, None)
            crawl_status = CRAWL_STATUS_NOT_CRAWLING

        return crawl_status

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def validate_crawl(crawl):
        """
        Validate the correct crawl command is given
        - can not start new crawl when already crawling
        - can not stop crawl if not crawling
        """

        crawl_status = cache.get(CRAWL_STATUS)

        if crawl == CRAWL_COMMAND_START and crawl_status == CRAWL_STATUS_CRAWLING:
            raise serializers.ValidationError('Can not start new crawl when already crawling')

        if crawl == CRAWL_COMMAND_STOP and (
            crawl_status is None or
            crawl_status == CRAWL_STATUS_NOT_CRAWLING
        ):
            raise serializers.ValidationError('Can not stop crawl if not crawling')

        return crawl
