# sdg-events.de: analysis

This repo contains the code for scraping and analyzing SDG events.

## Deployment

### Creating VPS

The code is deployed on DigitalOcean (1 GB VPS), using the Dokku image from the
marketplace.

### Configuring Dokku

After setting up the droplet, make sure to set up Dokku by going to the droplet
IP address and filling in the hostname: `api.sdg-events.de`

### Upgrading Dokku

Then, we updated Dokku to the
[latest version](https://github.com/dokku/dokku/releases) by installing system
updates:

```
$ sudo apt update
$ sudo apt upgrade
$ sudo reboot
```

Now `dokku --version` should return the latest version.

### Creating the application

Switch to the `dokku` user.

```
$ su dokku
$ cd /
```

Create the application:

```
$ dokku apps:create analysis
-----> Creating analysis...
```

Initialize a bare git repo (which will serve as a remote for deployment):

```
$ dokku git:initialize analysis
-----> Initializing git repository for analysis
```

### Creating the database

Install the postgres plugin (from `root`!):

```
$ sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```

Set up the postgres container:

```
$ dokku postgres:create analysisdb
$ dokku postgreas:link analysisdb analysis
```

This automatically creates the `DATABASE_URL` env var in Dokku, but we need to
replace the adapter from `postgres` to `postgresql` for use with SQLAlchemy:

```
$ dokku config:get analysis DATABASE_URL
postgres://<user>:<password>@<hostname>:5432/analysisdb
$ dokku config:set analysis DATABASE_URL=postgresql://...
```

### Setting environment variables

**NOTE: Currently, the project uses no environment variables (other than the ones set via `dokku`).**

To import environment variables from `.env` to Dokku, run the following command:

```
$ grep -v '^#' .env | xargs -d '\n' ssh dokku@api.sdg-events.de config:set analysis
-----> Setting config vars
       VAR1:  abc
       VAR2:  def
-----> Restarting app analysis
-----> Releasing analysis...
```

### Deploying the application

**On your local machine**, add the new git remote and push:

```
$ git remote add dokku dokku@api.sdg-events.de:analysis
$ git push dokku main
Enumerating objects: 36, done.
Counting objects: 100% (36/36), done.
Delta compression using up to 8 threads
Compressing objects: 100% (22/22), done.
Writing objects: 100% (36/36), 2.87 KiB | 489.00 KiB/s, done.
Total 36 (delta 11), reused 0 (delta 0)
-----> Cleaning up...
-----> Building analysis from dockerfile...
remote: build context to Docker daemon   7.68kB
Step 1/5 : FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
python3.7: Pulling from tiangolo/uvicorn-gunicorn-fastapi

...lots more output

-----> Attempting pre-flight checks (web.1)
   Waiting for 10 seconds ...
   Default container check successful!
-----> Running post-deploy
-----> Creating new app virtual host file...
-----> Configuring api.sdg-events.de...(using built-in template)
-----> Creating http nginx.conf
       Reloading nginx
-----> Renaming containers
       Renaming container (4a2bb8363848) to analysis.web.1
=====> Application deployed:
       http://api.sdg-events.de
```

Visit `http://api-sdg-events.de` and see the API response.

## Running one-off tasks

```bash
$ ssh dokku@api.sdg-events.de run:detached fastapi "python ./task.py"
```

You can follow the logs with:

```
$ ssh dokku@api.sdg-events.de run:list fastapi
$ ssh root@api.sdg-events.de docker logs -f <NAME>
```

The container will be removed automatically once the process has ended.

## Development

We use docker-compose to run the application in development.

To build and start the containers (`api` and `database`), run:

```
$ docker-compose -d up
```

The directory is automatically mounted into the container (`api`) under /app.

### Hot Reloading

Hot reloading is enabled, so any changes made to the code will instantly
reload the FastAPI server.

### Managing dependencies

[Poetry](https://github.com/python-poetry/poetry) is used to manage Python
dependencies. You can install it locally. Alternatively, you can use it within
the `api` container:

```
$ docker-compose exec api bash
$ poetry add <new-package>
```

### Managing migrations

The database is started automatically via docker-compose (`database`). To manage
migrations, enter the `api` container:

```
$ docker-compose exec api bash
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0fda6ea241e1, create account table
```

The database has a dedicated volume mounted, so the database is persisted even
when the container is destroyed/recreated.
