# micro-mart

## Required packages

- `nox`
- `nox-poetry`

## Getting started
You need `nox` and `nox-poetry` in your system python environment. I recommend using pyenv to manage your python environments.

- `docker compose up`
- Open the Redpanda console: localhost:8080
- Add the following topics:
    - `retail-service.product`

After you update a microservice's dependencies, run `poetry update` in the root directory to update poetry for nox.
