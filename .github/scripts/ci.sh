#!/usr/bin/env bash
# Run from the GitHub Actions workspace; dependencies are checked out by ci.yml.
set -eo pipefail
source /opt/ros/lyrical/setup.bash

for package in rpp_common rpp_plugin_registrator rpp_orchestrator rpp_py rpp_cli rpp_testing; do
  python -m pip install --no-deps -e "rpp_dev/src/$package"
done
python -m pip install "casadi>=3.5.5" numpy matplotlib
python -m pip install --no-deps -e libraries/more_common

python -m pytest libraries/more_common/tests
