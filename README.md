Uo# FastAPI Video data catalog

## Develop

### Setup:

Right click `v-data-catalog` -> Mark directory as -> Sources root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
uv install
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