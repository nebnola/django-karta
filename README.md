Karta is a small django app I wrote to keep track of the maps I have.
A database can store information such as the age of the map, its features
(e.g. contour lines, coordinate grid) and, most importantly, the area it covers.
Maps are displayed on an interactive leaflet map so you can pick the a map that
covers your area of interest.

## Dependencies

* Python 3.8
* Django 3.1

It probably works with other versions too but I didn't test that.

## Installation

* Either use an existing project, or create a new one: `django-admin startproject
myproject`
* Clone this repository and make the `karta` directory available from your project
(One possible way would be to have `import sys; sys.path.append('path/to/django-karta')`
in `myproject/settings.py`).
* Add karta to your project's `INSTALLED_APPS`:

```python
# myproject/settings.py

...

INSTALLED_APPS=[
    ...,
    'karta.apps.KartaConfig',
    ...
]
```

* Include karta's URLs in your project:

```python
# myproject/urls.py

from django.urls import include, path

...

urlpatterns = [
    ...,
    path('path/to/karta/', include('karta.urls')),
    ...
]
```

* [Download](https://leafletjs.com/download.html) `leaflet.js` and `leaflet.css`
and place them under `karta/static/karta/leaflet`. This is necessary to make the interactive map work.

* Apply necessary migrations to your database: `python manage.py migrate`

* If this is a new project, you'll want to create a superuser account so you can
use the admin functionality to add and edit maps: `python manage.py createsuperuser`

* Try it out! `python manage.py runserver` and visit `127.0.0.1:8000` in your browser