# Invoicer

## Installation

Install `brew` by `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` (if not already installed)

Install `Python` by  `brew install python`

And finally install this tool by `pip install invoicer`

## Usage

1) Create a new directory

2) Inside this directory create `base.yaml` file, `IN` file and add a picture with your signature.

3) Write records for the last month to the `IN` file and run `invoicer -r` command.

4) When you send an invoice run `invoicer -s NUMBER`.

5) After an invoice has been paid run `invoicer -p NUMBER`. 

## Publish to PYPI

1) Register on `https://pypi.python.org/`)

2) Register new project: `python setup.py register`

3) Upload new build: run `./release.sh`
(clean `rm -Rf dist`, then create a build `./setup.py sdist` and finally upload it `twine upload dist/*`)
