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
import multiprocessing
import itertools

from time import time

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update

from globomap_driver_keystone import settings
from globomap_driver_keystone.keystone import Keystone
from globomap_driver_keystone.util import clear


class Loader(object):

    logger = logging.getLogger(__name__)
    update = None

    def __init__(self):
        self.keystone = Keystone()
        self.page = 100
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_API_URL,
            username=settings.GLOBOMAP_LOADER_API_USERNAME,
            password=settings.GLOBOMAP_LOADER_API_PASSWORD
        )
        Loader.update = Update(auth=auth_inst, driver_name='keystone')

    @staticmethod
    def send(data):
        try:
            res = Loader.update.post(data)
        except Exception:
            Loader.logger.exception('Message dont sent %s', json.dumps(data))
        else:
            return res

    def run(self):
        current_time = int(time())
        pool = multiprocessing.Pool(processes=settings.WORKERS)

        projects = self.keystone.get_projects()
        self.run_workers(pool, projects)

        users = self.keystone.get_users()
        self.run_workers(pool, users)

        roles = self.keystone.get_roles()
        self.run_workers(pool, roles)

        self.run_clean(current_time)
        pool.close()

    def run_clean(self, current_time):
        documents = [
            clear('ks_project', 'collections', current_time),
            clear('ks_user', 'collections', current_time),
            clear('ks_role', 'edges', current_time)
        ]
        Loader.send(documents)

    def run_workers(self, pool, data, length=100):
        for _ in pool.imap_unordered(
                Loader.send, self.iterator_slice(data, length)):
            pass

    def iterator_slice(self, iterator, length):
        start = 0
        end = length

        while True:
            res = list(itertools.islice(iterator, start, end))
            start += length
            end += length
            if not res:
                break
            yield res
