import requests
import logging

__all__ = ['Client']


class Client(object):

    BASE_URL = 'http://online.sigmasms.ru/api'

    def __init__(self, username=None, password=None, sender=None):
        self.username = username
        self.password = password
        self.sender = sender
        self.token = None
        self.session = requests.Session()

    def _auth(self):
        if not (self.username and self.password):
            raise ValueError('Login and password are expected to be non-zero'
                             ' length strings')
        if not self.token:
            self._set_token()

    def _set_token(self):
        url = self.BASE_URL + '/login'
        payload = {'username': self.username, 'password': self.password}
        resp = self.session.request('POST', url, json=payload)
        json = resp.json()
        self.token = json['token'] if not json.get('error') else None

    def send_message(self, recipient, text, msg_type):
        self._auth()
        url = self.BASE_URL + '/sendings'
        payload = {
                'recipient': recipient,
                'type': msg_type,
                'payload': {
                    'sender': self.sender,
                    'text': text
                }
            }
        headers = {'Authorization': self.token}
        resp = self.session.request('POST', url, json=payload, headers=headers)
        return resp

    def check_status(self, message_id):
        self._auth()
        url = self.BASE_URL + '/sendings/' + message_id
        headers = {'Authorization': self.token}
        resp = self.session.request('GET', url, headers=headers)
        return resp
