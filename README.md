# info

Command line tool to search my info

## Setup

```sh
# Install UV
brew install uv

# This will create the .venv directory
uv sync

# Activate the environment
source .venv/bin/activate

# Should run automatically
direnv allow 
```

## Dev

```sh
# python -m infolist.main
uv run infolist
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
pip3 install ~/github/tonygilkerson/infolist/dist/infolist-0.1.9-py3-none-any.whl --user --break-system-packages

# Verify
infolist --version

```