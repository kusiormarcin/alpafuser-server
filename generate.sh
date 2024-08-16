#!/bin/bash

CURRENT_PATH=$(dirname "$0")
VENV_PATH="$CURRENT_PATH/.venv"

python -m venv "$VENV_PATH"

source "$VENV_PATH/bin/activate"

python $CURRENT_PATH/generate.py "$1"