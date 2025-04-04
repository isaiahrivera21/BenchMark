FROM python:3.11-bookworm

ENV PYTHONPATH=/code

RUN pip install --no-cache "poetry>=1.8,<1.9" 
RUN poetry config virtualenvs.create false


RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock* ./


RUN poetry install --only main --no-interaction --no-ansi --no-root -vv \
    && rm -rf /root/.cache/pypoetry

