from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from sales import models, serializers


class ProductCategory(ModelViewSet):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class CategoriesByProductList(ListAPIView):
    serializer_class = serializers.ProductCategorySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        product = models.ProductSales.objects.filter(pk=pk)
        return product.categories.all()


class ProductSales(ModelViewSet):
    queryset = models.ProductSales.objects.all()
    serializer_class = serializers.ProductSalesSerializer


class QuotationLine(ModelViewSet):
    queryset = models.QuotationLine.objects.all()
    serializer_class = serializers.QuotationLineSerializer


class Quotation(ModelViewSet):
    queryset = models.Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer


class SaleLine(ModelViewSet):
    queryset = models.SaleLine.objects.all()
    serializer_class = serializers.SaleLineSerializer


class Sale(ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializer.SaleSerializer
