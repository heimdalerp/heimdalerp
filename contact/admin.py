from contact import models
from django.contrib import admin
from reversion.admin import VersionAdmin


@admin.register(models.Contact)
class ContactAdmin(VersionAdmin):
    pass
