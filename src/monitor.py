#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegramapi import Chat
from checkurl import CheckUrl
import time
import argparse
import os
import json
import syslog
from pathlib import Path


def main(url, token, chat_id, timelapse):
    try:
        checkUrl = CheckUrl(url)
        checkUrl.is_changed()
        chat = Chat(token, chat_id)
        chat.send_message('Monitor start to watch {}'.format(url))
        syslog.syslog('Monitor start to watch {}'.format(url))
        while True:
            if checkUrl.is_up():
                syslog.syslog('La url {} está arriba'.format(url))
                if checkUrl.is_changed():
                    chat.send_message('La url {} ha cambiado'.format(url))
                    syslog.syslog('La url {} ha cambiado'.format(url))
                else:
                    syslog.syslog('La url {} no ha cambiado'.format(url))
            else:
                chat.send_message('La url {} está caida'.format(url))
                syslog.syslog('La url {} está caida'.format(url))
            time.sleep(timelapse)
    except KeyboardInterrupt:
        pass
    chat.send_message('Monitor stop to watch {}'.format(url))
    syslog.syslog('Monitor stop to watch {}'.format(url))


if __name__ == '__main__':
    url = None
    thisfile = Path(__file__)
    envfile = thisfile.absolute().parent / 'env.json'
    if envfile.exists():
        with open(envfile, 'r') as fr:
            env = json.load(fr)
            url = env['url']
            token = env['token']
            chat_id = env['chat_id']
            timelapse = env['timelapse']
    else:
        parser = argparse.ArgumentParser(description='Monitorize url')
        parser.add_argument('--url', help='url to monitorize', required=True)
        parser.add_argument('--token', help='token of the Telegram Bot',
                            required=True)
        parser.add_argument('--chat_id', help='id of the chat', required=True)
        parser.add_argument('--timelapse', help='time between checks',
                            type=int, default=300)

        args = parser.parse_args()

        url = args.url
        token = args.token
        chat_id = args.chat_id
        timelapse = args.timelapse

    if url is not None:
        main(url, token, chat_id, timelapse)
