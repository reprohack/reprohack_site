# Reprohack Hub web site (Django)

ReproHacks are reproducibilty hackathons where participants attempt to reproduce research papers from published code and data.  This [Django](https://www.djangoproject.com/)-powered site is for coordinating ReproHacks.

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Running a development version of the site using Docker/docker-compose

We use [Docker Compose](https://docs.docker.com/compose/)
to provide you with a few steps to have your development environment
up and running:

```{bash}
$ cd path/to/clone/of/this/repo
$ docker-compose -f local.yml up
```

Then visit [http://localhost:8000/](http://localhost:8000/) to see your development website.

Note: If you are using Docker with [Docker Machine](https://docs.docker.com/machine/)
you need to add the VM's IP address to `ALLOWED_HOSTS` in Django's setting.
You can do it by following the steps:

1. Find out the IP address of your VM: `docker-machine env <default>`; replace `<default>` with name of the VM used for docker-machine.
1. Before building the Docker image, edit `mysite/settings.py` by adding the IP address to `ALLOWED_HOSTS` list.
1. Proceed as instructed above.

If this is your first time,
you need to create the database:

```sh
$ docker-compose exec django python manage.py migrate
```

And you can create a super-user for site administration:

```sh
$ docker-compose exec django python manage.py createsuperuser
```

Docker Compose will bind your local files to the container and
Django will restart the server when it detects change in the files.

## Settings

See [settings](https://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Site management

### Setting Up Your Users

To create a **normal user account**,
just go to *Sign Up* and fill out the form.
Once you submit it, you'll see a *Verify Your E-mail Address* page.
Go to your console to see a simulated email verification message.
Copy the link into your browser.
Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command:

```sh
$ python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Misc management

The map can be edited from the AdminSite at ``/admin``.


Host Your Own
=============

Note: When hosting the page on the internet, you will need to add the `hostname` to the Django settings.
Edit `mysite/settings.py` by adding the `hostname`  to `ALLOWED_HOSTS` list.

## Contribution guidelines

### Code of Conduct

Please note that this 'reprohack_site' project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By contributing to this project, you agree to abide by its terms.

### Type checking

Running type checks with [mypy](https://mypy.readthedocs.io/en/stable/):

```sh
$ mypy reprohack_hub
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```sh
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html
```

Running tests with pytest:

```sh
$ pytest
```

### Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Celery

This app comes with [Celery](https://docs.celeryproject.org/en/stable/index.html).

To run a celery worker:

```sh
$ cd path/to/clone/of/this/repo
$ celery -A config.celery_app worker -l info
```

NB for Celery's import magic to work, it is important *where* the celery commands are run. 
If you are in the same folder with `manage.py`, you should be right.

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. 
For that reason a local SMTP server, [MailHog](https://github.com/mailhog/MailHog)_ (with a web interface)
is available as Docker container.

The Mailhog container will start automatically when you will run all Docker containers.
Please check the `cookiecutter-django` Docker documentation for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to [http://127.0.0.1:8025](http://127.0.0.1:8025)


## Deployment

### Docker

See detailed `cookiecutter-django Docker documentation`_.
