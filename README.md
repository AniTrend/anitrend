# [W.I.P] AniTrend Relations

A python graphql API for multiple data sources which works by polling for information and 
building database records which can be consumed from the GraphQL service.

## Setup

Create a `.env` file in the root directory of this project with the following contents:
```shell
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=CREATE_ANY_RANDOM_KEY
DJANGO_DATABASE_NAME=POSTGRES_DB_NAME
DJANGO_DATABASE_USER=POSTGRES_DB_USER
DJANGO_DATABASE_PASSWORD=POSTGRES_DB_USER_PASSWORD
DJANGO_DATABASE_HOST=POSTGRES_DB_HOST
DJANGO_DATABASE_PORT=POSTGRES_DB_PORT
```

### Virtual environment
Make install a virtual environment for your OS if one is not already installed see: 
https://docs.python.org/3/tutorial/venv.html for more information

#### Create virtual environment
```shell 
python3 -m virtualenv venv
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