from common.validators import date_is_present_or_past
from contact.models import Contact
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as _noop
from persons.models import Company


class Ledger(models.Model):
    """
    Ledger is the collection of all accounts used by a company.
    Here the grouping of accounts is performed.
    """
    persons_company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='ledgers',
        related_query_name='ledger',
        on_delete=models.PROTECT,
        db_index=True
    )
    name = models.CharField(
        _('name'),
        max_length=150
    )

    def __str__(self):
        return _noop('%(persons_company)s::%(name)s') % {
            'persons_company': self.persons_company,
            'name': self.name
        }

    class Meta:
        unique_together = ('persons_company', 'name')
        verbose_name = _('ledger')
        verbose_name_plural = ('ledgers')
        default_permissions = ('view', 'add', 'change', 'delete')


ACCOUNT_TYPE_PERSONAL = 'P'
ACCOUNT_TYPE_REAL = 'R'
ACCOUNT_TYPE_NOMINAL = 'N'
ACCOUNT_TYPES = (
    (ACCOUNT_TYPE_PERSONAL, _('Personal')),
    (ACCOUNT_TYPE_REAL, _('Real')),
    (ACCOUNT_TYPE_NOMINAL, _('Nominal')),
)


class Account(models.Model):
    """
    Ledgers are organized in multiple accounts which themselves organize
    the transactions of the company.
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
    ledger = models.ForeignKey(
        Ledger,
        verbose_name=_('ledger'),
        related_name='accounts',
        related_query_name='account',
        on_delete=models.PROTECT,
        db_index=True
    )
    code = models.SlugField(
        _('code'),
        max_length=30
    )
    name = models.CharField(
        _('name'),
        max_length=150
    )
    account_type = models.CharField(
        _('main type'),
        max_length=1,
        choices=ACCOUNT_TYPES,
        blank=True,
        null=True
    )
    balance = models.DecimalField(
        _('balance'),
        max_digits=20,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop('%(code)s %(name)s') % {
            'code': self.code,
            'name': self.name
        }

    class Meta:
        unique_together = ('ledger', 'code')
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
        default_permissions = ('view', 'add', 'change', 'delete')


class Transaction(models.Model):
    """
    The object of book-keeping is to keep a complete record of all the
    transactions that place in the company.
    """
    timestamp = models.DateTimeField(
        _('timestamp'),
        auto_now_add=True
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=12,
        decimal_places=2
    )
    debit_account = models.ForeignKey(
        Account,
        verbose_name=_('debit account'),
        related_name='debit_transactions',
        related_query_name='debit_transaction',
        on_delete=models.PROTECT
    )
    debit_account_balance = models.DecimalField(
        _('account balance'),
        max_digits=20,
        decimal_places=2
    )
    credit_account = models.ForeignKey(
        Account,
        verbose_name=_('credit account'),
        related_name='credit_transactions',
        related_query_name='credit_transaction',
        on_delete=models.PROTECT
    )
    credit_account_balance = models.DecimalField(
        _('credit account balance'),
        max_digits=20,
        decimal_places=2
    )

    def __str__(self):
        return _('Transaction #%(id)s') % {'id': self.pk}

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        default_permissions = ('view', 'add', 'change', 'delete')


class CompanyAccounting(models.Model):
    """
    An Accounting extension for Company.
    """
    persons_company = models.OneToOneField(
        Company,
        verbose_name=_('company')
    )
    default_debit_account_for_cash = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for cash'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_cash = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for cash'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_creditcard = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for credit card'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_creditcard = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for credit card'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_debitcard = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for debit card'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_debitcard = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for debit card'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_bankaccount = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for bank account'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_bankaccount = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for bank account'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_check = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for check'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_check = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for check'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_paypal = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for PayPal'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_paypal = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for PayPal'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_googlewallet = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for Google Wallet'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_googlewallet = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for Google Wallet'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_applepay = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for Apple Pay'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_applepay = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for Apple Pay'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_debit_account_for_bitcoin = models.ForeignKey(
        Account,
        verbose_name=_('default debit account for Bitcoin'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )
    default_credit_account_for_bitcoin = models.ForeignKey(
        Account,
        verbose_name=_('default credit account for Bitcoin'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return str(self.persons_company)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')


PAYMENT_TYPE_SEND = 'S'
PAYMENT_TYPE_RECEIVE = 'R'
PAYMENT_TYPE_INTERNAL = 'I'
PAYMENT_TYPES = (
    (PAYMENT_TYPE_SEND, _('Send')),
    (PAYMENT_TYPE_RECEIVE, _('Receive')),
    (PAYMENT_TYPE_INTERNAL, _('Internal'))
)

PAYMENT_METHOD_CASH = 'C'
PAYMENT_METHOD_CREDITCARD = 'CC'
PAYMENT_METHOD_DEBITCARD = 'DB'
PAYMENT_METHOD_BANKACCOUNT = 'B'
PAYMENT_METHOD_CHECK = 'CH'
PAYMENT_METHOD_PAYPAL = 'P'
PAYMENT_METHOD_GOOGLEWALLET = 'GW'
PAYMENT_METHOD_APPLEPAY = 'AP'
PAYMENT_METHOD_BITCOIN = 'BC'
PAYMENT_METHODS = (
    (PAYMENT_METHOD_CASH, _('Cash')),
    (PAYMENT_METHOD_CREDITCARD, _('Credit Card')),
    (PAYMENT_METHOD_DEBITCARD, _('Debit Card')),
    (PAYMENT_METHOD_BANKACCOUNT, _('Bank Account')),
    (PAYMENT_METHOD_CHECK, _('Check')),
    (PAYMENT_METHOD_PAYPAL, _('PayPal')),
    (PAYMENT_METHOD_GOOGLEWALLET, _('Google Wallet')),
    (PAYMENT_METHOD_APPLEPAY, _('Apple Pay')),
    (PAYMENT_METHOD_BITCOIN, _('Bitcoin')),
)


class Payment(models.Model):
    """
    Payments are made by Contacts, most of the time to pay an invoice, but
    also they are made by Companies for Contacts.
    """
    accounting_company = models.ForeignKey(
        CompanyAccounting,
        verbose_name=_('company'),
        related_name='payments',
        related_query_name='payment',
        on_delete=models.PROTECT,
        db_index=True
    )
    contact_contact = models.ForeignKey(
        Contact,
        verbose_name=_('contact'),
        related_name='payments',
        related_query_name='payment',
        on_delete=models.PROTECT,
        db_index=True
    )
    payment_date = models.DateField(
        _('payment date'),
        help_text=_("Not necessarily today."),
        validators=[date_is_present_or_past]
    )
    payment_type = models.CharField(
        _('payment type'),
        max_length=1,
        default=PAYMENT_TYPE_RECEIVE,
        choices=PAYMENT_TYPES
    )
    payment_method = models.CharField(
        _('payment method'),
        max_length=2,
        default=PAYMENT_METHOD_CASH,
        choices=PAYMENT_METHODS
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=15,
        decimal_places=2
    )
    transaction = models.ForeignKey(
        Transaction,
        verbose_name=_('transaction'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.contact_contact) + ' : ' + str(self.amount)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        default_permissions = ('view', 'add', 'change', 'delete')
