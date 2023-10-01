FROM python:3.11-slim

# Configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV
RUN $POETRY_VENV/bin/pip install -U pip setuptools
RUN $POETRY_VENV/bin/pip install -U pip setuptools
RUN $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"


WORKDIR /usr/src/chugunapp


# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install


# Copy Application
COPY . .

EXPOSE 7000
EXPOSE 5432

CMD [ "poetry", "run", "python", "-c", "print('Hello, World!')" ]
