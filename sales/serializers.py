from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField

from invoice.serializers import ProductSerializer

from sales import models


class ProductCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = (
            'url',
            'id',
            'company',
            'name',
            'description'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:productcategory-detail'
            },
            'company': {
                'view_name': 'api:persons:company-detail'
            }
        }
 

class ProductSalesSerializer(HyperlinkedModelSerializer):
    product = ProductSerializer()
    categories = HyperlinkedIdentityField(
        view_name='api:sales:productsales-categories'
    )

    class Meta:
        model = models.ProductSales
        fields = (
            'url',
            'id',
            'product',
            'description'
            'categories'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:productsales-detail'
            }
        }


class QuotationLineSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.QuotationLine
        fields = (
            'url',
            'id',
            'product',
            'product_price_override',
            'product_vat_override',
            'product_discount',
            'quantity'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:quotationline-detail'
            }
            'product': {
                'view_name': 'api:invoice:product-detail'
            }
        }


class QuotationSerializer(HyperlinkedModelSerializer):
    quotation_lines = QuotationLineSerializer(many=True)

    class Meta:
        model = models.Quotation
        fields = (
            'url',
            'id',
            'company',
            'clients',
            'quotation_lines',
            'quotation_date',
            'notes',
            'subtotal',
            'total'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:quotation-detail'
            }
            'company': {
                'view_name': 'api:persons:company-detail'
            }
            'clients': {
                'view_name': 'api:invoice:client-detail',
                'many': True
            }
        }


class SaleLineSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.SaleLine
        fields = (
            'url',
            'id',
            'product',
            'product_price_override',
            'product_vat_override',
            'product_discount',
            'quantity'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:saleline-detail'
            }
            'product': {
                'view_name': 'api:invoice:product-detail'
            }
        }


class SaleSerializer(HyperlinkedModelSerializer):
    sale_lines = SaleLineSerializer(many=True)

    class Meta:
        model = models.Sale
        fields = (
            'url',
            'id',
            'company',
            'clients',
            'sale_lines',
            'sale_date',
            'notes',
            'subtotal',
            'total',
            'status'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:sale-detail'
            }
            'company': {
                'view_name': 'api:persons:company-detail'
            }
            'clients': {
                'view_name': 'api:invoice:client-detail',
                'many': True
            }
        }
