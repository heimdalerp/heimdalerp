from django.contrib import admin
from reversion.admin import VersionAdmin

from sales import models


class ProductCategoryAdmin(VersionAdmin):
    pass


class ProductSalesAdmin(VersionAdmin):
    pass


class QuotationLineAdmin(VersionAdmin):
    pass


class QuotationAdmin(VersionAdmin):
    pass


class SaleLineAdmin(VersionAdmin):
    pass


class SaleAdmin(VersionAdmin):
    pass


admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductSales, ProductSalesAdmin)
admin.site.register(models.QuotationLine, QuotationLineAdmin)
admin.site.register(models.Quotation, QuotationAdmin)
admin.site.register(models.SaleLine, SaleLineAdmin)
admin.site.register(models.Sale, SaleAdmin)
