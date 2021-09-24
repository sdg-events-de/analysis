FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# From https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-216865
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
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.9 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Copy poetry version file
COPY poetry.lock pyproject.toml ./

# Export to requirements.txt
# pip can't handle vcs & editable dependencies when requiring hashes (https://github.com/pypa/pip/issues/4995)
# poetry exports local dependencies as editable by default (https://github.com/python-poetry/poetry/issues/897)
RUN poetry export -f "requirements.txt" --without-hashes --with-credentials > requirements.txt.orig
RUN sed -e 's/^-e //' < "requirements.txt.orig" > "requirements.txt" && rm "requirements.txt.orig"

# Read python version
RUN PYTHON_RUNTIME_VERSION="$(sed -n -e '/^\[metadata\]/,/^\[/p' poetry.lock | sed -n -e 's/^python-versions\s*=\s*//p' | tr -d \"\')"
RUN echo "python-$PYTHON_RUN_TIME_VERSION" > runtime.txt

# Copy /api to /app (that's where fastapi expects our entrypoint)
COPY ./api /app
