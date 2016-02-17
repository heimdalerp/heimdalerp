from django.db import models
from django.conf import settings

from heimdalerp.persons.models import PersonProfile, GENRE_TYPES


class Employee(PersonProfile):
    """
    All Employees must have a User, whereas they'll use the system or not.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user')
    )
    genre = models.CharField(
        _('genre'),
        max_length=1,
        choices=GENRE_TYPES,
    )
    member_since = models.DateField(
        _('member_since'),
        blank=True,
        null=True
    )

