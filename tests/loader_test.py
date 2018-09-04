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
import unittest2

from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_keystone.loader import Loader


class TestLoader(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def test_send(self):
        """ Test send """

        self._mock_update()

        self.loader = Loader()
        self.loader.update.post = Mock(return_value='test')
        data = self.loader.send('test')

        self.assertEqual(data, 'test')
        self.loader.update.post.assert_called_with('test')

    def test_run(self):
        """ Test run """

        self._mock_update()

        self.loader = Loader()

        project = self._open_file('tests/json/project.json')
        user = self._open_file('tests/json/user.json')
        role = self._open_file('tests/json/role.json')

        self.loader.run_clean = MagicMock()
        self.loader.keystone.get_projects = MagicMock(return_value=project)
        self.loader.keystone.get_users = MagicMock(return_value=user)
        self.loader.keystone.get_roles = MagicMock(return_value=role)

        self.loader.run()

        self.loader.run_clean.assert_called()
        self.loader.keystone.get_projects.assert_called()
        self.loader.keystone.get_users.assert_called()
        self.loader.keystone.get_roles.assert_called()

    def test_run_clean(self):
        """ Test clean of collections """

        self._mock_update()

        documents = self._open_file('tests/json/clean.json')

        self.loader = Loader()
        self.loader.update.post = MagicMock(return_value=documents)
        self.loader.run_clean(123456789)

        self.loader.update.post.assert_called_with(documents)

    def test_iterator_slice(self):
        """ Test iterator slice """

        self._mock_update()

        self.loader = Loader()
        self.loader.send = MagicMock()

        data = [1, 2, 3]
        self.loader.iterator_slice(data, 2)

        call_count = self.loader.send.call_count
        self.assertEqual(call_count, 2)

        call_args_list = self.loader.send.call_args_list

        first_call = call_args_list[0][0][0]
        self.assertEqual(first_call, [1, 2])

        last_call = call_args_list[1][0][0]
        self.assertEqual(last_call, [3])

    def _mock_update(self):
        patch('globomap_driver_keystone.loader.auth').start()
        patch('globomap_driver_keystone.loader.Update').start()

    def _open_file(self, file):
        with open(file, 'r') as file:
            item = json.load(file)

        return item
