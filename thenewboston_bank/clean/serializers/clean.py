from django.core.cache import cache
from rest_framework import serializers
from thenewboston.constants.clean import (
    CLEAN_COMMAND_START,
    CLEAN_COMMAND_STOP,
    CLEAN_STATUS_CLEANING,
    CLEAN_STATUS_NOT_CLEANING,
    CLEAN_STATUS_STOP_REQUESTED
)

from thenewboston_bank.cache_tools.cache_keys import CLEAN_CACHE_LOCK_KEY, CLEAN_STATUS
from thenewboston_bank.tasks.clean import start_clean


class CleanSerializer(serializers.Serializer):
    clean = serializers.ChoiceField(choices=[CLEAN_COMMAND_START, CLEAN_COMMAND_STOP])

    default_error_messages = {
        **serializers.Serializer.default_error_messages,
        'cant_start_clean': 'Can not start new clean when already cleaning',
        'cant_stop_clean': 'Can not stop clean if not cleaning',
    }

    def create(self, validated_data):
        """Start a network clean"""
        clean = validated_data['clean']

        if clean == CLEAN_COMMAND_START:
            cache.set(CLEAN_STATUS, CLEAN_STATUS_CLEANING, None)
            start_clean.delay()

        if clean == CLEAN_COMMAND_STOP:
            cache.set(CLEAN_STATUS, CLEAN_STATUS_STOP_REQUESTED, None)

        return validated_data

    def is_valid(self, raise_exception=False):
        with cache.lock(CLEAN_CACHE_LOCK_KEY):
            return super().is_valid(raise_exception)

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate_clean(self, clean):
        """
        Validate the correct clean command is given

        - can not start new clean when already cleaning
        - can not stop clean if not cleaning
        """
        clean_status = cache.get(CLEAN_STATUS)

        if clean == CLEAN_COMMAND_START and clean_status in (CLEAN_STATUS_CLEANING, CLEAN_STATUS_STOP_REQUESTED):
            raise serializers.ValidationError(self.error_messages['cant_start_clean'])

        if clean == CLEAN_COMMAND_STOP and clean_status in (CLEAN_STATUS_NOT_CLEANING, CLEAN_STATUS_STOP_REQUESTED):
            raise serializers.ValidationError(self.error_messages['cant_stop_clean'])

        return clean
