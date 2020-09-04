from rest_framework import serializers


class CrawlSerializer(serializers.Serializer):
    crawl = serializers.ChoiceField(choices=['start', 'stop'])

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')
