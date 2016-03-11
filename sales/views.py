from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from sales import models, serializers


class ProductCategoryViewSet(ModelViewSet):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class CategoriesByProductList(ListAPIView):
    serializer_class = serializers.ProductCategorySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        product = models.ProductSales.objects.filter(pk=pk)
        return product.categories.all()


class ProductSalesViewSet(ModelViewSet):
    queryset = models.ProductSales.objects.all()
    serializer_class = serializers.ProductSalesSerializer


class QuotationLineViewSet(ModelViewSet):
    queryset = models.QuotationLine.objects.all()
    serializer_class = serializers.QuotationLineSerializer


class QuotationViewSet(ModelViewSet):
    queryset = models.Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer


class SaleLineViewSet(ModelViewSet):
    queryset = models.SaleLine.objects.all()
    serializer_class = serializers.SaleLineSerializer


class SaleViewSet(ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer
