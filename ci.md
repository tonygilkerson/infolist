# Dagger Python CI

This notebook will help run Dagger CI for your python project.

## Setup

Before you get starte you will need to

* Install Docker
* Install Dagger
* Install the Runme extension

## Getting Started

Verify that Runme and Dagger are working by running the following cell

```sh
dagger core container \
    from --address="busybox" \
    with-exec --args="echo","Hello World" \
    stdout
```

Verify that this notebook has access to your environment variables

```sh
source .env
dagger core container \
    from --address="busybox" \
    with-exec --args="echo","TESTVAR contains: $TESTVAR" \
    stdout
```

### Python CI

The ACT3 Dagger module used for python CI is `github.com/act3-ai/dagger/python`.  For detail help use the `--help` flag or run the cell below. A web version of the help is also mirrored in the [daggerverse](https://daggerverse.dev/mod/github.com/act3-ai/dagger/python)

```sh
dagger call -m github.com/act3-ai/dagger/python@v0.1.4 --src "." --help
```

#### Lint

The `lint` function will execute the following

* ruff-check
* ruff-format
* mypy
* pylint
* pyright

For detail help run `lint --help`

```sh
dagger call -m github.com/act3-ai/dagger/python@v0.1.4 --src "." lint --help
```

Run `lint` on this project to see how you are doing!

```sh {"terminalRows":"37"}
dagger call -m github.com/act3-ai/dagger/python@v0.1.4 --src "." lint
```

#### Check

Check

```sh {"terminalRows":"16"}
dagger -m github.com/act3-ai/dagger/release call --src="." python check
```