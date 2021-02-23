from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class CleanStatusConsumer(JsonWebsocketConsumer):

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
        return 'clean_status'

    def send_clean_status(self, event):
        """Send clean_status notification to group"""
        self.send_json(event['message'])
