# sdg-events.de: analysis

This repo contains the code for scraping and analyzing SDG events.

## Table of Contents

- [sdg-events.de: analysis](#sdg-eventsde-analysis)
  - [Table of Contents](#table-of-contents)
  - [Deployment](#deployment)
    - [Creating VPS](#creating-vps)
    - [Configuring Dokku](#configuring-dokku)
    - [Upgrading Dokku](#upgrading-dokku)
    - [Creating the application](#creating-the-application)
    - [Creating the database](#creating-the-database)
    - [Setting environment variables](#setting-environment-variables)
    - [Deploying the application](#deploying-the-application)
    - [Enabling HTTPS](#enabling-https)
  - [Running one-off tasks](#running-one-off-tasks)
    - [Scraping](#scraping)
  - [Development](#development)
    - [Hot Reloading](#hot-reloading)
    - [Managing dependencies](#managing-dependencies)
    - [Managing migrations](#managing-migrations)
  - [Testing](#testing)

## Deployment

### Creating VPS

The code is deployed on DigitalOcean (1 GB VPS), using the Dokku image from the
marketplace.

### Configuring Dokku

After setting up the droplet, make sure to set up Dokku by going to the droplet
IP address and filling in the hostname: `api.sdg-events.de`

We may need to double check the hostname. We can check the hostname using:

```
$ dokku domains:report --global
       Domains global enabled:        true
       Domains global vhosts:         api.sdg-events.de
```

If this does not return `api.sdg-events.de`, we need to set it manually:

```
$ dokku domains:set-global api.sdg-events.de
```

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

We also need to enable Docker Buildkit support (for caching dependencies
between builds for faster deployments):

```
$ echo "export DOCKER_BUILDKIT=1" | sudo tee -a /etc/default/dokku
$ echo "export BUILDKIT_PROGRESS=plain" | sudo tee -a /etc/default/dokku
```

### Creating the database

Install the postgres plugin (from `root`!):

```
$ sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```

Set up the postgres container:

```
$ dokku postgres:create analysisdb
$ dokku postgres:link analysisdb analysis
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

Visit [http://api-sdg-events.de](http://api-sdg-events.de) and see the API
response.

### Enabling HTTPS

Thanks to Dokku, setting up https is very easy. Run as `root`:

```
$ sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
```

Then set your email address:

```
$ dokku config:set --no-restart analysis DOKKU_LETSENCRYPT_EMAIL=your@email.tld
```

Then enable encryption and set up a cron job for automatic renewal:

```
$ dokku letsencrypt:enable analysis
=====> Let's Encrypt analysis... [lots of output]
$ dokku letsencrypt:cron-job --add
```

Traffic is automatically rerouted to HTTPS.
Visit [https://api.sdgindex.org](https://api.sdgindex.org) to see.

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

### Scraping

To run all scrapers, simply run `python ./scrape.py`. Scrapers can be run in a
one-off task as described above.

## Development

We use docker-compose to run the application in development.

Buildkit needs to be enabled. This is done by setting the env var
`DOCKER_BUILDKIT` to `1`. For example, by adding `export DOCKER_BUILDKIT=1`
in `~/.bashrc`.

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
dependencies. You need to install it locally and the run `poetry install` from
within the repo. Adding and removing dependencies via `poetry add <name>` and
`poetry remove <name>`.

When adding new dependencies, the container needs to be rebuilt with
`docker-compose build api`.

### Managing migrations

The database is started automatically via docker-compose (`database`).
Migrations are automatically run when the `api` container starts.

To autogenerate or manually manage revisions, enter the `api` container:

```
$ docker-compose exec api bash
$ alembic revision --autogenerate -m "create accounts"
```

The database has a dedicated volume mounted, so the database is persisted even
when the container is destroyed/recreated.

## Testing

We use pytest to test the application. Tests are defined in the `/tests`
directory.

To run the tests, start the testing container and the testing database:

```
$ docker-compose up -d api-test database-test
```

You can then follow the test output with

```
$ docker-compose logs -f api-test
```

The container is started with `pytest-watch`, which automatically reruns all
tests when a test is modified, added, or removed.
