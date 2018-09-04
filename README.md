# GloboMap Driver Keystone

Python library to get data from [Keystone](https://auth.s3.globoi.com:5000/v3/).
The data are inserted in API of [Globo Map Core Loader] (https://github.com/globocom/globomap-core-loader) through of [Globo Map API Loader Client] (https://github.com/globocom/globomap-loader-api-client)

## Starting Project:

` make setup `

## Running Tests:

` make setup ` (When project not started yet.)<br>
` make tests `

## Deploy in Tsuru:

` make deploy project=<name of project> `<br>

## Environment variables configuration

All of the environment variables below must be set for the api to work properly.

| Variable                     |  Description                 | Example                                    |
|----------------------------- |------------------------------|--------------------------------------------|
| KEYSTONE_AUTH_URL            | Keystone API endpoint        | https://auth.s3.globoi.com:5000/v3         |
| KEYSTONE_USERNAME            | Keystone username            | username                                   |
| KEYSTONE_PASSWORD            | Keystone password            | xyz                                        |
| KEYSTONE_PROJECT_NAME        | Keystone project name        | project                                    |
| KEYSTONE_USER_DOMAIN_NAME    | Keystone user domain name    | Default                                    |
| KEYSTONE_PROJECT_DOMAIN_NAME | Keystone project domain name | Default                                    |
| GLOBOMAP_LOADER_API_URL      | GloboMap Loader API endpoint | http://api.globomap.loader.domain.com:8080 |
| GLOBOMAP_LOADER_API_USER     | GloboMap Loader API user     | user                                       |
| GLOBOMAP_LOADER_API_PASSWORD | GloboMap Loader API password | password                                   |
| SCHEDULER_FREQUENCY_EXEC     | Frequency of execution.      | 0-23                                       |
| SENTRY_DSN                   | Destination Sentry server.   | https://user:password@sentry.io/test       |

## Licensing

GloboMap Driver Keystone is under [Apache 2 License](./LICENSE)
