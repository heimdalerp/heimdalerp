from django.contrib import admin
from reversion.admin import VersionAdmin

from contact import models


class ContactAdmin(VersionAdmin):
    pass


admin.site.register(models.Contact, ContactAdmin)
