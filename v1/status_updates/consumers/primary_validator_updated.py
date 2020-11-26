from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class PrimaryValidatorUpdatedConsumer(JsonWebsocketConsumer):

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
        return 'primary_validator_updated'

    def send_primary_validator_updated(self, event):
        """Send primary_validator_updated notification to group"""
        self.send_json(event['message'])
