#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json
from checkurl import CheckUrl
from telegramapi import Chat


class TestCheckUrl(unittest.TestCase):

    def test_is_up(self):
        url = 'https://www.google.com'
        checkUrl = CheckUrl(url)
        self.assertTrue(checkUrl.is_up())

    def test_is_changed(self):
        url = 'https://www.google.com'
        checkUrl = CheckUrl(url)
        checkUrl.delete()
        self.assertTrue(checkUrl.is_changed())
        self.assertFalse(checkUrl.is_changed())
        checkUrl.delete()
        self.assertFalse(os.path.exists(checkUrl.get_tempfile()))

    def test_send_message(self):
        with open('env.json') as fr:
            env = json.load(fr)
            message = 'esto es un mensage'
            token = env['token']
            chat_id = env['chat_id']
            chat = Chat(token, chat_id)
            self.assertTrue(chat.send_message(message))


if __name__ == '__main__':
    unittest.main()
