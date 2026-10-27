#!/bin/bash
# Run RobotControl.py with the project venv (sudo needed for xboxdrv)
cd "$(dirname "$(readlink -f "$0")")" || exit 1
sudo venv/bin/python RobotControl.py "$@"
