# Getting started

## Debian
apt-get install libfreetype6-dev libjpeg-dev zlib1g-dev libpng12-dev libxft-dev libjpeg62

## virtualenv

    $ pip install --user --upgrade virtualenv                                                      
    $ virtualenv -p python3 env 
    $ source env/bin/activate
    $ pip install -r REQUIREMENTS.txt

### Check if virtualenv is active

    $ printenv | grep VIRTUAL_ENV

### Deactivate virtualenv

    $ deactivate

## FAQ

### I get "The _imaging C module is not installed"!

Install the latest Pillow version (you installed the above packages, right?):

    $ pip install git+git://github.com/python-imaging/Pillow.git --upgrade

### Which Python version is needed?

Python >= 3.
