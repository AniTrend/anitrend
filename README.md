# [W.I.P] anitrend-relations-py

A python graphql API for multiple data sources with caching capabilities consumed from the GraphQL service.

## Setup

To get started you need to run the following:

```shell
cp .env.default .env
```

### Virtual environment

This project primarily uses [poetry](https://python-poetry.org/docs/) to manage dependency, after installing run:

```shell
# initialize poetry inside the directory
poetry init

# if you wish to include the venv inside the project remember to execute
poetry config virtualenvs.in-project true

# install dependencies
poetry install
```

### Migrations

If you are not using something like PyCharm your virtual environment may not be automatically activated, all the python commands for this case would need to be run using `poetry run python` see: https://python-poetry.org/docs/basic-usage/#using-poetry-run or alternatively activate your virtual environment by running:

```shell
poetry shell
```

#### Create migrations and migrate

```shell
python manage.py makemigrations
python manage.py migrate
```

## Starting the server

```shell
python manage.py runserver
```

See `http://localhost:8000/playground/` for the graphql editor in debug mode

> Schedule tasks using:
> http://localhost:8000/admin/django_q/schedule/add/
>
> or
>
> ```python
> python manage.py shell
> from django_q.models import Schedule
> Schedule.objects.create(
>     func='module.tasks.method_name',
>     minutes=1,
>     repeats=-1
> )
> ```

If you wish to exporting graphql schema use:

```shell
python manage.py graphql_schema
```

The result will be saved in `./tmp`

## Starting process workers

```shell
python manage.py qcluster
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