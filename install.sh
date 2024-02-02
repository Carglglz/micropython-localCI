#!/usr/bin/bash

echo "cloning MicroPython ..."
git clone https://github.com/micropython/micropython.git ../micropython_CI
echo "done"

echo "Installing git hooks..."
cp ./git_hooks/* ../micropython_CI/.git/hooks/
echo "done"

echo "Updating MicroPython CI server info"
GIT_DIR="../micropython_CI/.git" git --bare update-server-info
GIT_DIR="../micropython_CI/.git" git config --local receive.denyCurrentBranch ignore 
echo "done"

echo "Installing default .env"
cp .env ../micropython_CI/
echo "done"

echo "Installing requirements..."
pip3 install -r requirements.txt
echo "done"
