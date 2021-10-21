#!/bin/bash

set -e 

rm -rf tst || true
mkdir tst
pushd tst
# test installation of module in virtual environment
virtualenv my-venv
source my-venv/bin/activate

cp ../*.py ../*.png ../*.ogg ../*.mp3 .       
pip3 install pygamewrap

python3 12-add-animated-sprite.py

echo "everything is fine. test passed"

deactivate

rm -rf my-venv

popd tst
