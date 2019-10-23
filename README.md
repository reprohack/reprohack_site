# reprohack_site

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


Reprohack django site

Install
=======

Install Django dependencies:

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