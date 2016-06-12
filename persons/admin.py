from django.contrib import admin
from reversion.admin import VersionAdmin

from persons import models


@admin.register(models.PhysicalAddress)
class PhysicalAddressAdmin(VersionAdmin):
    pass


@admin.register(models.Company)
class CompanyAdmin(VersionAdmin):
    pass
