from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contact.models import Contact
from geo.models import Locality, Country
from persons.models import Company
from invoice.models import (ContactInvoice,
                            CompanyInvoice,
                            INVOICE_STATUSTYPE_DRAFT,
                            InvoiceType,
                            FiscalPosition,
                            Product,
                            VAT)
from invoice_ar import models


class CompanyInvoiceARTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json',
        'invoice_ar/tests/fixtures/geo.json',
        'invoice_ar/tests/fixtures/invoicing.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:companyinvoicear-list')
        data = {
            'invoice_company': {
                'persons_company': {
                    'fantasy_name': 'IRONA',
                    'slogan': 'tfw no slogan'
                },
                'legal_name': 'Baragiola-Zanitti SH',
                'initiated_activities': '2016-01-01',
                'fiscal_position': (
                    reverse(
                        'api:invoice:fiscalposition-detail',
                        args=[FiscalPosition.objects.get(name='Do Easy').pk]
                    )
                ),
                'fiscal_address': {
                    'street_address': '9 de Julio 2454',
                    'floor_number': '',
                    'apartment_number': '',
                    'locality': reverse(
                        'api:geo:locality-detail',
                        args=[
                            Locality.objects.get(default_name='Santa Fe').pk
                        ]
                    ),
                    'postal_code': '3000'
                },
                'default_invoice_debit_account': '',
                'default_invoice_credit_account': ''
            },
            'cuit': '30111111118',
            'iibb': '123456'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.CompanyInvoiceAR.objects.get().delete()
        CompanyInvoice.objects.get().delete()
        Company.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.CompanyInvoiceAR.objects.count(), 1)

    def test_correctness(self):
        obj = models.CompanyInvoiceAR.objects.get(
            invoice_company__legal_name='Baragiola-Zanitti SH'
        )
        self.assertEqual(
            obj.invoice_company.persons_company.fantasy_name,
            'IRONA'
        )
        self.assertEqual(
            obj.invoice_company.legal_name,
            'Baragiola-Zanitti SH'
        )
        self.assertEqual(
            obj.invoice_company.persons_company.slogan,
            'tfw no slogan'
        )
        self.assertEqual(
            obj.invoice_company.initiated_activities,
            date(2016, 1, 1)
        )
        self.assertEqual(
            obj.invoice_company.fiscal_position,
            FiscalPosition.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.postal_code,
            '3000'
        )
        self.assertEqual(
            obj.cuit,
            '30111111118'
        )
        self.assertEqual(
            obj.iibb,
            '123456'
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice_ar:companyinvoicear-detail',
            args=[
                models.CompanyInvoiceAR.objects.get(
                    invoice_company__legal_name='Baragiola-Zanitti SH'
                ).pk
            ]
        )
        data = {
            'invoice_company': {
                'persons_company': {
                    'fantasy_name': 'ANORI',
                    'slogan': 'when face the slogan no'
                },
                'legal_name': 'Zanitti-Baragiola SH',
                'initiated_activities': '2015-02-03',
                'fiscal_position': reverse(
                    'api:invoice:fiscalposition-detail',
                    args=[FiscalPosition.objects.get(name='Do No Easy').pk]
                ),
                'fiscal_address': {
                    'street_address': 'San Martín 1100',
                    'floor_number': '1',
                    'apartment_number': '2',
                    'locality': reverse(
                        'api:geo:locality-detail',
                        args=[
                            Locality.objects.get(default_name='Rosario').pk
                        ]
                    ),
                    'postal_code': '2000'
                },
                'default_invoice_debit_account': '',
                'default_invoice_credit_account': ''
            },
            'cuit': '30222222229',
            'iibb': '654321'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.CompanyInvoiceAR.objects.get(
            invoice_company__legal_name='Zanitti-Baragiola SH'
        )
        self.assertEqual(
            obj.invoice_company.persons_company.fantasy_name,
            'ANORI'
        )
        self.assertEqual(
            obj.invoice_company.legal_name,
            'Zanitti-Baragiola SH'
        )
        self.assertEqual(
            obj.invoice_company.persons_company.slogan,
            'when face the slogan no'
        )
        self.assertEqual(
            obj.invoice_company.initiated_activities,
            date(2015, 2, 3)
        )
        self.assertEqual(
            obj.invoice_company.fiscal_position,
            FiscalPosition.objects.get(name='Do No Easy')
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.floor_number,
            '1'
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.apartment_number,
            '2'
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.locality,
            Locality.objects.get(pk=2)
        )
        self.assertEqual(
            obj.invoice_company.fiscal_address.postal_code,
            '2000'
        )
        self.assertEqual(
            obj.cuit,
            '30222222229'
        )
        self.assertEqual(
            obj.iibb,
            '654321'
        )


class ContactInvoiceARTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json',
        'invoice_ar/tests/fixtures/geo.json',
        'invoice_ar/tests/fixtures/invoicing.json',
        'invoice_ar/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:contactinvoicear-list')
        data = {
            'invoice_contact': {
                'contact_contact': {
                    'persons_company': reverse(
                            'api:persons:company-detail',
                            args=[
                                Company.objects.get(fantasy_name='IRONA').pk
                            ]
                     ),
                    'name': 'Tobias Riper',
                    'birth_date': '1970-07-07',
                    'born_in': reverse(
                        'api:geo:country-detail',
                        args=[
                            Country.objects.get(default_name='Argentina').pk
                        ]
                    ),
                    'phone_numbers': '555444555,333222333',
                    'extra_emails': (
                        'top@kek.com'
                    ),
                    'contact_type': 'I',
                    'home_address': {
                        'street_address': '9 de Julio 2454',
                        'floor_number': '',
                        'apartment_number': '',
                        'locality': reverse(
                            'api:geo:locality-detail',
                            args=[
                                Locality.objects.get(
                                    default_name='Santa Fe'
                                ).pk
                            ]
                        ),
                        'postal_code': '3000'
                    }
                },
                'legal_name': 'Tobias Riper',
                'fiscal_position': reverse(
                    'api:invoice:fiscalposition-detail',
                    args=[FiscalPosition.objects.get(name='Do Easy').pk]
                ),
                'fiscal_address': {
                    'street_address': '9 de Julio 2454',
                    'floor_number': '',
                    'apartment_number': '',
                    'locality': reverse(
                        'api:geo:locality-detail',
                        args=[
                            Locality.objects.get(default_name='Santa Fe').pk
                        ]
                    ),
                    'postal_code': '3000'
                }
            },
            'id_type': models.ID_TYPE_CUIT,
            'id_number': '20111111112'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.ContactInvoiceAR.objects.get().delete()
        Contact.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ContactInvoiceAR.objects.count(), 1)

    def test_correctness(self):
        obj = models.ContactInvoiceAR.objects.get(
            invoice_contact__legal_name='Tobias Riper'
        )
        contact_contact = obj.invoice_contact.contact_contact
        self.assertEqual(
            contact_contact.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            contact_contact.name,
            'Tobias Riper'
        )
        self.assertEqual(
            contact_contact.birth_date,
            date(1970, 7, 7)
        )
        self.assertEqual(
            contact_contact.born_in,
            Country.objects.get(pk=1)
        )
        self.assertEqual(
            contact_contact.phone_numbers,
            '555444555,333222333'
        )
        self.assertEqual(
            contact_contact.extra_emails,
            'top@kek.com'
        )
        self.assertEqual(
            contact_contact.contact_type,
            'I'
        )
        self.assertEqual(
            contact_contact.home_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            contact_contact.home_address.floor_number,
            ''
        )
        self.assertEqual(
            contact_contact.home_address.apartment_number,
            ''
        )
        self.assertEqual(
            contact_contact.home_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            contact_contact.home_address.postal_code,
            '3000'
        )
        self.assertEqual(
            obj.invoice_contact.legal_name,
            'Tobias Riper'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_position,
            FiscalPosition.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.postal_code,
            '3000'
        )
        self.assertEqual(
            obj.id_type,
            models.ID_TYPE_CUIT
        )
        self.assertEqual(
            obj.id_number,
            '20111111112'
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice_ar:contactinvoicear-detail',
            args=[
                models.ContactInvoiceAR.objects.get(
                    invoice_contact__legal_name='Tobias Riper'
                ).pk
            ]
        )
        data = {
            'invoice_contact': {
                'contact_contact': {
                    'persons_company': (
                        reverse(
                            'api:persons:company-detail',
                            args=[
                                Company.objects.get(fantasy_name='IRONA').pk
                            ]
                        )
                    ),
                    'name': 'Riper Tobias',
                    'birth_date': '1980-09-09',
                    'born_in': reverse(
                        'api:geo:country-detail',
                        args=[
                            Country.objects.get(default_name='Uruguay').pk
                        ]
                    ),
                    'phone_numbers': '123456',
                    'extra_emails': (
                        'kek@top.com'
                    ),
                    'contact_type': 'C',
                    'home_address': {
                        'street_address': 'San Martín 1100',
                        'floor_number': '1',
                        'apartment_number': '2',
                        'locality': reverse(
                            'api:geo:locality-detail',
                            args=[
                                Locality.objects.get(
                                    default_name='Rosario'
                                ).pk
                            ]
                        ),
                        'postal_code': '2000'
                    }
                },
                'legal_name': 'Riper Tobias',
                'fiscal_position': reverse(
                    'api:invoice:fiscalposition-detail',
                    args=[FiscalPosition.objects.get(name='Do No Easy').pk]
                ),
                'fiscal_address': {
                    'street_address': 'San Martín 1100',
                    'floor_number': '1',
                    'apartment_number': '2',
                    'locality': reverse(
                        'api:geo:locality-detail',
                        args=[
                            Locality.objects.get(default_name='Rosario').pk
                        ]
                    ),
                    'postal_code': '2000'
                }
            },
            'id_type': models.ID_TYPE_CUIL,
            'id_number': '20222222223'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.ContactInvoiceAR.objects.get(
            invoice_contact__legal_name='Riper Tobias'
        )
        contact_contact = obj.invoice_contact.contact_contact
        self.assertEqual(
            contact_contact.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            contact_contact.name,
            'Riper Tobias'
        )
        self.assertEqual(
            contact_contact.birth_date,
            date(1980, 9, 9)
        )
        self.assertEqual(
            contact_contact.born_in,
            Country.objects.get(default_name='Uruguay')
        )
        self.assertEqual(
            contact_contact.phone_numbers,
            '123456'
        )
        self.assertEqual(
            contact_contact.extra_emails,
            'kek@top.com'
        )
        self.assertEqual(
            contact_contact.contact_type,
            'C'
        )
        self.assertEqual(
            contact_contact.home_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            contact_contact.home_address.floor_number,
            '1'
        )
        self.assertEqual(
            contact_contact.home_address.apartment_number,
            '2'
        )
        self.assertEqual(
            contact_contact.home_address.locality,
            Locality.objects.get(default_name='Rosario')
        )
        self.assertEqual(
            contact_contact.home_address.postal_code,
            '2000'
        )
        self.assertEqual(
            obj.invoice_contact.legal_name,
            'Riper Tobias'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_position,
            FiscalPosition.objects.get(name='Do No Easy')
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.floor_number,
            '1'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.apartment_number,
            '2'
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.locality,
            Locality.objects.get(default_name='Rosario')
        )
        self.assertEqual(
            obj.invoice_contact.fiscal_address.postal_code,
            '2000'
        )
        self.assertEqual(
            obj.id_type,
            models.ID_TYPE_CUIL
        )
        self.assertEqual(
            obj.id_number,
            '20222222223'
        )


class ConceptTypeTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:concepttype-list')
        data = {
            'name': 'Do Easy',
            'code': '1',
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.ConceptType.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ConceptType.objects.count(), 1)

    def test_correctness(self):
        obj = models.ConceptType.objects.get(name='Do Easy')
        self.assertEqual(obj.name, 'Do Easy')
        self.assertEqual(obj.code, '1')


class InvoiceARHasVATSubtotalTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json',
        'invoice_ar/tests/fixtures/invoicing.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:invoicearhasvatsubtotal-list')
        data = {
            'vat': reverse(
                'api:invoice:vat-detail',
                args=[VAT.objects.get(name='10%').pk]
            ),
            'subtotal': 100.00,
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.InvoiceARHasVATSubtotal.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.InvoiceARHasVATSubtotal.objects.count(), 1)

    def test_correctness(self):
        obj = models.InvoiceARHasVATSubtotal.objects.get(vat__name='10%')
        self.assertEqual(
            obj.vat,
            VAT.objects.get(name='10%')
        )
        self.assertEqual(obj.subtotal, Decimal('100.00'))


class PointOfSaleTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json',
        'invoice_ar/tests/fixtures/invoicing.json',
        'invoice_ar/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:pointofsale-list')
        invoicear_company = models.CompanyInvoiceAR.objects.get(
            invoice_company__legal_name='Baragiola-Zanitti SH'
        )
        data = {
            'invoicear_company': reverse(
                'api:invoice_ar:companyinvoicear-detail',
                args=[invoicear_company.pk]
            ),
            'afip_id': 1,
            'point_of_sale_type': models.POINTOFSALE_TYPE_WEBSERVICE,
            'fiscal_address': reverse(
                'api:persons:physicaladdress-detail',
                args=[invoicear_company.invoice_company.fiscal_address.pk]
            ),
            'is_inactive': False
        } 
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.PointOfSale.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.PointOfSale.objects.count(), 1)

    def test_correctness(self):
        invoicear_company = models.CompanyInvoiceAR.objects.get(
            invoice_company__legal_name='Baragiola-Zanitti SH'
        )
        obj = models.PointOfSale.objects.get(
            invoicear_company=invoicear_company
        )
        self.assertEqual(
            obj.invoicear_company,
            invoicear_company
        )
        self.assertEqual(obj.afip_id, 1)
        self.assertEqual(
            obj.point_of_sale_type,
            models.POINTOFSALE_TYPE_WEBSERVICE
        )
        self.assertEqual(
            obj.fiscal_address,
            invoicear_company.invoice_company.fiscal_address
        )
        self.assertEqual(
            obj.is_inactive,
            False
        )


class InvoiceARTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice_ar/tests/fixtures/users.json',
        'invoice_ar/tests/fixtures/geo.json',
        'invoice_ar/tests/fixtures/invoicing.json',
        'invoice_ar/tests/fixtures/companies.json',
        'invoice_ar/tests/fixtures/products.json',
        'invoice_ar/tests/fixtures/contacts.json',
        'invoice_ar/tests/fixtures/pos.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice_ar:invoicear-list')
        data = {
            'invoicear_company': reverse(
                'api:invoice_ar:companyinvoicear-detail',
                args=[
                    models.CompanyInvoiceAR.objects.get(
                        invoice_company__legal_name='Baragiola-Zanitti SH'
                    ).pk
                ]
            ),
            'invoicear_contact': reverse(
                'api:invoice_ar:contactinvoicear-detail',
                args=[
                    models.ContactInvoiceAR.objects.get(
                        invoice_contact__legal_name='Tobias Riper'
                    ).pk
                ]
            ),
            'number': 1,
            'invoice_lines': [
                {
                    'product': reverse(
                        'api:invoice:product-detail',
                        args=[Product.objects.get(name='Do Easy').pk]
                    ),
                    'price_sold': 100.00,
                    'discount': 0.00,
                    'quantity': 2,
                    'description': 'hello there'
                },
                {
                    'product': reverse(
                        'api:invoice:product-detail',
                        args=[
                            Product.objects.get(name='Do No Easy').pk
                        ]
                    ),
                    'price_sold': 200.00,
                    'discount': 0.50,
                    'quantity': 1,
                    'description': ''
                }
            ],
            'invoice_type': reverse(
                'api:invoice:invoicetype-detail',
                args=[InvoiceType.objects.get(name='Do Easy').pk]
            ),
            'invoice_date': str(date.today()),
            'notes': 'cardio kills gains',
            'point_of_sale': reverse(
                'api:invoice_ar:pointofsale-detail',
                args=[models.PointOfSale.objects.get(afip_id=1).pk]
            ),
            'due_date': str(date.today() + timedelta(days=30)),
            'service_start': str(date.today()),
            'concept_type': reverse(
                'api:invoice_ar:concepttype-detail',
                args=[models.ConceptType.objects.get(name='Do Easy').pk]
            )
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.InvoiceAR.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.InvoiceAR.objects.count(), 1)

    def test_correctness(self):
        obj = models.InvoiceAR.objects.get(number=1)
        self.assertEqual(
            obj.invoicear_company,
            models.CompanyInvoiceAR.objects.get(
                invoice_company__legal_name='Baragiola-Zanitti SH'
            )
        )
        self.assertEqual(
            obj.invoicear_contact,
            models.ContactInvoiceAR.objects.get(
                invoice_contact__legal_name='Tobias Riper'
            )
        )
        self.assertEqual(obj.number, 1)
        self.assertEqual(
            obj.invoice_type,
            InvoiceType.objects.get(name='Do Easy')
        )
        self.assertEqual(obj.invoice_date, date.today())
        self.assertEqual(obj.notes, 'cardio kills gains')
        self.assertEqual(
            obj.point_of_sale,
            models.PointOfSale.objects.get(afip_id=1)
        )
        self.assertEqual(
            obj.due_date,
            date.today() + timedelta(days=30)
        )
        self.assertEqual(
            obj.service_start,
            date.today()
        )
        self.assertEqual(
            obj.concept_type,
            models.ConceptType.objects.get(name='Do Easy')
        )
        self.assertEqual(obj.status, INVOICE_STATUSTYPE_DRAFT)
        self.assertEqual(obj.subtotal, Decimal('300.00'))
        self.assertEqual(obj.total, Decimal('341.00'))
        self.assertEqual(obj.vat_total, Decimal('41.00'))
        self.assertEqual(
            obj.vat_subtotals.get(vat__name='10%').subtotal,
            Decimal('20.00')
        )
        self.assertEqual(
            obj.vat_subtotals.get(vat__name='21%').subtotal,
            Decimal('21.00')
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice_ar:invoicear-detail',
            args=[models.InvoiceAR.objects.get(number=1).pk]
        )
        data = {
            'invoicear_company': reverse(
                'api:invoice_ar:companyinvoicear-detail',
                args=[
                    models.CompanyInvoiceAR.objects.get(
                        invoice_company__legal_name='Zanitti-Baragiola SH'
                    ).pk
                ]
            ),
            'invoicear_contact': reverse(
                'api:invoice_ar:contactinvoicear-detail',
                args=[
                    models.ContactInvoiceAR.objects.get(
                        invoice_contact__legal_name='Riper Tobias'
                    ).pk
                ]
            ),
            'number': 2,
            'invoice_lines': [
                {
                    'product': reverse(
                        'api:invoice:product-detail',
                        args=[Product.objects.get(name='Do Easy').pk]
                    ),
                    'price_sold': 100.00,
                    'discount': 0.00,
                    'quantity': 1,
                    'description': 'The Negus used to rule Ethiopia'
                },
                {
                    'product': reverse(
                        'api:invoice:product-detail',
                        args=[
                            Product.objects.get(name='Do No Easy').pk
                        ]
                    ),
                    'price_sold': 200.00,
                    'discount': 0.00,
                    'quantity': 2,
                    'description': 'no description'
                }
            ],
            'invoice_type': reverse(
                'api:invoice:invoicetype-detail',
                args=[InvoiceType.objects.get(name='Do No Easy').pk]
            ),
            'invoice_date': str(date.today() - timedelta(days=1)),
            'notes': 'gains are killed by cardio',
            'point_of_sale': reverse(
                'api:invoice_ar:pointofsale-detail',
                args=[models.PointOfSale.objects.get(afip_id=2).pk]
            ),
            'due_date': str(date.today() + timedelta(days=29)),
            'service_start': str(date.today() - timedelta(days=1)),
            'concept_type': reverse(
                'api:invoice_ar:concepttype-detail',
                args=[models.ConceptType.objects.get(name='Do No Easy').pk]
            )
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.InvoiceAR.objects.get(number=2)
        self.assertEqual(
            obj.invoicear_company,
            models.CompanyInvoiceAR.objects.get(
                invoice_company__legal_name='Zanitti-Baragiola SH'
            )
        )
        self.assertEqual(
            obj.invoicear_contact,
            models.ContactInvoiceAR.objects.get(
                invoice_contact__legal_name='Riper Tobias'
            )
        )
        self.assertEqual(obj.number, 2)
        self.assertEqual(
            obj.invoice_type,
            InvoiceType.objects.get(name='Do No Easy')
        )
        self.assertEqual(obj.invoice_date, date.today() - timedelta(days=1))
        self.assertEqual(obj.notes, 'gains are killed by cardio')
        self.assertEqual(
            obj.point_of_sale,
            models.PointOfSale.objects.get(afip_id=2)
        )
        self.assertEqual(
            obj.due_date,
            date.today() + timedelta(days=29)
        )
        self.assertEqual(
            obj.service_start,
            date.today() - timedelta(days=1)
        )
        self.assertEqual(
            obj.concept_type,
            models.ConceptType.objects.get(name='Do No Easy')
        )
        self.assertEqual(obj.status, INVOICE_STATUSTYPE_DRAFT)
        self.assertEqual(obj.subtotal, Decimal('500.00'))
        self.assertEqual(obj.total, Decimal('594.00'))
        self.assertEqual(obj.vat_total, Decimal('94.00'))
        self.assertEqual(
            obj.vat_subtotals.get(vat__name='10%').subtotal,
            Decimal('10.00')
        )
        self.assertEqual(
            obj.vat_subtotals.get(vat__name='21%').subtotal,
            Decimal('84.00')
        )
