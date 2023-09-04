FROM python:3.11.4-slim as base

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY src ./src/
COPY pyproject.toml ./

EXPOSE 8000

# Develop
FROM base as development

COPY --from=base / /
COPY start.dev.sh ./
RUN true
ENV PYTHONASYNCIODEBUG 1

RUN poetry install --no-root --no-interaction --no-ansi

RUN useradd -rm -d /home/mm -s /bin/bash -g root -G sudo -u 1000 mm
USER mm

ENTRYPOINT ["sh", "/app/start.dev.sh"]

# Production
FROM base as production
COPY --from=base / /

RUN poetry install --no-dev --no-root --no-interaction --no-ansi

WORKDIR src
ENTRYPOINT ["gunicorn"]
