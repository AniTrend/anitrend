# [W.I.P] Anitrend Relations

A python graphql API for [anime-offline-database](https://github.com/manami-project/anime-offline-database) which is updated every week: A JSON based offline anime database containing the most important meta-data as well as cross-references to various anime sites such as MAL, ANIDB, ANILIST, KITSU and more...

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FAniTrend%2Fanitrend-relations-py.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FAniTrend%2Fanitrend-relations-py?ref=badge_large)

## Setup

### Virtual environment
Make install a virtual environment for your OS if one is not already installed see: 
https://docs.python.org/3/tutorial/venv.html for more information

#### Create virtual environment
```shell 
python3 -m venv venv
```

#### Install requirements
```shell
source venv/bin/activate
pip install -r requirements.txt
```


### Migrations
#### Create migrations and migrate
```shell
./scripts/manage.py makemigrations
./scripts/manage.py migrate
```

## Starting the server

```shell
./scripts/manage.py runserver
```
See `http://localhost:8000/graphql/` for the graphql editor in debug mode

> Schedule tasks using:
> http://localhost:8000/admin/django_q/schedule/add/
> 
> or
> 
> ```python
> ./scripts/manage.py shell
> from django_q.models import Schedule
> Schedule.objects.create(
>     func='module.tasks.method_name',
>     minutes=1,
>     repeats=-1
> )
> ```

If you wish to exporting graphql schema use:
```shell
./scripts/manage.py graphql_schema
```
The result will be saved in `./tmp`

## Starting process workers

```shell
./scripts/manage.py qcluster
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