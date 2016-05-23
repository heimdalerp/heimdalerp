from django.db import models
from django.utils.translation import ugettext_lazy as _

from persons.models import PersonProfile

CONTACT_TYPE_COMPANY = 'C'
CONTACT_TYPE_INDIVIDUAL = 'I'
CONTACT_TYPES = (
    (CONTACT_TYPE_COMPANY, _('Company')),
    (CONTACT_TYPE_INDIVIDUAL, _('Individual')),
)


class Contact(PersonProfile):
    """
    Contacts may be clients or vendors, and these may also be individuals
    or companies.
    """
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True
    )
    contact_type = models.CharField(
        _('contact type'),
        max_length=1,
        choices=CONTACT_TYPES,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        default_permissions = ('view', 'add', 'change', 'delete')
