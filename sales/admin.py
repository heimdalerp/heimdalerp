from django.contrib import admin
from reversion.admin import VersionAdmin

from sales import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(VersionAdmin):
    pass


@admin.register(models.ProductSales)
class ProductSalesAdmin(VersionAdmin):
    pass


@admin.register(models.QuotationLine)
class QuotationLineAdmin(VersionAdmin):
    pass


@admin.register(models.Quotation)
class QuotationAdmin(VersionAdmin):
    pass


@admin.register(models.SaleLine)
class SaleLineAdmin(VersionAdmin):
    pass


@admin.register(models.Sale)
class SaleAdmin(VersionAdmin):
    pass
