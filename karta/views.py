import json
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Karte, Ablageort

def index_view(request):
    ablagen={a.name: Karte.objects.filter(ablageort=a).all() for a in Ablageort.objects.all()}
    context={'ablagen': ablagen,
             'karte':{'pk':None}}
    # Der key 'karte' ist notwendig, damit im template kartenliste.html (was in index.html included ist)
    # karte.pk existiert
    return render(request, template_name='karta/index.html', context=context)

def allgeojson(request):
    # basically a union of all KarteGeoViews
    featureset = []
    for karte in Karte.objects.all():
        featureset += karte.geojson_set()
    return HttpResponse(json.dumps(featureset))


class KartenView(generic.DetailView):
    model = Karte
    template_name = 'karta/karte.html'
    context_object_name = 'karte'

    def get_context_data(self, **kwargs):
        context = super(KartenView, self).get_context_data(**kwargs)
        ablage_id = context['karte'].ablageort_id
        context['surrounding'] = Karte.objects.filter(ablageort_id= ablage_id).all()
        return context

class KarteGeoView(generic.DetailView):
    model = Karte
    def get(self, request, *args, **kwargs):
        karte = self.get_object()
        returnset = karte.geojson_set()
        return HttpResponse(json.dumps(returnset))