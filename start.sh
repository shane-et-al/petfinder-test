#!/bin/sh
mkdir -p ./pf-img
nohup nice pipenv run python pf-img.py &
