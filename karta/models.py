from django.db import models
from django.urls import reverse
from datetime import date
import json

def format_boolean(bool):
    """
    Formatiert einen boolean als Ja/Nein/Unbekannt
    :param bool: ein Boolean, oder None (für Unbekannt)
    """
    if bool is None:
        return "Unbekannt"
    if bool:
        return "Ja"
    else:
        return "Nein"

class NameClass(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Zweck(NameClass):
    beschreibung = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Zwecke'


class Ablageort(NameClass):
    class Meta:
        verbose_name_plural = 'Ablageorte'


class Verlag(NameClass):
    class Meta:
        verbose_name_plural = 'Verlage'


class Land(NameClass):
    class Meta:
        verbose_name_plural = 'Länder'


class Gebiet(NameClass):
    laender = models.ManyToManyField(Land, blank=True, related_name='gebiete')

    class Meta:
        verbose_name_plural = 'Gebiete'


class Karte(models.Model):
    name = models.CharField(max_length=150)
    zwecke = models.ManyToManyField(Zweck)
    ablageort = models.ForeignKey(Ablageort, null=True, on_delete=models.PROTECT)
    reihenfolge = models.FloatField(null=True)
    # Eine Karte stellt ihre Gebiete mehr oder weniger vollständig dar
    gebiete = models.ManyToManyField(Gebiet, related_name='karten')
    # laender enthaelt alle Laender, von denen die Karte Teile darstellt.
    laender = models.ManyToManyField(Land, related_name='karten_in_land')
    verlag = models.ForeignKey(Verlag, null=True, blank=True, on_delete=models.PROTECT)
    stand = models.DateField(blank=True, null=True)
    hinzugefuegt = models.DateField(default=date.today, blank=True, null=True)
    preis = models.FloatField(blank=True, null=True)
    bemerkung = models.CharField(max_length=500, blank=True)
    hat_ortsverzeichnis = models.BooleanField(default=False)
    hat_hoehenlinien = models.BooleanField(default=False, null=True)
    hat_gps = models.BooleanField(default=False, null=True)
    hat_huelle = models.BooleanField(default=False)
    zustand = models.CharField(max_length=1, default='N', choices=[('N', 'Neu'),
                                                                   ('A', 'Alt')])

    def list_information(self):
        return {
            "Verlag": self.verlag,
            "Preis": 'Unbekannt' if self.preis is None else f"{self.preis:.2f}€",
            "Stand": self.stand or 'Unbekannt',
            "Hinzugefügt am": self.hinzugefuegt or 'Unbekannt',
            "Ortsverzeichnis": format_boolean(self.hat_ortsverzeichnis),
            "Höhenlinien": format_boolean(self.hat_hoehenlinien),
            "GPS-Support": format_boolean(self.hat_gps),
            "Hülle": format_boolean(self.hat_huelle),
            "Zustand": {'N': 'Neu', 'A': 'Alt'}[self.zustand],
            "Bemerkung": self.bemerkung
        }

    def geojson_set(self):
        # Menge von GeoJSON-Features nach RFC 7946, die alle Ansichten der Karte beschreiben
        ansichten = self.ansicht_set.all()
        returnset = []
        for ansicht in ansichten:
            if not ansicht.koords_json:
                continue
            feature = {"type": "Feature",
                       "properties": {
                           "karte": self.name,
                           "pk": ansicht.pk,
                           "karte_pk": self.pk,
                           "href": reverse('karte-detail', args=(self.pk,)),
                           "description": ansicht.kurzbeschreibung,
                           "massstab": ansicht.massstab_f
                       },
                       "geometry": {
                           "type": "Polygon",
                           "coordinates": [ansicht.koords]
                       }}
            returnset.append(feature)
        return returnset

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Karten'
        ordering = ['reihenfolge']


class Ansicht(models.Model):
    """Eine Karte ist **eine,** physische Karte. Eine Ansicht ist eine "Teilkarte" einer Karte."""
    karte = models.ForeignKey(Karte, on_delete=models.CASCADE)
    massstab = models.IntegerField(blank=True, null=True)
    koords_json = models.CharField(max_length=1000, blank=True, null=True)
    kurzbeschreibung = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "{} - Ansicht von {}".format(self.kurzbeschreibung, self.karte.name)

    @property
    def massstab_f(self):
        if self.massstab:
            return f"1:{self.massstab}"
        return "Unbekannt"
    # koords ist eine Liste von Koordinaten. Koordinaten sind wiederum eine Liste der Form [lon, lat]
    # ! Zuerst der Längengrad (Ost/West) dann der Breitengrad (Nord/Süd)
    @property
    def koords(self):
        try:
            return json.loads(self.koords_json)
        except TypeError:
            return []

    @koords.setter
    def koords(self, newcoords):
        self.koords_json = json.dumps(newcoords)

    class Meta:
        verbose_name_plural = 'Ansichten'
