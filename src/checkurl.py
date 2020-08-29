#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import hashlib
import tempfile
import os


class CheckUrl():

    def __init__(self, url):
        self._url = url
        self._b64 = base64.b64encode(url.encode('utf-8')).decode()
        self._tempfile = os.path.join(tempfile.gettempdir(),
                                      self._b64 + '.check_url')
        self.is_changed()

    def delete(self):
        os.remove(self._tempfile)

    def get_tempfile(self):
        return self._tempfile

    def _get_hash(self):
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                hash_object = hashlib.md5(response.text.encode('utf-8'))
                return hash_object.hexdigest()
        except Exception:
            pass
        return None

    def is_up(self):
        try:
            response = requests.get(self._url)
            return response.status_code == 200
        except Exception:
            pass
        return False

    def is_changed(self):
        changed = True
        new_hash = self._get_hash()
        if os.path.exists(self._tempfile):
            with open(self._tempfile, 'r') as fr:
                old_hash = fr.read()
                changed = old_hash == new_hash
        with open(self._tempfile, 'w') as fw:
            fw.write(new_hash)
        return changed


def main(url):
    check_url = CheckUrl(url)
    print('Is up: {}'.format(check_url.is_up()))
    print('Is changed: {}'.format(check_url.is_changed()))
    check_url.delete()
    print('Is changed: {}'.format(check_url.is_changed()))



if __name__ == '__main__':
    main('https://www.google.es')
