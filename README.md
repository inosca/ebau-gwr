# ebau-gwr

[![Build Status](https://github.com/inosca/ebau-gwr/workflows/Tests/badge.svg)](https://github.com/inosca/ebau-gwr/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/inosca/ebau-gwr/blob/main/pyproject.toml#L96)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

GWR synchronisation for ebau projects

## Getting started

### Installation

**Requirements**

- docker
- docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/inosca/ebau-gwr/main/docker-compose.yml) and run the following command:

```bash
echo UID=$UID > .env

docker compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Configuration

ebau-gwr is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

A list of configuration options which you need to set when using ebau-gwr as a
standalone service:

- `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
- `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
- `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
- `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
- `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
- `DATABASE_NAME`: Name of database to use (default: ebau-gwr)
- `DATABASE_USER`: Username to use when connecting to the database (default: ebau-gwr)
- `DATABASE_PASSWORD`: Password to use when connecting to database

##### App specific settings

A list of configuration options which you need to set in any case:

- `GWR_WSK_ID`: This is the ID that has been assigned to you by the BfS
- `GWR_FERNET_KEY`: A secret key used for encrypting the passwords in housing stat credentials. Can be generated with the `generate_fernet_key` command

By default, the app will talk to the GWR production API if running with `ENV=production` (and the test API otherwise). You can overwrite this behavior by setting

- `GWR_HOUSING_STAT_BASE_URI`: base uri of GWR API, e.g. `"https://www-r.housing-stat.ch/regbl/api/ech0216/2"`

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.

## Maintenance

A few notes for maintainers can be found [here](MAINTENANCE.md).
