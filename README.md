# reprohack_site

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


Reprohack django site

Install
=======

The site requires System Library `GDAL` to map event locations. See [installation instructions](https://gdal.org/download.html).

Once `GDAL` is installed, install Django dependencies:

```{bash}
pip install -r requirements.txt
```

Initialize database tables:

```{bash}
python manage.py migrate
```

Create a super-user for the admin:

```{bash}
python manage.py createsuperuser
```

Run
===

```{bash}
python manage.py runserver
```

The map visible on http://127.0.0.1:8000/ can be edited from the AdminSite at ``/admin``.

Docker
======

This project also has support for docker. In order to run with docker you must first have docker installed.

NOTE: Docker support is in beta as does not yet support volumes (persistent data) so all data will erase

To build docker container:
```{bash}
docker build -t reprohack .
```

To run image built in previous step:
```{bash}
docker run -it -p 8000:8000 -v <folder-on-local-machiene>:/data reprohack
```

***

Please note that the 'reprohack_site' project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By contributing to this project, you agree to abide by its terms.

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
