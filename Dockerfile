FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Adapted from https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-216865
# python
ENV PYTHONUNBUFFERED=1 \
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


# Prepare venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install poetry - respects $POETRY_VERSION, etc...
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR /app
COPY poetry.lock pyproject.toml ./

# install runtime deps
RUN poetry install

# Set up the app (this is where the image expects files)
COPY ./ /app

# Set the FastAPI entry point (api.py with variable api)
ENV MODULE_NAME=api \
    VARIABLE_NAME=api
