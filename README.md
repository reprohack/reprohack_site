# Reprohack (Django) web site
# reprohack_site

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

Set development environment
===========================

We use [Docker Compose](https://docs.docker.com/compose/)
to provide you with a few steps to have your development environment
up and running:

```{bash}
$ docker-compose up
```

Visit http://localhost:8000/ to see your development website.

Note: If you are using docker with docker-machine you need to add vm's ip adress to `ALLOWED_HOSTS` in Django setting. You can do it by following the steps:
1. Find out the ip address of your vm: `docker-machine env <default>`; replace <default> with name of the vm used for docker-machine.
2. Before builidng the Docker image, edit `mysite/settings.py` by adding the ip address to `ALLOWED_HOSTS` list.
3. Proceed as instructed above.

If this is your first time,
you need to create the database:

```{bash}
$ docker-compose exec django python manage.py migrate
```

And you can create a super-user for the admin:

```{bash}
$ docker-compose exec django python manage.py createsuperuser
```

Docker Compose will bind your local files to the container
and
Django will restart the server when it detects change in the files.

Use
===

The map can be edited from the AdminSite at ``/admin``.

Host Your Own
=============

Note: When hosting the page on the internet, you will need to add the `hostname` to the Django settings.
Edit `mysite/settings.py` by adding the `hostname`  to `ALLOWED_HOSTS` list.

***

Please note that the 'reprohack_site' project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By contributing to this project, you agree to abide by its terms.

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
