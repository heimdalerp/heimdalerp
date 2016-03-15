from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugetttext_noop as _noop

from persons.models import Company


class Ledger(models.Model):
    """
    Ledger is the collection of all accounts used by a company.
    Here the grouping of accounts is performed.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='ledgers',
        related_query_name='ledger',
        db_index=True
    )
    accounts = models.ManyToManyField(
        'Account',
        verbose_name=_('accounts'),
        related_name='accounts',
        related_query_name='account',
        trough='LedgerHasAccount',
        trough_fields=('ledger', 'account')
    )


class Account(models.Model):
    """
    Ledgers are organized in multiple accounts which themselves organize
    the transactions of the company.
    """
    code = models.SlugField(
        _('code'),
        max_length=50
    )
    name = models.CharField(
        _('name'),
        max_length=150
    )
    account_type = models.CharField(
    transactions = models.ManyToManyField(
        'Transaction',
        verbose_name=_('transactions'),
        related_name='+',
        related_name='account'
    )


ACCOUNT_TYPE_PERSONAL = 'P'
ACCOUNT_TYPE_REAL = 'R'
ACCOUNT_TYPE_NOMINAL = 'N'
ACCOUNT_TYPES = (
    (ACCOUNT_TYPE_PERSONAL, _('Personal')),
    (ACCOUNT_TYPE_REAL, _('Real')),
    (ACCOUNT_TYPE_NOMINAL, _('Nominal')),
)


class AccountSubType(models.Model):
    """
    Accounts have several types, the common types are:
        * Personal Accounts: DEBIT THE RECEIVER, CREDIT THE GIVER.
            - Natural persons.
            - Artificial or legal persons.
            - Groups/Representative.
        * Real Accounts: DEBIT WHAT COMES IN, CREDIT WHAT GOES OUT.
            - Tangible (cash, machinery, stock, furniture, etc).
            - Intangile (goodwill, patents, trademarks, copyrights, etc).
        * Nominal Accounts: 
          DEBIT ALL EXPENSES AND LOSSES, CREDIT ALL INCOMES AND GAINS.
          Wages, rent, comission, interest received, etc.
    """
    company = ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='account_subtypes',
        related_query_name='account_subtype',
        db_index=True
    )
    main_type = models.CharField(
        _('main type'),
        max_length=1,
        choices=ACCOUNT_TYPES,
        db_index=True
    )    
    name = models.CharField(
        _('name'),
        max_length=50
    )

    def __str__(self):
        return _noop('%(main_type)s::(%name)s') % {
            'main_type': self.main_type,
            'name': self.name
        }

    class Meta:
        unique_together = ('company', 'name')
        index_together = ['company', 'name']
        verbose_name = _('account subtype')
        verbose_name_plural = _('account subtypes')
        default_permissions = ('view', 'add', 'change', 'delete')


class Transaction(models.Model):
    """
    The object of book-keeping is to keep a complete record of all the
    transactions that place in the company.
    """
    pass
