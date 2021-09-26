FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as base

# Adapted from https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-216865
ENV \
    # Set the FastAPI entry point (api.py with variable api)
    MODULE_NAME=api \
    VARIABLE_NAME=api \
    \
    # python
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # python venv
    VIRTUAL_ENV="/venv" \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.9 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

# Set up path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# Create non-root user
ENV UNAME=user
RUN useradd -m -u 1000 -o -s /bin/bash $UNAME
RUN mkdir -p $POETRY_HOME $VIRTUAL_ENV
RUN chown $UNAME $POETRY_HOME $VIRTUAL_ENV /app
USER $UNAME

# Create virtual environment
RUN python -m venv $VIRTUAL_ENV

# Copy poetry.lock and pyproject.toml
WORKDIR /app
COPY poetry.lock pyproject.toml ./

FROM base as builder

# Install poetry - respects $POETRY_VERSION, etc...
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# `development` image is used during development / testing
FROM base as development
ENV FASTAPI_ENV=development

# copy in our built poetry + venv
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# quicker install as runtime deps are already installed
WORKDIR /app
RUN poetry install

CMD ["/start-reload.sh"]

# `production` image used for runtime
FROM base as production
ENV FASTAPI_ENV=production
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
WORKDIR /app
COPY ./app /.


