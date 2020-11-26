from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ValidatorConfirmationServiceConsumer(JsonWebsocketConsumer):

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
        return 'validator_confirmation_service'

    def send_validator_confirmation_service(self, event):
        """Send validator confirmation service notification to group"""
        self.send_json(event['message'])
