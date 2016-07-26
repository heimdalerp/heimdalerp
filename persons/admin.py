from django.contrib import admin
from persons import models
from reversion.admin import VersionAdmin


@admin.register(models.PhysicalAddress)
class PhysicalAddressAdmin(VersionAdmin):
    pass


@admin.register(models.Company)
class CompanyAdmin(VersionAdmin):
    pass
