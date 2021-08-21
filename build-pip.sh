#!/bin/bash

set -ex

# remove files not under git
git clean -f -d

mkdir -p staging_dir/src/pywrap 
mkdir -p staging_dir/tests

cp *.py *.ogg *.png *.mp3 staging_dir/tests
cp pywrap/*.py staging_dir/src/pywrap
cp LICENSE.txt README.md staging_dir
cp pip-build/* staging_dir

if [[ -f build.zip ]]; then
    rm build.zip
fi
pushd staging_dir
zip  ../build.zip -r .
popd

echo "*** files in build.zip ***"
unzip -l ./build.zip

echo "*** build completed ***"

