from django.contrib import admin
from reversion.admin import VersionAdmin

from geo import models


@admin.register(models.AlternativeName)
class AlternativeNameAdmin(VersionAdmin):
    pass


@admin.register(models.Country)
class CountryAdmin(VersionAdmin):
    pass


@admin.register(models.Region)
class RegionAdmin(VersionAdmin):
    pass


@admin.register(models.Locality)
class LocalityAdmin(VersionAdmin):
    pass
