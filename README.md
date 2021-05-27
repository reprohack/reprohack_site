# Reprohack website

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

## Overview

The Reprohack app is built using django webapp framework.

## Development and testing
The following are instructions for running the app on your local machine for testing or development.


### Dependencies

The project uses a combination of python and javascript libraries. [pip](https://pypi.org/) can be used to install all python related 
packages and [node/npm](https://nodejs.org) can be used to install javascript packages.

### Installation (using conda)
Use of conda is recommended as it is able to install all dependencies including nodejs. [A minimal version of 
conda can be obtained from here](https://docs.conda.io/en/latest/miniconda.html).

Once `conda` is installed, the installation steps are as follows:

```
# Create a conda environment called 'reprohack'
conda create -n reprohack python=3.8

# Activate environment
source activate reprohack

# Install nodejs from conda-forge
conda install -c conda-forge nodejs

# Install python dependencies
pip install -r requirements/local.txt

# Install node dependencies
npm install
```

#### The conda environment must be activated every session
The conda environment must be re-activate after every session, e.g. when you open a new terminal. The following 
line of code must be run again to re-activate your conda environment:

```
source activate reprohack
```

### Configuration (`secret.py`): IMPORTANT!

You must create a 'secret' python settings file for storing information that should not be public at:

```
config/settings/secret.py
```

The default values of these settings are located at `config/settings/secret_default.py`.


### Running the development server

Run the development server with the following command:

```bash
npm run serve
```

The app can then be accessed from `http://127.0.0.1:8000`. The app uses the `config.settings.local` config by default.


#### Running processes separately

The `npm run serve` runs two commands in parallel:

* `npm run serve:site` - Runs the django's development serve`
* `npm run serve:assets` - Monitors and builds javascript and scss assets with gulp

It may be useful to only run `npm run serve:assets` on its own while running the django app through an IDE of
your choice for debugging.

Run `npm run` to see the full list of commands.

### Creating normal users
To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll 
see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. 
Copy the link into your browser. Now the user's email should be verified and ready to go.
 

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on 
Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Creating a superuser

To create an **superuser account**, use this command 

```bash
python manage.py createsuperuser
```

Only the superuser is allowed to log into the admin panel (see next section).

### Admin panel

The admin panel can be access at `/admin` e.g. for the local development server `http://127.0.0.1:8000/admin`.

The panel can be used to browse and edit your database.  


### Testing

The `pytest` library is used for testing. Run the following command:

```
npm run test
```

#### Type checks
**Is this useful?**
Running type checks with mypy:

```bash
mypy reprohack_hub
```

#### Test coverage
**Is this useful?**
To run the tests, check your test coverage, and generate an HTML coverage report

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```


## Deployment: Pythonanywhere
The following are steps for deploying on python anywhere.

* App setting is located at `config/settings/pythonanywhere.py`

### Installation: Python anywhere

**Instructions for installing a FRESH copy of the app on pythonanywhere.**

#### On Pythonanywhere web GUI: Creating a web app

* Log in to pythonanywhere
* Go to the `Web` section
* Click on `Add a new web app`
* Select Manual app
* On the web app configuration page, set:
  * Source code `/home/reprohacks/reprohack_site`
  * Working directory `/home/reprohacks/reprohack_site`
  * WSGI Configuraiton file, click on the link and set according to the next section
  * Virtualenv `/home/reprohacks/reprohack_site/.virtualenv`
  * Static files set URL as `/static/` and directory `/home/reprohacks/reprohack_site/`
* Set up the database by clicking on the `Databases` section
  * Press `create database`
  * You'll need to set a password
  * Create a database named `reprohack`
  

#### On Pythonanywhere web GUI: Setting up WSGI file for the webapp

```python
import os
import sys

# add your project directory to the sys.path
project_home = '/home/reprohacks/reprohack_site'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'


# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Installing the app from github repository

Python anywhere already comes with `Python 3.8` installed, so we can use virtualenv instead. Installation of node
on the server is not as javascript dependencies are copied to django's static folder and is tracked through version 
control.

Access pythonanywhere's bash console or ssh into pythonanywhere, then run the following: 

```bash
# Make sure we're in the home folder
cd ~

# Clone the app from the repository
git pull https://github.com/reprohack/reprohack_site.git

# Go into the folder
cd reprohack_site

# Create a virtual python environment using python 3.8
python -m virtualenv --python=/usr/bin/python3.8  .virtualenv

# Activate the virtual environment
source .virtualenv/bin/activate

# Install python dependencies
pip install requirements/production.txt
```

You will then need to create a secrets setting file at `config/settings/secret.py`, copy the 
contents of `config/settings/secret_default.py` and use that as the basis. Add the settings such as `MYSQL_USERNAME`,
`MYSQL_PASSWORD` etc. to the `secret.py`.

Once all the above has been set up, we then need to build a 
```
# Build the database (
./manage.py migrate

# Collect the static assets into /staticfiles folder
./manage.py collectstatic
```


## Host Your Own

Note: When hosting the page on the internet, you will need to add the `hostname` to the Django settings.
Edit `mysite/settings.py` by adding the `hostname`  to `ALLOWED_HOSTS` list.

***

Please note that the 'reprohack_site' project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By contributing to this project, you agree to abide by its terms.

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
