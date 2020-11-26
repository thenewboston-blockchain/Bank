from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class CrawlStatusConsumer(JsonWebsocketConsumer):

    def connect(self):
        """Accepts an incoming socket"""
        async_to_sync(self.channel_layer.group_add)(
            self.group_name(),
            self.channel_name
        )
        self.accept()

    @staticmethod
    def group_name():
        """Name of group where messages will be broadcast"""
        return 'crawl_status'

    def send_crawl_status(self, event):
        """Send crawl_status notification to group"""
        self.send_json(event['message'])
