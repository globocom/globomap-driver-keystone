"""
   Copyright 2017 Globo.com

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
# -*- coding: utf-8 -*-
import json
import logging
import requests
import time

from globomap_driver_keystone import settings

from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from keystoneclient.v3 import client


class Keystone(object):

    def __init__(self):
        auth = v3.Password(auth_url=settings.KEYSTONE_AUTH_URL,
                           username=settings.KEYSTONE_USERNAME,
                           password=settings.KEYSTONE_PASSWORD,
                           project_name=settings.KEYSTONE_PROJECT_NAME,
                           user_domain_name=settings.KEYSTONE_USER_DOMAIN_NAME,
                           project_domain_name=settings.KEYSTONE_PROJECT_DOMAIN_NAME)

        self.session = Session(auth=auth)

    def get_projects(self):
        self.conn = client.Client(session=self.session)
        project_list = self.conn.projects.list()
        data = []

        for project in project_list:
            data.append(self.treat_projects(project))

        return data

    def get_users(self):
        self.conn = client.Client(session=self.session)
        user_list = self.conn.users.list()
        data = []

        for user in user_list:
            data.append(self.treat_users(user))

        return data

    def get_roles(self):
        self.conn = client.Client(session=self.session)
        role_list = self.conn.roles.list()
        user_list = self.conn.users.list()
        roles = {}
        data = []

        for role in role_list:
            roles[role.id] = role.name

        for user in user_list:
            roles_users = self.conn.role_assignments.list(user)
            for role_user in roles_users:
                role = self.treat_roles(role_user, roles)
                if (role):
                    data.append(role)

        return data

    def treat_projects(self, project):
        """ Treat project """

        project = project.to_dict()
        element = {
            'id': project.get('id'),
            'name': project.get('name'),
            'provider': 'ks',
            'properties': {
                'description': project['description'],
                'enabled': json.dumps(project.get('enabled')),
                'is_domain': json.dumps(project.get('is_domain')),
                'domain_id': project['domain_id'],
                'parent_id': project['parent_id'],
                'links': project.get('links')
            },
            'properties_metadata': {
                'description': {
                    'description': 'Description'
                },
                'enabled': {
                    'description': 'Enabled'
                },
                'is_domain': {
                    'description': 'Is Domain'
                },
                'domain_id': {
                    'description': 'Domain ID'
                },
                'parent_id': {
                    'description': 'Parent ID'
                },
                'links': {
                    'description': 'Links'
                }
            }
        }

        return self.encapsulate('ks_project', 'collections', element)

    def treat_users(self, user):
        """ Treat user """

        user = user.to_dict()
        element = {
            'id': user.get('id'),
            'name': user.get('name'),
            'provider': 'ks',
            'properties': {
                'email': user.get('email'),
                'domain_id': user.get('domain_id'),
                'default_project_id': user.get('default_project_id'),
                'enabled': user.get('enabled'),
                'options': user.get('options'),
                'password_expires_at': user.get('password_expires_at'),
                'links': user.get('links')
            },
            'properties_metadata': {
                'email': {
                    'description': 'Email'
                },
                'domain_id': {
                    'description': 'Domain ID'
                },
                'default_project_id': {
                    'description': 'Default Project ID'
                },
                'enabled': {
                    'description': 'Enabled'
                },
                'options': {
                    'description': 'Options'
                },
                'password_expires_at': {
                    'description': 'Password Expires At'
                },
                'links': {
                    'description': 'Links'
                }
            }
        }

        return self.encapsulate('ks_user', 'collections', element)

    def treat_roles(self, role_user, roles):
        """ Treat role """

        role_user = role_user.to_dict()

        try:
            role_id = role_user.get('role').get('id')
            project_id = role_user.get('scope').get('project').get('id')
            user_id = role_user.get('user').get('id')
            source = 'ks_project/ks_{}'.format(project_id)
            target = 'ks_user/ks_{}'.format(user_id)
        except Exception:
            return None

        element = {
            'id': '{}{}'.format(role_id, user_id),
            'name': roles[role_id],
            'provider': 'ks',
            'from': source,
            'to': target,
        }

        return self.encapsulate('ks_role', 'edges', element)

    def encapsulate(self, collection, kind, element):
        element['timestamp'] = int(time.time())
        data = {
            'collection': collection,
            'type': kind,
            'action': 'UPDATE',
            'element': element,
            'key': '{}_{}'.format(element['provider'], element['id'])
        }

        return data
