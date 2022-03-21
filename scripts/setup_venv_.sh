#!/bin/bash

module load python/3.7

cd $HOME/syde-750

virtualenv --no-download env_derl
source env_derl/bin/activate
pip install --no-index --upgrade pip
pip install --no-index Pillow numpy Cython imageio glfw cffi fasteners
pip install --no-deps mujoco_py==2.0.2.8
pip install --no-index pyyaml lxml
pip install --no-index gym==0.17.1
pip install --no-index networkx
pip install --no-index typing-extensions

cd $HOME/syde-750/derl
pip install -e .

export PYTHONUNBUFFERED=1