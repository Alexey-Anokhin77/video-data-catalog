# FastAPI Video data catalog

## Develop

Check GH Action after any push.

### Setup:

Right click `v-data-catalog` -> Mark directory as -> Sources root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install dependencies

Install all packages:
```shell
uv sync
```

### Run

Go to workdir:
```shell
cd v-data-catalog
```

Run dev server:
```shell
fastapi dev
```

## Snippets
```shell
python -c "import secrets;print(secrets.token_urlsafe(16))"
```
