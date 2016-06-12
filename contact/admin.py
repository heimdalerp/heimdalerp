from django.contrib import admin
from reversion.admin import VersionAdmin

from contact import models


@admin.register(models.Contact)
class ContactAdmin(VersionAdmin):
    pass
