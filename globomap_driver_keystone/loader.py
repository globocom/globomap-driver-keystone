"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json
import logging

from time import time

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update

from globomap_driver_keystone import settings
from globomap_driver_keystone.keystone import Keystone
from globomap_driver_keystone.util import clear


class Loader(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.keystone = Keystone()
        self.page = 100
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_API_URL,
            username=settings.GLOBOMAP_LOADER_API_USERNAME,
            password=settings.GLOBOMAP_LOADER_API_PASSWORD
        )
        self.update = Update(auth=auth_inst, driver_name='keystone')

    def send(self, data):
        try:
            return self.update.post(data)
        except Exception:
            self.logger.exception('Message dont sent %s', json.dumps(data))

    def run(self):
        current_time = int(time())

        projects = self.keystone.get_projects()
        self.iterator_slice(projects, self.page)

        users = self.keystone.get_users()
        self.iterator_slice(users, self.page)

        roles = self.keystone.get_roles()
        self.iterator_slice(roles, self.page)

        self.run_clean(current_time)

    def run_clean(self, current_time):
        documents = [
            clear('ks_project', 'collections', current_time),
            clear('ks_user', 'collections', current_time),
            clear('ks_role', 'edges', current_time)
        ]
        self.send(documents)

    def iterator_slice(self, iterator, length):
        start = 0
        end = length

        while True:
            items = iterator[start:end]
            start += length
            end += length
            if not items:
                break
            self.send(items)
