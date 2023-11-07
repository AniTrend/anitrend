# anitrend

A GraphQL API for multiple data sources with caching capabilities.

## Setup

To get started you need to run the following:

```shell
cp .env.default .env
```

### Virtual environment

This project primarily uses [poetry](https://python-poetry.org/docs/) to manage dependency, after installing run:

```shell
poetry init
poetry install
```

### Migrations

If you are not using something like PyCharm your virtual environment may not be automatically activated, all the python
commands for this case would need to be run using `poetry run python` see: https://python-poetry.org/docs/basic-usage/#using-poetry-run

#### Create migrations and migrate

```shell
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Starting the server

```shell
poetry run python manage.py runserver
```

If you wish to exporting graphql schema use:

```shell
poetry run python manage.py graphql_schema
```

The result will be saved in `./tmp`

## Starting process workers

```shell
poetry run python manage.py qcluster
```

See `/admin/django_q/` for tasks updates

## License

```
    Copyright (C) 2021  AniTrend

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```