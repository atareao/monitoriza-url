#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class Chat():
    def __init__(self, token, chat_id):
        self._token = token
        self._chat_id = chat_id

    def send_message(self, message):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(self._token)
        data = {'chat_id': self._chat_id, 'text': message}
        response = requests.post(url, data)
        return response.status_code == 200 and response.json()['ok'] is True
