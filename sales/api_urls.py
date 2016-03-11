from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from sales import views


router = DefaultRouter()
router.register(r'productcategories', views.ProductCategoryViewSet)
router.register(r'products', views.ProductSalesViewSet)
router.register(r'quotationlines', views.QuotationLineViewSet)
router.register(r'quotations', views.QuotationViewSet)
router.register(r'salelines', views.SaleLineViewSet)
router.register(r'sales', views.SaleViewSet)

app_name = 'sales'
urlpatterns = [
    url(
        r'^products/(?P<pk>\d+)/categories/$',
        views.CategoriesByProductList.as_view(),
        name='productsales-categories'
    ),
    url(r'^', include(router.urls)),
]
