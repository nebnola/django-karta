from django.urls import path
from . import views

urlpatterns=[
    path('', views.index_view),
    path('karte/<int:pk>', views.KartenView.as_view(), name='karte-detail'),
    path('karte/<int:pk>/geo.json', views.KarteGeoView.as_view(), name='karte-geojson'),
    path('allgeo.json', views.allgeojson, name='all-geojson')
]