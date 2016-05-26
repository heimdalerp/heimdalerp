from django.contrib import admin
from reversion.admin import VersionAdmin

from persons import models


class PhysicalAddressAdmin(VersionAdmin):
    pass


class CompanyAdmin(VersionAdmin):
    pass


admin.site.register(models.PhysicalAddress, PhysicalAddressAdmin)
admin.site.register(models.Company, CompanyAdmin)
