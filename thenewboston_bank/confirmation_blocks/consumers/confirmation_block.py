import re

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ConfirmationBlockConsumer(JsonWebsocketConsumer):

    def connect(self):
        """Accepts an incoming socket"""
        url_route = self.scope.get('url_route')

        if url_route:
            account_number = url_route['kwargs']['account_number']
        else:
            # We need this for testing, as url_route is not available during tests
            account_number = re.match(
                '^ws/confirmation_blocks/(?P<account_number>[a-f0-9]{64})',
                self.scope['path']
            ).group(1)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name(account_number),
            self.channel_name
        )
        self.accept()

    @staticmethod
    def group_name(account_number):
        """Name of group where messages will be broadcast"""
        return 'confirmation_blocks_%s' % account_number

    def send_confirmation_block(self, event):
        """Send confirmation block notification to group"""
        self.send_json(event['message'])
