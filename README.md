# info

Command line tool to search my info

## Setup

```sh
# Install UV
brew install uv

# This will create the .venv directory
uv sync

## Dev Env
printf "INFOLIST_DATA=./infolist-dev.yaml\n" >> .env

# Activate the environment
source .venv/bin/activate
source .env
```

## Dev

```sh
python3 -m infolist.main
```

## Dist

Python wheel

```sh
source .venv/bin/activate # if not done already

# build for dist
uv build
```

## As a User

To use `infolist`, as opposed to develop `infolist` then do the following:

```sh
# In a new terminal window not in this venv
pip3 install ~/github/tonygilkerson/infolist/dist/infolist-0.1.7-py3-none-any.whl --user --break-system-packages

# Verify
infolist --version

```

## Dagger

```sh
dacongger -m github.com/act3-ai/dagger/python@v0.1.4 call --src="." --netrc=env:NETRC mypy
`   `