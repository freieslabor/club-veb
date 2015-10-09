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

## FAQ & issues

### Which Python version is needed?

Python >= 3.

### I get "The _imaging C module is not installed"!

Install the latest Pillow version (you installed the above packages, right?):

    $ pip install git+git://github.com/python-imaging/Pillow.git --upgrade

### Photologue throws SyntaxErrors!

Yes, photologue uses explicit unicode literals. If you are using Python
3.0/3.1/3.2 you have to patch photologue (10 occurrences, search for "u'").
Python 3.3 reintroduced explicit unicode literals, see
[PEP 414](https://www.python.org/dev/peps/pep-0414/).
