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
import os

GLOBOMAP_LOADER_API_URL = os.getenv('GLOBOMAP_LOADER_API_URL')
GLOBOMAP_LOADER_API_USERNAME = os.getenv('GLOBOMAP_LOADER_API_USERNAME')
GLOBOMAP_LOADER_API_PASSWORD = os.getenv('GLOBOMAP_LOADER_API_PASSWORD')

KEYSTONE_AUTH_URL = os.getenv('KEYSTONE_AUTH_URL')
KEYSTONE_USERNAME = os.getenv('KEYSTONE_USERNAME')
KEYSTONE_PASSWORD = os.getenv('KEYSTONE_PASSWORD')
KEYSTONE_PROJECT_NAME = os.getenv('KEYSTONE_PROJECT_NAME')
KEYSTONE_USER_DOMAIN_NAME = os.getenv('KEYSTONE_USER_DOMAIN_NAME')
KEYSTONE_PROJECT_DOMAIN_NAME = os.getenv('KEYSTONE_PROJECT_DOMAIN_NAME')

SCHEDULER_FREQUENCY_EXEC = os.getenv('SCHEDULER_FREQUENCY_EXEC')

WORKERS = int(os.getenv('WORKERS', '1'))

SENTRY_DSN = os.getenv('SENTRY_DSN')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': 'level=%(levelname)s timestamp=%(asctime)s module=%(module)s line=%(lineno)d' +
            'message=%(message)s '
        }
    },
    'handlers': {
        'default': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'sentry'],
            'level': 'WARNING',
            'propagate': True
        },
        'werkzeug': {'propagate': True},
    }
}
