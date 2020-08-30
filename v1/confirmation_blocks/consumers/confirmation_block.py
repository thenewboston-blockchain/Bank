import re

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ConfirmationBlockConsumer(JsonWebsocketConsumer):
    def connect(self):
        url_route = self.scope.get('url_route')
        if not url_route:
            # We need this for testing, as url_route not available during tests
            account_identifier = re.match(
                '^ws/confirmation_blocks/(?P<account_identifier>[a-f0-9]{64})',
                self.scope['path']
            ).group(1)
        else:
            account_identifier = url_route['kwargs']['account_identifier']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name(account_identifier),
            self.channel_name
        )
        self.accept()

    @staticmethod
    def group_name(acount_identifier):
        return 'confirmation_blocks_%s' % acount_identifier

    def send_confirmation_block(self, event):
        self.send_json(event['message'])
