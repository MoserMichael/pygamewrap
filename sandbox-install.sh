#!/bin/bash

# test installation of module in virtual environment
virtualenv my-pywrap-venv
source my-pywrap-venv/bin/activate

pip3 install PygameWrap
deactivate


