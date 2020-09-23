from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ValidationConfirmationConsumer(JsonWebsocketConsumer):

    def connect(self):
        """
        Accepts an incoming socket
        """

        async_to_sync(self.channel_layer.group_add)(
            self.group_name(),
            self.channel_name
        )
        self.accept()

    @staticmethod
    def group_name():
        """
        Name of group where messages will be broadcast
        """

        return 'validation_confirmation_created'

    def send_validation_confirmation_created(self, event):
        """
        Send validation_confirmation_created notification to group
        """

        self.send_json(event['message'])
