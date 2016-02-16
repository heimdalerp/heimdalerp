from django.contrib import admin

from reversion.admin import VersionAdmin

from persons import models


class PhoneNumberAdmin(VersionAdmin):
    pass


class ExtraEmailAddressAdmin(VersionAdmin):
    pass


class PhysicalAddressAdmin(VersionAdmin):
    pass


admin.site.register(models.PhoneNumber, PhoneNumberAdmin)
admin.site.register(models.ExtraEmailAddress, ExtraEmailAddressAdmin)
admin.site.register(models.PhysicalAddress, PhysicalAddressAdmin)

