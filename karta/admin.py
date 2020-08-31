from django.contrib import admin
from .models import *

class AnsichtInline(admin.TabularInline):
    model = Ansicht
    extra = 1

@admin.register(Karte)
class KarteAdmin(admin.ModelAdmin):
    inlines = [AnsichtInline]
    def verlag_name(self, karte):
        verlag = karte.verlag
        if verlag:
            return karte.verlag.name
        return ''
    def ablage_name(self, karte):
        return karte.ablageort.name
    def gebiete_namen(self, karte):
        ge = karte.gebiete.all()
        if not ge:
            return ''
        return ', '.join(g.name for g in ge[:3])

    list_display = ('reihenfolge','name','gebiete_namen','verlag_name','ablage_name','bemerkung')
    list_display_links = ('name',)
    list_editable = ('reihenfolge',)
    list_per_page = 200
    search_fields = ['name','gebiete__name']

    fieldsets = [
        (None,{'fields': ('name','zwecke','ablageort')}),
        ('Geographie', {'fields': ('gebiete','laender')}),
        ('Eigenschaften',{'fields': (('verlag','preis'),
                                     ('stand','hinzugefuegt'),
                                     ('hat_ortsverzeichnis','hat_hoehenlinien','hat_gps','hat_huelle'),
                                     ('zustand','bemerkung'))})
    ]
    filter_horizontal = ['gebiete','laender']

class KarteInline(admin.StackedInline):
    model = Karte
    extra = 0
    fields = ('name','zwecke','gebiete','preis','stand','hinzugefuegt','bemerkung')

@admin.register(Verlag)
class VerlagAdmin(admin.ModelAdmin):
    inlines = [KarteInline]

@admin.register(Gebiet)
class GebietAdmin(admin.ModelAdmin):
    pass

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    pass

@admin.register(Zweck)
class ZweckAdmin(admin.ModelAdmin):
    pass

@admin.register(Ablageort)
class AblageortAdmin(admin.ModelAdmin):
    pass
