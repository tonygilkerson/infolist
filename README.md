# info

Command line tool to search my info

## Setup

```sh
mkdir .venv

python3 -m venv .venv
source .venv/bin/activate
pip install poetry



## Dev Env
printf "INFOLIST_DATA=./infolist-dev.yaml\n" >> .env

# Install project dependencies
# see: https://python-poetry.org/docs/basic-usage/
poetry install

# If you want to install the dependencies only, run the install command with the --no-root flag:
poetry install --no-root
```

## Dev

```sh
python3 -m src.main
```

## Dist

Python wheel

```sh
# dev install to see if it works
poetry build
poetry install
infolist

# Actual install 
poetry build

# install the whl
pip3 install /Users/tonygilkerson/github/tonygilkerson/infolist/dist/infolist-0.1.1-py3-none-any.whl --force-reinstall
```

## As a User

To use `infolist`, as opposed to develope `infolist` then do the following:

```sh

# You need to be in this project and the python venv active

# Make sure the latest release is installed
pip3 install /Users/tonygilkerson/github/tonygilkerson/infolist/dist/infolist-0.1.1-py3-none-any.whl --force-reinstall

# run the app by calling it directly
export INFOLIST_DATA=~/infolist-data.yaml
infolist
```