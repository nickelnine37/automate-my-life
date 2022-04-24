from http.client import HTTPSConnection
from urllib.parse import urlencode
import json
from secrets.config import secrets


class Notification:

    def __init__(self, title: str, message: str):
        """
        Creates a Pushover Notification object.
        """

        self.title = title
        self.message = message

    def send(self):

        data = urlencode({'token': secrets['pushover_api_token'],
                          'user': secrets['pushover_user_token'],
                          'title': self.title,
                          'message': self.message})

        conn = HTTPSConnection('api.pushover.net:443')
        conn.request('POST', '/1/messages.json', data, {'Content-type': 'application/x-www-form-urlencoded'})
        output = conn.getresponse().read().decode('utf-8')
        data = json.loads(output)

        if data['status'] != 1:
            print(f'Failed to send notification with title {self.title}')

